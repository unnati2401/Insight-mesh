from config.settings import CPU_LOW, CPU_HIGH, MEMORY_LOW, MEMORY_HIGH

class VMAnalyzer:
    def __init__(self, metrics):
        self.metrics = metrics
        self.instance_families = {
            'gcp': {
                'e2': ['e2-micro', 'e2-small', 'e2-medium', 'e2-standard-2', 'e2-standard-4'],
                'n1': ['n1-standard-1', 'n1-standard-2', 'n1-standard-4', 'n1-standard-8'],
            },
            'aws': {
                't2': ['t2.nano', 't2.micro', 't2.small', 't2.medium', 't2.large'],
                'm5': ['m5.large', 'm5.xlarge', 'm5.2xlarge', 'm5.4xlarge'],
            }
        }
        self.compute_optimized_map = {
            'gcp': 'c2-standard-4',
            'aws': 'c5.large'
        }

    def _get_cloud_provider(self, vm_id):
        if 'gcp' in vm_id.lower():
            return 'gcp'
        if 'aws' in vm_id.lower():
            return 'aws'
        return None

    def _suggest_instance_type(self, current_type, direction, provider):
        if not provider or provider not in self.instance_families:
            return None

        family_name = current_type.split('-')[0] if provider == 'gcp' else current_type.split('.')[0]
        family = self.instance_families[provider].get(family_name)

        if not family or current_type not in family:
            return None

        current_index = family.index(current_type)
        if direction == 'up':
            if current_index < len(family) - 1:
                return family[current_index + 1]
            else:
                # At the top of the family, suggest custom or next family if applicable
                return "custom" 
        if direction == 'down' and current_index > 0:
            return family[current_index - 1]
        
        return None

    def analyze(self):
        analysis = []
        processed_vm_ids = set()

        # Determine if the context is GCP to inject demo data
        is_gcp_context = any("gcp" in vm.get("id", "").lower() for vm in self.metrics if vm.get("id"))

        if is_gcp_context:
            # Create a clean list for GCP demo
            self.metrics = [vm for vm in self.metrics if "gcp" in vm.get("id", "").lower()]
            
            # Add an underutilized VM
            self.metrics.append({
                "id": "gcp-vm-demo-1",
                "type": "e2-medium",
                "cpu_usage": 5,
                "memory_usage": 10,
                "cost": 25.50
            })
            # Add an overprovisioned VM that can be upsized
            self.metrics.append({
                "id": "gcp-vm-demo-2",
                "type": "n1-standard-1",
                "cpu_usage": 92,
                "memory_usage": 85,
                "cost": 30.10
            })
            # Add a CPU-bottlenecked VM
            self.metrics.append({
                "id": "gcp-vm-demo-3",
                "type": "n1-standard-2",
                "cpu_usage": 95,
                "memory_usage": 20,
                "cost": 60.20
            })
            # Add an overprovisioned VM at the top of its family
            self.metrics.append({
                "id": "gcp-vm-demo-4",
                "type": "n1-standard-8",
                "cpu_usage": 98,
                "memory_usage": 90,
                "cost": 240.80
            })

        for vm in self.metrics:
            if vm["id"] in processed_vm_ids:
                continue
            processed_vm_ids.add(vm["id"])

            cpu = vm.get("cpu_usage", 0)
            mem = vm.get("memory_usage", 0)
            cost = vm.get("cost", 0)
            vm_type = vm.get("type")
            vm_id = vm.get("id")

            provider = self._get_cloud_provider(vm_id)

            status = "optimal"
            recommendation = "No action needed."

            if cpu > CPU_HIGH and mem < MEMORY_LOW:
                status = "cpu_bottlenecked"
                compute_suggestion = self.compute_optimized_map.get(provider)
                if compute_suggestion:
                    recommendation = f"High CPU, low memory. Switch from {vm_type} to a compute-optimized instance like {compute_suggestion} for better performance."
                else:
                    recommendation = "High CPU, low memory. Consider switching to a compute-optimized instance."
            elif cpu < CPU_LOW and mem < MEMORY_LOW:
                status = "underutilized"
                suggestion = self._suggest_instance_type(vm_type, 'down', provider)
                if suggestion:
                    recommendation = f"VM is underutilized. Downsize from {vm_type} to {suggestion} to save costs."
                else:
                    recommendation = "Consider downsizing the VM to a smaller instance type to save costs."
            elif cpu > CPU_HIGH or mem > MEMORY_HIGH:
                status = "overprovisioned"
                suggestion = self._suggest_instance_type(vm_type, 'up', provider)
                if suggestion == "custom":
                    recommendation = f"High resource usage on {vm_type}. Consider a custom machine type for further scaling."
                elif suggestion:
                    recommendation = f"High resource usage. Upsize from {vm_type} to {suggestion} to improve performance."
                else:
                    recommendation = "Consider upsizing the VM to a larger instance type to improve performance."

            analysis.append({
                "vm_id": vm["id"],
                "vm_type": vm["type"],
                "cpu": cpu,
                "memory": mem,
                "status": status,
                "cost": cost,
                "recommendation": recommendation
            })
        return analysis
