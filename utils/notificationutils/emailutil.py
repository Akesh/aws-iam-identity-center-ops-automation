from base.base_processor import BaseProcessor
from utils.awsutils.sesutil import SES


class EmailProcessor(BaseProcessor):
    def __init__(self):
        super(EmailProcessor, self).__init__()
        self.ses = SES()
        pass

    def send_templated_email(self, instance_id, instance_name, error_msg):
        pass
