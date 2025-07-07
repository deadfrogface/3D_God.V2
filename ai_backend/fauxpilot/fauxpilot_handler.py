import requests

def generate_code(prompt: str, server_url: str = "http://localhost:5000/completion") -> str | None:
    """
    Sendet ein Prompt an den lokalen FauxPilot-Server und gibt den generierten Code zurück.

    :param prompt: Eingabetext (z. B. "Erzeuge Shader-Material für Gold in Blender")
    :param server_url: URL des laufenden FauxPilot-Servers
    :return: Code als Text oder None bei Fehler
    """
    try:
        response = requests.post(server_url, json={"prompt": prompt})
        response.raise_for_status()

        data = response.json()
        return data.get("completion", "").strip()

    except requests.exceptions.RequestException as e:
        print("❌ Verbindung zu FauxPilot fehlgeschlagen:", e)
        return None
    except ValueError:
        print("❌ Antwort war kein gültiges JSON.")
        return None
