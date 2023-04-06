from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class SSOAdmin(AWSBaseProcessor):
    def __init__(self):
        super(SSOAdmin, self).__init__('sso-admin')
        self.ssoadmin_client = super().get_service_client()
        pass

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def create_account_assignment(self, instance_arn, target_id, permission_set_arn, principal_type, principal_id):
        return self.ssoadmin_client.create_account_assignment(InstanceArn=instance_arn, TargetId=target_id,
                                                              TargetType='AWS_ACCOUNT',
                                                              PermissionSetArn=permission_set_arn,
                                                              PrincipalType=principal_type, PrincipalId=principal_id)

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def list_all_permission_sets(self, instance_arn):
        permission_sets_list = list()
        permission_sets_response = self.ssoadmin_client.list_permission_sets(InstanceArn=instance_arn)
        while True:
            permission_sets_list.extend(permission_sets_response['PermissionSets'])
            if "NextToken" in permission_sets_response:
                permission_sets_response = self.ssoadmin_client.list_permission_sets(InstanceArn=instance_arn,
                                                                                     NextToken=
                                                                                     permission_sets_response[
                                                                                         'NextToken'])
                continue
            else:
                break
        return permission_sets_list

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def describe_permission_set(self, identity_center_instance_arn, permission_sets_arn):
        return self.ssoadmin_client.describe_permission_set(InstanceArn=identity_center_instance_arn,
                                                            PermissionSetArn=permission_sets_arn)

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def list_permissions_sets_of_account(self, instance_arn, account_id):
        permission_sets_list = list()
        permission_sets_response = self.ssoadmin_client.list_permission_sets_provisioned_to_account(
            InstanceArn=instance_arn, AccountId=account_id)
        while True:
            permission_sets_list.extend(permission_sets_response['PermissionSets'])
            if "NextToken" in permission_sets_response:
                permission_sets_response = self.ssoadmin_client.list_permission_sets_provisioned_to_account(
                    InstanceArn=instance_arn, AccountId=account_id,
                    NextToken=permission_sets_response['NextToken'])
                continue
            else:
                break
        return permission_sets_list

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def list_account_assignments(self, instance_arn, account_id, permission_sets_arn):
        account_assignments_list = list()
        account_assignments_response = self.ssoadmin_client.list_account_assignments(InstanceArn=instance_arn,
                                                                                     AccountId=account_id,
                                                                                     PermissionSetArn=permission_sets_arn)
        while True:
            account_assignments_list.extend(account_assignments_response['AccountAssignments'])
            if "NextToken" in account_assignments_response:
                account_assignments_response = self.ssoadmin_client.list_account_assignments(InstanceArn=instance_arn,
                                                                                             AccountId=account_id,
                                                                                             PermissionSetArn=permission_sets_arn,
                                                                                             NextToken=
                                                                                             account_assignments_response[
                                                                                                 'NextToken'])
                continue
            else:
                break
        return account_assignments_list

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def delete_account_assignment(self, instance_arn, account_id, permission_set_id, principal_type, principal_id):
        response = self.ssoadmin_client.delete_account_assignment(InstanceArn=instance_arn, TargetId=account_id,
                                                                  TargetType='AWS_ACCOUNT',
                                                                  PermissionSetArn=permission_set_id,
                                                                  PrincipalType=principal_type,
                                                                  PrincipalId=principal_id)
        return response

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def get_account_assignment_deletion_status(self, identity_center_instance_arn, request_id):
        return self.ssoadmin_client.describe_account_assignment_deletion_status(InstanceArn=identity_center_instance_arn,
                                                                                AccountAssignmentDeletionRequestId=request_id)
