import pygame
from threading import Thread
import time
from core.logger import log  # ⬅ Logging-Modul importieren

class ControllerInput:
    def __init__(self, tab_switch_callback):
        log.info(f"[ControllerInput][__init__] Eingabe: tab_switch_callback={tab_switch_callback}")
        self.tab_switch_callback = tab_switch_callback
        self.running = False
        self.current_tab = 0
        log.success("[ControllerInput][__init__] ✅ Initialisiert")

    def start(self):
        log.info("[ControllerInput][start] Starte Controller-Erkennung")
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            log.warning("[ControllerInput][start] ❌ Kein Gamepad erkannt.")
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        log.success(f"[ControllerInput][start] ✅ Verbunden mit: {self.joystick.get_name()}")
        self.running = True

        self.thread = Thread(target=self.listen_loop)
        self.thread.daemon = True
        self.thread.start()
        log.success("[ControllerInput][start] ✅ Listener-Thread gestartet")

    def listen_loop(self):
        log.debug("[ControllerInput][listen_loop] ▶️ Eingabe-Überwachung gestartet")
        while self.running:
            pygame.event.pump()

            try:
                if self.joystick.get_button(0):
                    log.debug("[ControllerInput][listen_loop] 🎮 Button 0 gedrückt – weiter")
                    self.tab_switch_callback(1)
                    time.sleep(0.3)
                elif self.joystick.get_button(1):
                    log.debug("[ControllerInput][listen_loop] 🎮 Button 1 gedrückt – zurück")
                    self.tab_switch_callback(-1)
                    time.sleep(0.3)
            except Exception as e:
                log.error(f"[ControllerInput][listen_loop] ❌ Fehler bei Button-Check: {e}")

            time.sleep(0.05)

        log.info("[ControllerInput][listen_loop] ❎ Eingabe-Überwachung beendet")

    def stop(self):
        log.info("[ControllerInput][stop] ▶️ Stoppe ControllerInput")
        self.running = False
        log.success("[ControllerInput][stop] ✅ Gestoppt")