from enum import Enum


class Labels(Enum):
    PRINCIPAL = "IAM Group/User"
    PERMISSIONS_SET = "Permission Sets"
    TARGET_TYPE = "Target Type"
    TARGET_VALUE = "Target Value"
    ACTION = "Action"
