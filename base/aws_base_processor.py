import boto3

from .base_processor import BaseProcessor


class AWSBaseProcessor(BaseProcessor):
    service_client = None

    def __init__(self, aws_service_name):
        super().__init__()
        self.service = aws_service_name

    def get_service_client(self):
        """
        Create boto3 client using AWS credentials
        :return:client
        """
        # if service_client is already created then no need to create it again
        if self.service_client:
            # print(">>>>> client already created for {} in region {}".format(self.service, self.region))
            return self.service_client
        else:
            # print(">>>>> creating new boto3 client for {} in region {}".format(self.service, self.account))
            self.service_client = boto3.client(self.service)
        return self.service_client

    def __create_session(self):
        """
        Create boto3 client using default credentials
        :return:
        """
        session = boto3.session.Session()
        return session.client(self.service)
