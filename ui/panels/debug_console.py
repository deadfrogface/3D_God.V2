from PySide6.QtWidgets import ( QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QCheckBox, QLineEdit, QFileDialog ) import sys import datetime import os import re

class DebugConsole(QWidget): def init(self): super().init() print("[DebugConsole][init] ▶️ Initialisiere Debug-Konsole...") self.setWindowTitle("🛠 Debug-Konsole") layout = QVBoxLayout()

# 🔎 Filter-Kategorien
    self.filters = {
        "Sculpt": QCheckBox("Sculpt"),
        "Export": QCheckBox("Export"),
        "Rig": QCheckBox("Rig"),
        "AI": QCheckBox("AI"),
        "All": QCheckBox("Alle anzeigen")
    }
    filter_row = QHBoxLayout()
    for cb in self.filters.values():
        cb.setChecked(False)
        cb.stateChanged.connect(self.apply_filter)
        filter_row.addWidget(cb)
    layout.addLayout(filter_row)

    # 🔍 Suchfeld
    self.search_box = QLineEdit()
    self.search_box.setPlaceholderText("🔍 Suche im Log...")
    self.search_box.textChanged.connect(self.apply_filter)
    layout.addWidget(self.search_box)

    # 📄 Textausgabe
    self.output = QTextEdit()
    self.output.setReadOnly(True)
    layout.addWidget(self.output)

    # 🔘 Buttons (Clear, Export, Diagnose)
    btn_row = QHBoxLayout()
    btn_clear = QPushButton("🧹 Leeren")
    btn_clear.clicked.connect(self.clear_console)
    btn_row.addWidget(btn_clear)

    btn_export = QPushButton("📁 Log exportieren")
    btn_export.clicked.connect(self.export_log)
    btn_row.addWidget(btn_export)

    layout.addLayout(btn_row)

    # 🔬 Diagnose-Button
    btn_diagnostics = QPushButton("🧠 Projekt-Diagnose starten")
    btn_diagnostics.clicked.connect(self.run_diagnostics)
    layout.addWidget(btn_diagnostics)

    self.setLayout(layout)
    self.full_log = []

    sys.stdout = self
    print("[DebugConsole][__init__] ✅ Debug-Konsole bereit.")

def write(self, message):
    msg = message.strip()
    if msg:
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        log_entry = f"{timestamp} {msg}"
        self.full_log.append(log_entry)
        self.apply_filter()

def flush(self):
    pass

def apply_filter(self):
    self.output.clear()
    search = self.search_box.text().lower()
    filtered_count = 0
    for line in self.full_log:
        if self._passes_filter(line) and search in line.lower():
            self.output.append(line)
            filtered_count += 1
    print(f"[DebugConsole][apply_filter] ✅ {filtered_count} Zeilen gefiltert")

def _passes_filter(self, msg):
    if self.filters["All"].isChecked():
        return True
    for key, cb in self.filters.items():
        if cb.isChecked() and key.lower() in msg.lower():
            return True
    return False

def clear_console(self):
    self.full_log.clear()
    self.output.clear()
    print("[DebugConsole][clear_console] ✅ Konsole geleert")

def export_log(self):
    path, _ = QFileDialog.getSaveFileName(self, "Speichere Log als", "debug_log.txt", "Textdateien (*.txt)")
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.full_log))
        print(f"[DebugConsole][export_log] ✅ Log exportiert nach: {path}")
    else:
        print("[DebugConsole][export_log] ❌ Kein Pfad gewählt")

def run_diagnostics(self):
    print("[DebugConsole][run_diagnostics] ▶️ Starte Projektprüfung...")
    base_dir = os.getcwd()
    problem_count = 0

    known_file_mistakes = {
        ".gitinore": ".gitignore",
        ".gitingore": ".gitignore",
        ".gitigonre": ".gitignore",
        "readme.txt": "README.md",
        "README": "README.md",
        "read.me": "README.md",
        "licence.txt": "LICENSE",
        "LICENSEE": "LICENSE",
        "lisense": "LICENSE"
    }

    required_dirs = ["core", "ui", "ui/panels", "ai_backend", "blender_embed"]

    found_panels = set()
    used_panels = set()
    main_window_path = os.path.join("ui", "gui_main_window.py")

    # 🔍 MainWindow analysieren (falls vorhanden)
    if os.path.exists(main_window_path):
        with open(main_window_path, "r", encoding="utf-8") as mw:
            content = mw.read()
            used_panels.update(re.findall(r"from ui\\.panels\\.([a-zA-Z0-9_]+) import", content))

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, base_dir)
            file_lower = file.lower()

            # 🟥 Leere Datei
            if os.path.getsize(path) == 0:
                print(f"[Diagnostic][Leere Datei] 🟥 {rel_path}")
                problem_count += 1

            # 🟧 Platzhalter-Inhalte
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if any(kw in content for kw in ["# Stub", "# TODO", "pass", "...", "return None"]):
                        print(f"[Diagnostic][Platzhalter] 🟧 {rel_path}")
                        problem_count += 1
                    # Importfehler-Erkennung
                    if re.search(r"from .* import", content):
                        for line in content.splitlines():
                            if "from" in line and "import" in line:
                                parts = line.split("import")[0].strip().split()
                                if parts and not parts[-1].replace(".", os.sep) in rel_path:
                                    print(f"[Diagnostic][ImportPfad] ⚠️ {rel_path} enthält evtl. ungültigen Import")
                                    break
            except Exception as e:
                print(f"[Diagnostic][Fehler beim Lesen] ❌ {rel_path} → {e}")
                problem_count += 1

            # 🟨 Falsche Dateinamen
            if file_lower in known_file_mistakes:
                correct = known_file_mistakes[file_lower]
                print(f"[Diagnostic][Falsch benannt] 🟨 {rel_path} → erwartet: {correct}")
                problem_count += 1

            # 🔄 Panel-Tracking
            if "/ui/panels/" in rel_path.replace("\\", "/") and file.endswith(".py"):
                found_panels.add(file.replace(".py", ""))

    # 🔍 Fehlende Verbindungen
    unconnected = found_panels - used_panels
    for panel in sorted(unconnected):
        print(f"[Diagnostic][Unverknüpft] 🔌 Panel nicht verbunden: {panel}")
        problem_count += 1

    # 🔧 Fehlen von Pflichtordnern
    for folder in required_dirs:
        if not os.path.exists(folder):
            print(f"[Diagnostic][Fehlender Ordner] 📁 {folder} fehlt!")
            problem_count += 1

    print(f"[DebugConsole][run_diagnostics] ✅ Projektprüfung abgeschlossen – {problem_count} Auffälligkeiten")

