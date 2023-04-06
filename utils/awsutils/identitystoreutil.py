from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class IdentityStore(AWSBaseProcessor):
    def __init__(self):
        super(IdentityStore, self).__init__('identitystore')
        self.identitystore_client = super().get_service_client()
        pass

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def list_all_groups(self, identity_store_id):
        identity_groups_list = list()
        identity_groups_list_response = self.identitystore_client.list_groups(IdentityStoreId=identity_store_id)
        while True:
            identity_groups_list.extend(identity_groups_list_response['Groups'])
            if "NextToken" in identity_groups_list_response:
                identity_groups_list_response = self.identitystore_client.list_groups(IdentityStoreId=identity_store_id,
                                                                                      NextToken=
                                                                                      identity_groups_list_response[
                                                                                          'NextToken'])
                continue
            else:
                break
        return identity_groups_list

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def list_all_users(self, identity_store_id):
        identity_users_list = list()
        identity_users_list_response = self.identitystore_client.list_users(IdentityStoreId=identity_store_id)
        while True:
            identity_users_list.extend(identity_users_list_response['Users'])
            if "NextToken" in identity_users_list_response:
                identity_users_list_response = self.identitystore_client.list_users(IdentityStoreId=identity_store_id,
                                                                                    NextToken=
                                                                                    identity_users_list_response[
                                                                                        'NextToken'])
                continue
            else:
                break
        return identity_users_list