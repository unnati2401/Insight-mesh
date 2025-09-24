class VMRecommender:
    def __init__(self, analysis):
        self.analysis = analysis

        self.instance_map = {
            "t2.micro": {"down": None, "up": "t2.small"},
            "t2.small": {"down": "t2.micro", "up": "t2.medium"},
            "t2.medium": {"down": "t2.small", "up": "t2.large"},
            "t2.large": {"down": "t2.medium", "up": "t2.xlarge"}
        }

    def generate(self):
        recs = []
        for vm in self.analysis:
            vm_type = vm["vm_type"]
            cpu, memory, status = vm["cpu"], vm["memory"], vm["status"]

            suggestion = "No changes needed."
            if status == "underutilized":
                new_type = self.instance_map.get(vm_type, {}).get("down")
                if new_type:
                    suggestion = f"{vm['vm_id']} is underutilized. Consider downsizing to {new_type}."
            elif status == "overprovisioned":
                if cpu > 80 and memory < 30:
                    suggestion = f"{vm['vm_id']} is CPU-bound. Consider a CPU-optimized instance (e.g., c5.large)."
                elif memory > 80 and cpu < 30:
                    suggestion = f"{vm['vm_id']} is memory-bound. Consider a memory-optimized instance (e.g., r5.large)."
                else:
                    new_type = self.instance_map.get(vm_type, {}).get("up")
                    if new_type:
                        suggestion = f"{vm['vm_id']} is overutilized. Consider upgrading to {new_type}."

            recs.append({**vm, "recommendation": suggestion})
        return recs
