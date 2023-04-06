class Accounts:
    __instance = None

    def __init__(self):
        pass

    @property
    def organization_id(self):
        return self.__organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        self.__organization_id = organization_id

    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, organization_name):
        self.__organization_name = organization_name

    @property
    def account_id(self):
        return self.__account_id

    @account_id.setter
    def account_id(self, account_id):
        self.__account_id = account_id

    @property
    def account_name(self):
        return self.__account_name

    @account_name.setter
    def account_name(self, account_name):
        self.__account_name = account_name

    @property
    def account_email_id(self):
        return self.__account_email_id

    @account_email_id.setter
    def account_email_id(self, account_email_id):
        self.__account_email_id = account_email_id

    @property
    def account_status(self):
        return self.__account_status

    @account_status.setter
    def account_status(self, account_status):
        self.__account_status = account_status
