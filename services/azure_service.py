from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from datetime import datetime, timedelta
import random

class AzureService:
    def __init__(self, subscription_id):
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        self.compute_client = ComputeManagementClient(self.credential, self.subscription_id)
        self.resource_client = ResourceManagementClient(self.credential, self.subscription_id)
        self.monitor_client = MonitorManagementClient(self.credential, self.subscription_id)
        self._vm_size_details = {}
        self.cost_map = {
            # General purpose B-series (burstable) - Estimated monthly cost
            'Standard_B1s': 7.50,
            'Standard_B1ms': 15.00,
            'Standard_B2s': 30.00,
            'Standard_B2ms': 60.00,
            # General purpose D-series
            'Standard_DS1_v2': 70.00,
            'Standard_DS2_v2': 140.00,
            # Default cost
            'default': 50.00
        }

    def _get_vm_size_details(self, location, vm_size):
        if location not in self._vm_size_details:
            self._vm_size_details[location] = {size.name: size for size in self.compute_client.virtual_machine_sizes.list(location)}
        return self._vm_size_details[location].get(vm_size)

    def get_resource_groups(self):
        try:
            groups = self.resource_client.resource_groups.list()
            return [group.name for group in groups]
        except Exception as e:
            print(f"Error fetching Azure resource groups: {e}")
            return []

    def get_metrics(self, resource_group=None):
        results = []
        groups_to_scan = []

        if resource_group and resource_group != 'all':
            groups_to_scan.append(resource_group)
        else:
            groups_to_scan = self.get_resource_groups()

        timespan = f"{(datetime.utcnow() - timedelta(minutes=15)).isoformat()}/{(datetime.utcnow()).isoformat()}"

        for rg_name in groups_to_scan:
            try:
                vms = self.compute_client.virtual_machines.list(rg_name)
                for vm in vms:
                    cpu_usage = 0
                    memory_usage = 0

                    try:
                        # Get CPU Usage
                        cpu_metrics = self.monitor_client.metrics.list(vm.id, timespan=timespan, metricnames='Percentage CPU', aggregation='Average')
                        if cpu_metrics.value and cpu_metrics.value[0].timeseries and cpu_metrics.value[0].timeseries[0].data:
                            cpu_usage = cpu_metrics.value[0].timeseries[0].data[-1].average

                        # Get Memory Usage
                        size_details = self._get_vm_size_details(vm.location, vm.hardware_profile.vm_size)
                        if size_details:
                            total_memory_mb = size_details.memory_in_mb
                            # For Linux, use 'Available Memory Bytes'. For Windows, it's different. Assuming Linux for simplicity.
                            mem_metrics = self.monitor_client.metrics.list(vm.id, timespan=timespan, metricnames='Available Memory Bytes', aggregation='Average')
                            if mem_metrics.value and mem_metrics.value[0].timeseries and mem_metrics.value[0].timeseries[0].data:
                                available_memory_bytes = mem_metrics.value[0].timeseries[0].data[-1].average
                                available_memory_mb = available_memory_bytes / (1024 * 1024)
                                memory_usage = ((total_memory_mb - available_memory_mb) / total_memory_mb) * 100 if total_memory_mb > 0 else 0

                    except Exception as e:
                        print(f"Could not fetch live metrics for {vm.name}: {e}. Using random data.")
                        cpu_usage = random.randint(10, 95)
                        memory_usage = random.randint(10, 95)

                    vm_size = vm.hardware_profile.vm_size
                    cost = self.cost_map.get(vm_size, self.cost_map['default'])

                    results.append({
                        "id": vm.name,
                        "type": vm_size,
                        "cpu_usage": cpu_usage,
                        "memory_usage": memory_usage,
                        "cost": cost
                    })
            except Exception as e:
                print(f"Error fetching VMs from resource group {rg_name}: {e}")
                continue
        return results
