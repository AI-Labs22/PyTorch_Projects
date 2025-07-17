import torch
import torch.nn as nn
import requests

class APICallWrapper(nn.Module):
    def __init__(self, endpoint, retries=3):
        super().__init__()
        self.endpoint = endpoint
        self.retries = retries

    def forward(self, inputs):
        data = {"inputs": inputs.tolist()}
        for _ in range(self.retries):
            try:
                response = requests.post(self.endpoint, json=data, timeout=5)
                return torch.tensor(response.json()["outputs"])
            except requests.RequestException:
                continue
        raise RuntimeError("API call failed after retries.")
