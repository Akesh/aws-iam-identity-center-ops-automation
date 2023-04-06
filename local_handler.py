import sys

from data.labels import Labels
from data.targets import Targets
from processors.identity_center_ops_processor import IdentityCenterOpsProcessor
from utils import helpers


def local_handler():
    try:
        ops_processor = IdentityCenterOpsProcessor()
        identity_mapping_data = ops_processor.read_and_convert_excel_sheet_data_to_list()
        for record in identity_mapping_data:
            target_type = record[Labels.TARGET_TYPE.value]  # OU or ACCOUNT
            target_value = record[Labels.TARGET_VALUE.value]  # OU_name[OU_id] or Account_name[Account_id] or ALL(All accounts in all OUs)
            principal = record[Labels.PRINCIPAL.value]  # IAM User or IAM Group
            permission_set = record[Labels.PERMISSIONS_SET.value]  # Name of the permission set
            action = record[Labels.ACTION.value]  # ADD or DELETE
            (is_valid_data, principal, permission_set) = helpers.validate_and_trim_request_data(principal, permission_set)
            if not is_valid_data:
                raise Exception("Invalid request data. Please validate excel sheet and correct IAM User/Group or permission set name")
            if target_type == Targets.ORGANIZATION_UNIT.value:
                if target_value == Targets.ALL.value:
                    ops_processor.manage_permission_set_associations_with_all_accounts(principal, permission_set, action)
                else:
                    target_ou_name, target_ou_id = helpers.get_ou_details(target_value)
                    ops_processor.manage_permission_set_association_with_ou(target_ou_name, target_ou_id, principal, permission_set, action)
            elif target_type == Targets.ACCOUNT.value:
                target_id = helpers.get_account_id_from_request_data(target_value)
                ops_processor.manage_permission_set_association_with_account(target_id, principal, permission_set, action)
    except Exception as e:
        # If any other exceptions which we didn't expect are raised
        # then fail the job and log the exception message.
        print('Function failed due to exception')
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    local_handler()
