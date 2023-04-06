from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class Organizations(AWSBaseProcessor):
    def __init__(self):
        super(Organizations, self).__init__('organizations')
        self.organizations_client = super().get_service_client()
        pass

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def list_children(self, parent_id, child_type):
        return self.organizations_client.list_children(ParentId=parent_id, ChildType=child_type)

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def list_parents(self, account_id):
        return self.organizations_client.list_parents(ChildId=account_id)

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def list_accounts(self):
        accounts_list = list()
        accounts_details_response = self.organizations_client.list_accounts()
        while True:
            accounts_list.extend(accounts_details_response['Accounts'])
            if "NextToken" in accounts_details_response:
                accounts_details_response = self.organizations_client.list_accounts(
                    NextToken=accounts_details_response['NextToken'])
                continue
            else:
                break
        return accounts_list

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def describe_organizational_unit(self, organization_unit_id):
        return self.organizations_client.describe_organizational_unit(OrganizationalUnitId=organization_unit_id)
