import json

class AWSService:
    def get_metrics(self):
        with open("data/aws_dummy.json") as f:
            return json.load(f)
