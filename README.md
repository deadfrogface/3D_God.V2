don´t forget to put yolov7 locally in the right folder!
Download link: https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt
the folder structure: ai_backend/yolov7/yolov7.pt
___________________________________________________________________________
don´t forget to put triposr locally in the right folder!
Download link: https://huggingface.co/stabilityai/TripoSR/blob/main/model.ckpt
the folder structure: ai_backend/triposr/checkpoints/epoch_00009.ckpt
___________________________________________________________________________
don´t forget to put imagesuperresolution locally in the right folder!
Download link: https://huggingface.co/ai-forever/Real-ESRGAN/blob/main/RealESRGAN_x4.pth
the folder structure: ai_backend/imagesuperresolution/weights/RealESRGAN_x4plus.pth
___________________________________________________________________________
don´t forget to upload the base humans to github!
Download link: https://sketchfab.com/DNC44
base male and base female
________________________________________________________________________
-> rest coming soon.


Repo
🚀 2. Autoinstaller für dein Repo (für andere User)
Speichere diesen Inhalt als install_and_run.sh in deinem Projekt-Root (z. B. im GitHub-Repo):
#!/bin/bash

echo "🐍 Erstelle und aktiviere virtuelles Environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Installiere Python-Abhängigkeiten..."
pip install -r requirements.txt || {
  echo "⚠️ requirements.txt fehlt oder fehlerhaft – versuche manuelle Installation..."
  pip install PySide6==6.9.1 torch numpy==1.26.4 opencv-python Pillow trimesh requests
}

echo "🔧 Installiere Systembibliotheken (xcb, OpenGL, etc.)..."
sudo apt-get update && sudo apt-get install -y \
  libxcb1 libxcb-util1 libxcb-cursor0 libxcb-keysyms1 libxcb-xinerama0 \
  libxcb-randr0 libxcb-shape0 libxcb-icccm4 libxcb-image0 libxcb-xkb1 \
  libxkbcommon-x11-0 libx11-xcb1 libxrender1 libxi6 libxcomposite1 \
  libxcursor1 libxrandr2 libxtst6 libegl1 libgl1

echo "📁 Setze Qt-Plugin-Pfad..."
export QT_QPA_PLATFORM_PLUGIN_PATH=$(python -c "import PySide6, os; print(os.path.join(os.path.dirname(PySide6.__file__), 'Qt', 'plugins', 'platforms'))")

echo "🚀 Starte 3D_God..."
python /workspaces/3D_God.V2/main_launcher.py

✅ Verwendung:
chmod +x install_and_run.sh
./install_and_run.sh

#!/bin/bash

echo "🧪 [Local] Starte mit echtem Display..."

source .venv/bin/activate

# Optional: Qt Plugin Pfad nur setzen, falls nicht automatisch gefunden wird
export QT_QPA_PLATFORM_PLUGIN_PATH=$(python -c "import PySide6, os; print(os.path.join(os.path.dirname(PySide6.__file__), 'Qt', 'plugins', 'platforms'))")

# Starte ganz normal
python /workspaces/3D_God.V2/main_launcher.py

📂 Repo-Struktur-Vorschlag

3D_God.V2/
├── run_in_codespace.sh     ✅ Qt + xvfb
├── run_dev_local.sh        ✅ Lokal mit GUI
├── install_and_run.sh      ✅ Full-Autoinstaller
├── requirements.txt
├── main_launcher.py
└── ...

📝 README-Eintrag-Vorschlag
### 🖥️ Projekt starten

#### ✅ Lokale Entwicklung (mit Desktop-GUI)
bash
./run_dev_local.sh
____________________________________________________________

Codespace
✅ 1. Lokale Setup-Datei für deinen Codespace (manueller Start)
Speichere diesen Inhalt als start_3dgod_local.sh:
#!/bin/bash

echo "🔁 Aktivieren des Python venv..."
source .venv/bin/activate

echo "📦 Installiere alle benötigten nativen Qt/X11/GL-Bibliotheken..."
sudo apt-get update && sudo apt-get install -y \
  libxcb1 libxcb-util1 libxcb-cursor0 libxcb-keysyms1 libxcb-xinerama0 \
  libxcb-randr0 libxcb-shape0 libxcb-icccm4 libxcb-image0 libxcb-xkb1 \
  libxkbcommon-x11-0 libx11-xcb1 libxrender1 libxi6 libxcomposite1 \
  libxcursor1 libxrandr2 libxtst6 libegl1 libgl1

echo "📁 Setze Qt-Plugin-Pfad..."
export QT_QPA_PLATFORM_PLUGIN_PATH=$(python -c "import PySide6, os; print(os.path.join(os.path.dirname(PySide6.__file__), 'Qt', 'plugins', 'platforms'))")

echo "🐸 Starte 3D_God..."
python /workspaces/3D_God.V2/main_launcher.py

✅ Verwendung:
chmod +x start_3dgod_local.sh
./start_3dgod_local.sh

