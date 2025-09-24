from config.settings import CPU_LOW, CPU_HIGH, MEMORY_LOW, MEMORY_HIGH

class VMAnalyzer:
    def __init__(self, metrics):
        self.metrics = metrics

    def analyze(self):
        analysis = []
        for vm in self.metrics:
            cpu = vm.get("cpu_usage", 0)
            mem = vm.get("memory_usage", 0)

            status = "optimal"
            if cpu < CPU_LOW and mem < MEMORY_LOW:
                status = "underutilized"
            elif cpu > CPU_HIGH or mem > MEMORY_HIGH:
                status = "overprovisioned"

            analysis.append({
                "vm_id": vm["id"],
                "vm_type": vm["type"],
                "cpu": cpu,
                "memory": mem,
                "status": status
            })
        return analysis
