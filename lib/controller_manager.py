import pygame
import threading
import time
from core.logger import log

class ControllerManager:
    def __init__(self):
        log.info("[ControllerManager][__init__] ▶️ Initialisiere Pygame für Controller...")
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        self.running = False
        log.success("[ControllerManager][__init__] ✅ Pygame initialisiert")

    def is_connected(self):
        count = pygame.joystick.get_count()
        log.info(f"[ControllerManager][is_connected] ▶️ Verfügbare Controller: {count}")
        return count > 0

    def connect_to_window(self, main_window):
        log.info("[ControllerManager][connect_to_window] ▶️ Versuche Verbindung zum Controller...")
        if not self.is_connected():
            log.error("[ControllerManager][connect_to_window] ❌ Kein Controller erkannt.")
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.running = True
        log.success(f"[ControllerManager][connect_to_window] ✅ Controller verbunden: {self.joystick.get_name()}")

        # Starte Thread für Controller-Eingabe
        threading.Thread(target=self.poll_events, args=(main_window,), daemon=True).start()

    def poll_events(self, main_window):
        log.info("[ControllerManager][poll_events] ▶️ Starte Event-Loop für Controller...")
        while self.running:
            pygame.event.pump()

            try:
                if self.joystick.get_button(0):  # PS-Controller: X
                    log.info("[ControllerManager][poll_events] 🔘 Taste X gedrückt")
                    main_window.status_bar.showMessage("🎮 Taste X gedrückt → Sculpting öffnen")
                    main_window.tabs.setCurrentIndex(4)  # Tab 4 = Sculpting
            except Exception as e:
                log.error(f"[ControllerManager][poll_events] ❌ Fehler bei Button-Check: {e}")

            time.sleep(0.1)

    def stop(self):
        log.info("[ControllerManager][stop] ▶️ Stoppe ControllerManager...")
        self.running = False
        pygame.quit()
        log.success("[ControllerManager][stop] ✅ Pygame geschlossen")