import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

class FroggyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 5)
        self.conv2 = nn.Conv2d(16, 32, 5)
        self.fc1 = nn.Linear(32 * 53 * 53, 64)
        self.out = nn.Linear(64, 4)  # z. B. Fehlerklassen

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 32 * 53 * 53)
        x = F.relu(self.fc1(x))
        return self.out(x)

model = FroggyCNN()
model.eval()

def predict_image(img_path: str) -> int:
    image = Image.open(img_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    x = transform(image).unsqueeze(0)
    with torch.no_grad():
        out = model(x)
        return torch.argmax(out, dim=1).item()
