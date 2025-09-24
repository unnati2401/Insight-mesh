from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from config.settings import AZURE_SUBSCRIPTION_ID, RESOURCE_GROUP
import random

class AzureService:
    def __init__(self, subscription_id=AZURE_SUBSCRIPTION_ID):
        self.credential = DefaultAzureCredential()
        self.client = ComputeManagementClient(self.credential, subscription_id)

    def get_metrics(self):
        vms = self.client.virtual_machines.list(RESOURCE_GROUP)
        results = []
        for vm in vms:
            results.append({
                "id": vm.name,
                "type": vm.hardware_profile.vm_size,
                "cpu_usage": random.randint(10, 95),
                "memory_usage": random.randint(10, 95),
                "cost": random.randint(5, 100)
            })
        return results
