import json

class GCPService:
    def get_metrics(self):
        with open("data/gcp_dummy.json") as f:
            return json.load(f)
