# ai_backend/froggy/froggy_cnn.py

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

class FroggyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 5)
        self.conv2 = nn.Conv2d(16, 32, 3)
        self.conv3 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(64 * 26 * 26, 128)
        self.out = nn.Linear(128, 4)  # Fehlerklassen

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv3(x))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 64 * 26 * 26)
        x = F.relu(self.fc1(x))
        return self.out(x)

_model = FroggyCNN()
_model.eval()

_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_image_class(img_path: str) -> int:
    image = Image.open(img_path).convert("RGB")
    x = _transform(image).unsqueeze(0)
    with torch.no_grad():
        out = _model(x)
        return torch.argmax(out, dim=1).item()
