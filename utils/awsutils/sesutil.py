import logging

from botocore.exceptions import ClientError

from base.aws_base_processor import AWSBaseProcessor


class SES(AWSBaseProcessor):
    def __init__(self):
        super(SES, self).__init__('ses')

    def send_notification(self, subject, html_body, recipients):
        # The character encoding for the email.
        CHARSET = "UTF-8"
        try:
            # Provide the contents of the email.
            self.ses.send_email(
                Destination={'ToAddresses': recipients},
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': html_body,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': "",
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': subject,
                    },
                },
                Source=self.sender,
            )
        except ClientError as e:
            logging.error("Email sending Exception:" + e.response['Error']['Message'])
            return False
