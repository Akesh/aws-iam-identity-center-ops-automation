from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class CodePipeline(AWSBaseProcessor):
    def __init__(self):
        super(CodePipeline, self).__init__('codepipeline')
        self.codepipeline_client = super().get_service_client()
        pass

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def put_job_failure_result(self, jobId, failureDetails):
        return self.codepipeline_client.put_job_failure_result(jobId=jobId, failureDetails=failureDetails)

    @AWSRetry.backoff(tries=20, delay=5, added_exceptions="ThrottlingException")
    def put_job_success_result(self, jobId):
        return self.codepipeline_client.put_job_success_result(jobId=jobId)
