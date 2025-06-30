import pygame
import threading
import time

class ControllerManager:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        self.running = False

    def is_connected(self):
        return pygame.joystick.get_count() > 0

    def connect_to_window(self, main_window):
        if not self.is_connected():
            print("❌ Kein Controller erkannt.")
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.running = True
        print(f"🎮 Controller erkannt: {self.joystick.get_name()}")

        # Starte Thread für Controller-Eingabe
        threading.Thread(target=self.poll_events, args=(main_window,), daemon=True).start()

    def poll_events(self, main_window):
        while self.running:
            pygame.event.pump()

            # Beispiel: Taste X gedrückt?
            if self.joystick.get_button(0):  # PS-Controller: X
                print("🔘 Taste X gedrückt")
                main_window.status_bar.showMessage("🎮 Taste X gedrückt → Sculpting öffnen")
                main_window.tabs.setCurrentIndex(4)  # Tab 4 = Sculpting

            time.sleep(0.1)

    def stop(self):
        self.running = False
        pygame.quit()