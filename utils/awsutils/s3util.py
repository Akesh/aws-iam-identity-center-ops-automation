from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class S3(AWSBaseProcessor):
    def __init__(self):
        super(S3, self).__init__('s3')
        self.s3_client = super().get_service_client()
        pass

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def upload_file_to_s3(self, bucket_name, object_key, data):
        return self.s3_client.put_object(ACL='bucket-owner-full-control', Bucket=bucket_name, Key=object_key, Body=data,
                                         ContentType='application/json',
                                         ServerSideEncryption='AES256')

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def get_object(self, bucket_name, object_key):
        return self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
