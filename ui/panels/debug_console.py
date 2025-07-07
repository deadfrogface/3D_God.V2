from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QHBoxLayout, QCheckBox, QLineEdit, QFileDialog, QMessageBox
)
import sys
import os
from core.logger import log


class DebugConsole(QWidget):
    def __init__(self):
        try:
            super().__init__()
            log.info("[DebugConsole][__init__] ▶️ Initialisiere Debug-Konsole...")
            self.setWindowTitle("🛠 Debug-Konsole")
            layout = QVBoxLayout()

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

            self.search_box = QLineEdit()
            self.search_box.setPlaceholderText("🔍 Suche im Log...")
            self.search_box.textChanged.connect(self.apply_filter)
            layout.addWidget(self.search_box)

            self.output = QTextEdit()
            self.output.setReadOnly(True)
            layout.addWidget(self.output)

            btn_row = QHBoxLayout()
            btn_clear = QPushButton("🧹 Leeren")
            btn_clear.clicked.connect(self.clear_console)
            btn_row.addWidget(btn_clear)

            btn_export = QPushButton("📁 Log exportieren")
            btn_export.clicked.connect(self.export_log)
            btn_row.addWidget(btn_export)
            layout.addLayout(btn_row)

            btn_froggy = QPushButton("🐸 Froggy helfen lassen")
            btn_froggy.clicked.connect(self.ask_froggy)
            layout.addWidget(btn_froggy)

            # 🔤 Froggy Chatfeld (Copilot-Style)
            self.chat_input = QLineEdit()
            self.chat_input.setPlaceholderText("💬 Frag Froggy etwas... (z. B. 'Warum exportiert das nicht?')")
            self.chat_input.returnPressed.connect(self.ask_froggy_chat)
            layout.addWidget(self.chat_input)

            self.setLayout(layout)
            self.full_log = []

            sys.stdout = self
            sys.stderr = self
            log.info("[DebugConsole][__init__] ✅ Debug-Konsole bereit.")
        except Exception as e:
            log.error(f"[DebugConsole][__init__] ❌ Fehler bei Initialisierung: {e}")
            raise

    def apply_filter(self):
        self.output.clear()
        search = self.search_box.text().lower()
        count = 0
        for line in self.full_log:
            if self._passes_filter(line) and search in line.lower():
                self.output.append(line)
                count += 1
        log.debug(f"[DebugConsole][apply_filter] ✅ {count} Zeilen angezeigt")

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
        log.info("[DebugConsole][clear_console] ✅ Konsole geleert")

    def export_log(self):
        path, _ = QFileDialog.getSaveFileName(self, "Speichere Log als", "debug_log.txt", "Textdateien (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.full_log))
            log.info(f"[DebugConsole][export_log] ✅ Log gespeichert: {path}")
        else:
            log.warning("[DebugConsole][export_log] ❌ Kein Pfad gewählt")

    def run_diagnostics(self):
        self.ask_froggy()

    def ask_froggy(self):
        try:
            from ai_backend.froggy.froggy_handler import ask_froggy_anything
            log.info("[DebugConsole][ask_froggy] ▶️ Froggy wird gefragt...")
            log_text = "\n".join(self.full_log)

            result = ask_froggy_anything(log_text=log_text)

            self.output.append("\n🐸 Froggy sagt:\n")
            self.output.append(f"❌ Problem: {result.get('problem')}")
            self.output.append(f"📎 Ursache: {result.get('cause')}")
            self.output.append(f"💡 Vorschlag: {result.get('suggestion')}")

            if result.get("can_fix"):
                fix = QMessageBox.question(self, "Froggy kann es reparieren!",
                    "Froggy hat eine automatische Reparaturmöglichkeit gefunden. Jetzt ausführen?",
                    QMessageBox.Yes | QMessageBox.No)
                if fix == QMessageBox.Yes:
                    fix_result = result.get("fix_fn", lambda: "Kein Fix definiert")()
                    log.success(f"[Froggy] 🛠 Reparatur durchgeführt: {fix_result}")
                    self.output.append(f"\n🛠 Reparatur durchgeführt:\n{fix_result}")
        except Exception as e:
            log.error(f"[DebugConsole][ask_froggy] ❌ Fehler bei Froggy-Analyse: {e}")

    def ask_froggy_chat(self):
        from ai_backend.froggy import froggy_nlp
        msg = self.chat_input.text().strip()
        if not msg:
            return
        self.output.append(f"\n🗣 Du: {msg}")
        self.chat_input.clear()

        try:
            log_text = "\n".join(self.full_log)
            response = froggy_nlp.process_natural_input(msg, log_text)
            self.output.append(f"\n🐸 Froggy antwortet:\n{response}")
        except Exception as e:
            log.error(f"[DebugConsole][ask_froggy_chat] ❌ Fehler im Froggy NLP: {e}")
            self.output.append("\n❌ Froggy versteht das leider gerade nicht.")
