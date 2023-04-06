import re

regex = "^[a-z0-9]+[\._+]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


def get_account_id_from_request_data(target_account):
    # Function to read account id from a string like Account Name[12345678912]
    return target_account[target_account.find("[") + 1:target_account.find("]")].strip()


def is_non_empty_list(list_data):
    if len(list_data) != 0:
        return True
    return False


def get_principal_type(principal):
    """
    If principal is email id then return "USER" else return "GROUP"
    @param principal:
    @return: string
    """
    if is_email(principal):
        return "USER"
    return "GROUP"


def is_email(principal):
    """
    Check if principal is email id based on regular expression
    @param principal:
    @return: Boolean
    """
    if re.search(regex, principal):
        return True
    return False


def get_ou_details(target_value):
    """
    Read organization name from the format OU_NAME[OU_ID]
    @param target_value:
    @return:
    """
    ou_name = target_value[0: target_value.find("[")].strip()
    ou_id = target_value[target_value.find("[") + 1:target_value.find("]")].strip()
    return ou_name, ou_id


def validate_and_trim_request_data(principal, permission_set):
    if principal and permission_set:
        trimmed_lowered_principal = str(principal).strip().lower()
        trimmed_lowered_permission_set = str(permission_set).strip().lower()
        return True, trimmed_lowered_principal, trimmed_lowered_permission_set
    return False, None, None
