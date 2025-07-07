# ai_backend/froggy/__init__.py

"""
🐸 Froggy Initialisierung
– Automatische Projekt-Analyse beim ersten Import
– Baut Gedächtnis-Datei 'froggy_project_cache.json'
"""

from . import froggy_repo_indexer

try:
    print("🧠 Froggy: Scanne Projektstruktur...")
    data = froggy_repo_indexer.scan_project(froggy_repo_indexer.PROJECT_ROOT)
    froggy_repo_indexer.save_cache(data)
    print("✅ Froggy: Projekt-Gedächtnis aktualisiert.")
except Exception as e:
    print(f"❌ Froggy: Fehler beim automatischen Projekt-Scan: {e}")