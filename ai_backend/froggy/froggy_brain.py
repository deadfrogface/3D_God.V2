# 🧠 Auto-Installer für torch
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torch"])
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

import json
import os

# 📁 Pfade
_memory_path = os.path.join(os.path.dirname(__file__), "froggy_memory.json")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "froggy_model.pt")

# 🧠 Einfaches Feedforward-Netz für Froggys Entscheidungsfindung
class FroggyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(7, 64)   # 7 Feature-Werte aus Log
        self.fc2 = nn.Linear(64, 32)
        self.out = nn.Linear(32, 4)   # 4 Klassen (Fehlertypen)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)

# Globale Modellinstanz
_model = FroggyNet()
_model.eval()

# 💾 Speicherfunktionen
def _load_memory():
    if os.path.exists(_memory_path):
        with open(_memory_path, "r") as f:
            return json.load(f)
    return []

def _save_memory(memory):
    with open(_memory_path, "w") as f:
        json.dump(memory, f, indent=2)

def save_model():
    torch.save(_model.state_dict(), MODEL_PATH)

def load_model():
    global _model
    if os.path.exists(MODEL_PATH):
        _model.load_state_dict(torch.load(MODEL_PATH))
        _model.eval()
        print("✅ Froggy-Modell geladen.")

# 🔁 Training
def train_on_example(features: list, label: int):
    global _model
    _model.train()
    optimizer = torch.optim.Adam(_model.parameters(), lr=0.001)

    x = torch.tensor(features).float().unsqueeze(0)
    y = torch.tensor([label]).long()

    for _ in range(10):  # 10 Epochen Training
        optimizer.zero_grad()
        out = _model(x)
        loss = F.cross_entropy(out, y)
        loss.backward()
        optimizer.step()

    memory = _load_memory()
    memory.append({"x": features, "y": label})
    _save_memory(memory)
    save_model()

# 🧠 Feedback lernen
def train_feedback(features: list, correct_label: int):
    print(f"[Froggy Feedback] 📚 Korrigiere mit Label {correct_label}")
    train_on_example(features, correct_label)

# 🔮 Vorhersage
def predict(features: list) -> int:
    global _model
    _model.eval()
    x = torch.tensor(features).float().unsqueeze(0)
    with torch.no_grad():
        out = _model(x)
        return torch.argmax(out, dim=1).item()

# 🟢 Modell beim Start laden
load_model()