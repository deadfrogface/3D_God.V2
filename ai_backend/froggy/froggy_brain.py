import torch
import torch.nn as nn
import torch.nn.functional as F
import json
import os

# Einfaches Feedforward-Netz als Basis
class FroggyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(7, 64)
        self.fc2 = nn.Linear(64, 32)
        self.out = nn.Linear(32, 4)  # z. B. Fehlerklasse 0–3

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)

_model = FroggyNet()
_memory_path = os.path.join(os.path.dirname(__file__), "froggy_memory.json")

def load_brain():
    if os.path.exists(_memory_path):
        with open(_memory_path, "r") as f:
            data = json.load(f)
            return data
    return []

def save_brain(memory):
    with open(_memory_path, "w") as f:
        json.dump(memory, f, indent=2)

def train_on_example(features: list, label: int):
    global _model
    _model.train()
    optimizer = torch.optim.Adam(_model.parameters(), lr=0.001)

    x = torch.tensor(features).float().unsqueeze(0)
    y = torch.tensor([label]).long()

    for _ in range(10):  # 10 Epochen auf Einzeldatenpunkt
        optimizer.zero_grad()
        out = _model(x)
        loss = F.cross_entropy(out, y)
        loss.backward()
        optimizer.step()

    # Speichern im Langzeitgedächtnis
    memory = load_brain()
    memory.append({"x": features, "y": label})
    save_brain(memory)

def predict(features: list) -> int:
    _model.eval()
    x = torch.tensor(features).float().unsqueeze(0)
    with torch.no_grad():
        out = _model(x)
        pred = torch.argmax(out, dim=1).item()
        return pred
