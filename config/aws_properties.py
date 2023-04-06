###################################################################################################################
# AWS Properties                                                                                                  #
###################################################################################################################
##AWS Identity Center region
aws_region = "ap-southeast-1"
## AWS Identity Center instance ARN and store id. You can read retrieve these vales from AWS Identity Center console
aws_identity_center_instance_arn = "arn:aws:sso:::instance/ssoins-12345abcdpqrs6789"
aws_identity_store_id = "d-1111111111" #
## Management/Root account of organization. Permission sets and User/Group association will not be performed on this account
aws_management_account_id = "999999999999"
