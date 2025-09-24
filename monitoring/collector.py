from services.aws_service import AWSService
from services.azure_service import AzureService
from services.gcp_service import GCPService

class VMCollector:
    def __init__(self, csp, subscription=None):
        self.csp = csp
        self.subscription = subscription

    def collect(self):
        if self.csp == "AWS":
            return AWSService().get_metrics()
        elif self.csp == "Azure":
            return AzureService(self.subscription).get_metrics()
        elif self.csp == "GCP":
            return GCPService().get_metrics()
        return []
