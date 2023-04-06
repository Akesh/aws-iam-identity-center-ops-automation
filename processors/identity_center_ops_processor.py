import logging
import sys
import time

import pandas as pd
from botocore.exceptions import ClientError

from base.base_processor import BaseProcessor
from config import aws_properties
from data.accounts import Accounts
from data.actions import Actions
from data.style import Style
from utils import helpers
from utils.awsutils.identitystoreutil import IdentityStore
from utils.awsutils.organizationsutil import Organizations
from utils.awsutils.s3util import S3
from utils.awsutils.ssoadminutil import SSOAdmin

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setLevel(logging.DEBUG)
LOGGER.addHandler(HANDLER)


class IdentityCenterOpsProcessor(BaseProcessor):
    def __init__(self):
        super(IdentityCenterOpsProcessor, self).__init__()
        self.identity_center_instance_arn = aws_properties.aws_identity_center_instance_arn
        self.s3 = S3()
        self.organizations = Organizations()
        self.ssoadmin = SSOAdmin()
        self.identitystore = IdentityStore()
        self.principal_id_map = self.list_all_principal_details()
        self.permission_sets_name_arn_map = self.list_all_permission_sets_details()
        self.organization_data = self.load_organization_data()

    def read_and_convert_excel_sheet_data_to_list(self):
        """
        Donwload excel sheet from S3 bucket and read data
        @return:
        """
        # obj = self.s3.get_object(automation_properties.identity_center_ops_bucket,
        #                         automation_properties.identity_center_ops_file)
        # obj_data = obj['Body'].read()
        data = pd.read_excel('file/Identity Center Access Management.xlsx')
        # data = pd.read_excel(io.BytesIO(obj_data))
        identity_map_list = list()
        for entry in data.iterrows():
            identity_map_list.append(entry[1].to_dict())
        return identity_map_list

    def list_all_permission_sets_details(self):
        """
        List permission sets from identity center
        @return:
        """
        permission_sets_arn_map = dict()
        try:
            permission_sets_list = self.ssoadmin.list_all_permission_sets(self.identity_center_instance_arn)
            for permission_sets_arn in permission_sets_list:
                permission_sets_details_response = self.ssoadmin.describe_permission_set(self.identity_center_instance_arn, permission_sets_arn)
                permission_set_details = permission_sets_details_response["PermissionSet"]
                lowered_permission_set_name = str(permission_set_details["Name"]).lower()
                permission_sets_arn_map[lowered_permission_set_name] = permission_set_details["PermissionSetArn"]
        except ClientError as exe:
            self.error_and_exit('Failed to list permission sets details: ' + str(exe))
        return permission_sets_arn_map

    def list_all_principal_details(self):
        """
        List all IAM Users/Groups from Identity center
        @return:
        """
        principal_id_map = dict()
        try:
            identity_groups_list = self.identitystore.list_all_groups(aws_properties.aws_identity_store_id)
            identity_users_list = self.identitystore.list_all_users(aws_properties.aws_identity_store_id)
            for group in identity_groups_list:
                lowered_group_name = str(group["DisplayName"]).lower()
                principal_id_map[lowered_group_name] = group["GroupId"]

            for user in identity_users_list:
                lowered_user_name = str(user["UserName"]).lower()
                principal_id_map[lowered_user_name] = user["UserId"]
        except ClientError as exe:
            self.error_and_exit('Failed to list principal details: ' + str(exe))
        return principal_id_map

    def manage_permission_set_association_with_account(self, target_id, principal, permission_set, action):
        """
        Manage association of IAM User/Group and permission set with an AWS account
        @param target_id:
        @param principal:
        @param permission_set:
        @param action:
        @return:
        """
        result = None
        try:
            # Check if principal id is present in identity center
            if not self.does_principal_exists(principal):
                self.error_and_exit(Style.TXT_ERR_STYLE.value + "{}: Invalid IAM User/Group name or User/Group doesn't exist.".format(principal) + Style.RESET_STYLE.value)
            # Check if permissions set is present in identity center
            if not self.does_permission_set_exists(permission_set):
                self.error_and_exit(Style.TXT_ERR_STYLE.value + "{}: Invalid permission set name or permission set doesn't exist.".format(permission_set) + Style.RESET_STYLE.value)
            principal_type = helpers.get_principal_type(principal)
            principal_id = self.principal_id_map[principal]
            permission_set_arn = self.permission_sets_name_arn_map[permission_set]
            if action == Actions.ADD.value:
                result = self.create_account_assignment(target_id, permission_set_arn, principal_type, principal_id)
            elif action == Actions.DELETE.value:
                result = self.delete_account_assignment(target_id, permission_set_arn, principal_type, principal_id)
            return result
        except ClientError as exe:
            self.error_and_exit('Failed to associate/delete permissions with account: ' + str(exe))

        return None

    def manage_permission_set_association_with_ou(self, target_ou_name, target_ou_id, principal, permission_set, action):
        """
        Manage association of IAM User/Group and permission set with organization unit
        @param target_ou_name:
        @param target_ou_id:
        @param principal:
        @param permission_set:
        @param action:
        @return:
        """
        try:
            for account in self.organization_data:
                if str.upper(account.organization_name) == str.upper(target_ou_name) and account.organization_id == target_ou_id:
                    response = self.manage_permission_set_association_with_account(account.account_id, principal, permission_set, action)
        except ClientError as exe:
            self.error_and_exit('Failed to associate/delete permissions with OU: ' + str(exe))

        return None

    def generate_account_details_data(self, account_details, ou_details):
        """
        Populate account details data in account object
        @param account_details:
        @param ou_details:
        @return:
        """
        account = Accounts()
        account.account_id = account_details["Id"]
        account.account_name = account_details["Name"]
        account.account_email_id = account_details["Email"]
        account.account_status = account_details["Status"]
        account.organization_id = ou_details["Id"]
        account.organization_name = ou_details["Name"]
        return account

    def load_organization_data(self):
        """
        Iterate entire organization and populate all OUs and accounts with necessary details
        @return:
        """
        accounts = list()
        try:
            accounts_list_response = self.organizations.list_accounts()
            if accounts_list_response:
                for account_details in accounts_list_response:
                    parents_list_response = self.organizations.list_parents(account_details["Id"])
                    if helpers.is_non_empty_list(parents_list_response):
                        parent_id = parents_list_response["Parents"][0]["Id"]
                        account = None
                        if parents_list_response["Parents"][0]["Type"] == "ORGANIZATIONAL_UNIT":
                            describe_ou_response = self.organizations.describe_organizational_unit(parent_id)
                            ou_details = describe_ou_response["OrganizationalUnit"]
                            account = self.generate_account_details_data(account_details, ou_details)
                        elif parents_list_response["Parents"][0]["Type"] == "ROOT":
                            account = self.generate_account_details_data(account_details,
                                                                         ou_details={"Id": parent_id, "Name": "ROOT"})
                        # Do not perform any operations on master account
                        if account.account_id == aws_properties.aws_management_account_id:
                            continue
                        accounts.append(account)
                    else:
                        self.raise_exception("load_organization_data>> Something wrong listing parents of accounts.")
            return accounts
        except ClientError as exe:
            self.error_and_exit('Failed to load organization data: ' + str(exe))

    def manage_permission_set_associations_with_all_accounts(self, principal, permission_set, action):
        """
        Associate permission sets and principal with all accounts in an organization
        @param action:
        @param principal:
        @param permission_set:
        @return:
        """
        try:
            for account in self.organization_data:
                response = self.manage_permission_set_association_with_account(account.account_id, principal, permission_set, action)
        except ClientError as exe:
            self.error_and_exit('Failed to associate permissions with OU: ' + str(exe))

    def does_principal_exists(self, principal):
        """
        @param principal:
        @return: Boolean value based on the presence of principal
        """
        if principal in self.principal_id_map:
            return True
        return False

    def does_permission_set_exists(self, permission_set):
        """
        @param permission_set:
        @return: Boolean value based on the presence of permission set
        """
        if permission_set in self.permission_sets_name_arn_map:
            return True
        return False

    def create_account_assignment(self, target_id, permission_set_arn, principal_type, principal_id):
        """
        Associate IAM User/IAM Group with permissions set to AWS Account in Identity Center
        @param target_id:
        @param permission_set_arn:
        @param principal_type:
        @param principal_id:
        @return:
        """
        response = None
        try:
            if not self.does_association_exist(target_id, permission_set_arn, principal_type, principal_id):
                response = self.ssoadmin.create_account_assignment(self.identity_center_instance_arn, target_id, permission_set_arn, principal_type, principal_id)
                if response and response["AccountAssignmentCreationStatus"] == "FAILED":
                    self.error_and_exit("Permission set association failed for AWS account {} and failure reason is {}".format(response["TargetId"], response["FailureReason"]))
                LOGGER.info("Successfully associated {} {} and permission_set {} with AWS account {}".format(principal_type, principal_id, permission_set_arn, target_id))
            else:
                self.error_and_continue(
                    Style.TXT_HIGHLIGHT.value + "Association already exist for AWS account {} with {} {} and permission set {}".format(target_id, principal_type, principal_id,
                                                                                                                                       permission_set_arn) + Style.RESET_STYLE.value)
        except ClientError as exe:
            error_code = str(exe.response['Error']['Code'])
            if error_code == "ConflictException":
                LOGGER.info(Style.BG_HIGHLIGHT.value + "Conflicting execution occurred. Attempting retry" + Style.RESET_STYLE.value)
                time.sleep(5)
                return self.create_account_assignment(target_id, permission_set_arn, principal_type, principal_id)
            self.error_and_exit(Style.TXT_ERR_STYLE.value + "Account association failed for AWS account {} and error is: {}".format(target_id, str(exe)) + Style.RESET_STYLE.value)
        return response

    def delete_account_assignment(self, target_id, permission_set_arn, principal_type, principal_id):
        """
        Delete association of IAM User/Group and permission set for AWS account in Identity center
        @param target_id:
        @param permission_set_arn:
        @param principal_type:
        @param principal_id:
        @return:
        """
        response = None
        try:
            if self.does_association_exist(target_id, permission_set_arn, principal_type, principal_id):
                response = self.ssoadmin.delete_account_assignment(self.identity_center_instance_arn, target_id, permission_set_arn, principal_type, principal_id)
                if response and response["AccountAssignmentDeletionStatus"] == "FAILED":
                    self.error_and_exit("Account association failed for AWS account {} and failure reason is {}".format(response["TargetId"], response["FailureReason"]))
                LOGGER.info(
                    "Successfully deleted association of {} {} and permission_set {} from AWS account {}".format(principal_type, principal_id, permission_set_arn, target_id))
            else:
                self.error_and_continue(
                    Style.TXT_HIGHLIGHT.value + "Association doesn't exist for AWS account {} with {} {} and permission set {}".format(target_id, principal_type, principal_id,
                                                                                                                                       permission_set_arn) + Style.RESET_STYLE.value)
        except ClientError as exe:
            error_code = str(exe.response['Error']['Code'])
            if error_code == "ConflictException":
                LOGGER.info(Style.BG_HIGHLIGHT.value + "Conflicting execution occurred. Attempting retry" + Style.RESET_STYLE.value)
                time.sleep(5)
                return self.delete_account_assignment(target_id, permission_set_arn, principal_type, principal_id)
            self.error_and_exit(
                Style.TXT_ERR_STYLE.value + "Account association deletion failed for AWS account {} and error is: {}".format(target_id, str(exe)) + Style.RESET_STYLE.value)
        return response

    def does_association_exist(self, target_id, permission_set_arn, principal_type, principal_id):
        """
        Check if principal and permission set is associated with an AWS account
        @param target_id:
        @param permission_set_arn:
        @param principal_type:
        @param principal_id:
        @return:
        """
        response = self.ssoadmin.list_account_assignments(self.identity_center_instance_arn, target_id, permission_set_arn)
        if response and len(response) > 0:
            for account_assignment_details in response:
                if account_assignment_details["PrincipalId"] == principal_id:
                    return True
        return False
