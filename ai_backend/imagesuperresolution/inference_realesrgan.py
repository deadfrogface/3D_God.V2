import os
import argparse
import cv2
import torch
import numpy as np

from utils import set_realesrgan_arch
from torchvision.transforms.functional import normalize

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, help='Eingabebild')
    parser.add_argument('-o', '--output', type=str, default=None, help='Zielbild')
    parser.add_argument('-n', '--model_name', type=str, default='RealESRGAN_x4plus', help='Modellname')
    parser.add_argument('--tile', type=int, default=0, help='Tile size für RAM-optimierte Inferenz')
    parser.add_argument('--face_enhance', action='store_true', help='GFPGAN verwenden (nicht empfohlen, wenn nicht vorhanden)')
    parser.add_argument('--half', action='store_true', help='Verwende FP16 (nur CUDA)')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output or os.path.join("output", os.path.basename(input_path))
    model_name = args.model_name

    model_path = os.path.join(os.path.dirname(__file__), 'weights', model_name + '.pth')

    if not os.path.isfile(input_path):
        print("❌ Eingabebild nicht gefunden:", input_path)
        return

    if not os.path.isfile(model_path):
        print("❌ Modellgewicht nicht gefunden:", model_path)
        return

    print("📦 Lade Modell:", model_name)
    model = set_realesrgan_arch(model_name)
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()

    if torch.cuda.is_available():
        model = model.cuda()
        if args.half:
            model = model.half()

    # Bild laden
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    img = img.astype(np.float32) / 255.
    img = torch.from_numpy(np.transpose(img, (2, 0, 1))).unsqueeze(0)

    if torch.cuda.is_available():
        img = img.cuda()
        if args.half:
            img = img.half()

    with torch.no_grad():
        output = model(img)

    output_img = output.squeeze().float().cpu().clamp_(0, 1).numpy()
    output_img = np.transpose(output_img, (1, 2, 0))
    output_img = (output_img * 255.0).round().astype(np.uint8)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, output_img)
    print("✅ Hochskaliertes Bild gespeichert:", output_path)

if __name__ == '__main__':
    main()
