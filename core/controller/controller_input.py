import pygame
from threading import Thread
import time

class ControllerInput:
    def __init__(self, tab_switch_callback):
        self.tab_switch_callback = tab_switch_callback
        self.running = False
        self.current_tab = 0

    def start(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("[Controller] Kein Gamepad erkannt.")
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(f"[Controller] Verbunden: {self.joystick.get_name()}")
        self.running = True

        self.thread = Thread(target=self.listen_loop)
        self.thread.daemon = True
        self.thread.start()

    def listen_loop(self):
        while self.running:
            pygame.event.pump()
            # Beispiel: X-Button (0) → nächsten Tab
            if self.joystick.get_button(0):
                self.tab_switch_callback(1)
                time.sleep(0.3)
            elif self.joystick.get_button(1):
                self.tab_switch_callback(-1)
                time.sleep(0.3)
            time.sleep(0.05)

    def stop(self):
        self.running = False