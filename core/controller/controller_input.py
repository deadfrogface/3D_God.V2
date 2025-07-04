import pygame
from threading import Thread
import time

class ControllerInput:
    def __init__(self, tab_switch_callback):
        print(f"[ControllerInput][__init__] ▶️ Eingabe: tab_switch_callback={tab_switch_callback}")
        self.tab_switch_callback = tab_switch_callback
        self.running = False
        self.current_tab = 0
        print("[ControllerInput][__init__] ✅ Initialisiert")

    def start(self):
        print("[ControllerInput][start] ▶️ Starte Controller-Erkennung")
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("[ControllerInput][start] ❌ Kein Gamepad erkannt.")
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(f"[ControllerInput][start] ✅ Verbunden mit: {self.joystick.get_name()}")
        self.running = True

        self.thread = Thread(target=self.listen_loop)
        self.thread.daemon = True
        self.thread.start()
        print("[ControllerInput][start] ✅ Listener-Thread gestartet")

    def listen_loop(self):
        print("[ControllerInput][listen_loop] ▶️ Eingabe-Überwachung gestartet")
        while self.running:
            pygame.event.pump()

            if self.joystick.get_button(0):
                print("[ControllerInput][listen_loop] 🎮 Button 0 gedrückt – weiter")
                self.tab_switch_callback(1)
                time.sleep(0.3)
            elif self.joystick.get_button(1):
                print("[ControllerInput][listen_loop] 🎮 Button 1 gedrückt – zurück")
                self.tab_switch_callback(-1)
                time.sleep(0.3)

            time.sleep(0.05)

        print("[ControllerInput][listen_loop] ❎ Eingabe-Überwachung beendet")

    def stop(self):
        print("[ControllerInput][stop] ▶️ Stoppe ControllerInput")
        self.running = False
        print("[ControllerInput][stop] ✅ Gestoppt")