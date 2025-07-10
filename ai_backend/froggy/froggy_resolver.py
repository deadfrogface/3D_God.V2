# froggy_resolver.py
import os
import json
import ast
import importlib.util
from difflib import get_close_matches

# Pfade
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
CACHE_PATH = os.path.join(os.path.dirname(__file__), "froggy_project_cache.json")
ALIASES_PATH = os.path.join(os.path.dirname(__file__), "froggy_aliases.json")

# Lade Cache (Projektstruktur)
def load_project_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Lade Aliases
def load_aliases():
    if os.path.exists(ALIASES_PATH):
        with open(ALIASES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Semantisches Matching
def find_best_match(query, project_cache, aliases):
    candidates = []
    query_lower = query.lower().strip()

    # Zuerst: Harte Aliases checken
    for alias, info in aliases.items():
        if query_lower == alias.lower():
            return info

    # Dann: Ähnlichkeitssuche in Alias-Namen
    close = get_close_matches(query_lower, aliases.keys(), n=1, cutoff=0.7)
    if close:
        return aliases[close[0]]

    # Fallback: Volltextsuche in Funktionen + Docstrings
    for file, data in project_cache.items():
        for func in data.get("functions", []):
            score = 0
            name = func.lower()
            if query_lower in name:
                score += 2
            if any(k in name for k in query_lower.split()):
                score += 1
            if score > 0:
                candidates.append((score, file, func))

    if candidates:
        best = sorted(candidates, key=lambda x: -x[0])[0]
        return {"file": best[1], "function": best[2]}

    return None

# Dynamischer Import
def dynamic_import_function(file_path, func_name):
    abs_path = os.path.join(PROJECT_ROOT, file_path)
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, func_name)

# Hauptfunktion: resolve("Güther's sauce") → echte Funktion
def resolve(query: str):
    cache = load_project_cache()
    aliases = load_aliases()
    match = find_best_match(query, cache, aliases)

    if not match:
        raise ImportError(f"❌ Keine passende Funktion gefunden für: {query}")

    return dynamic_import_function(match["file"], match["function"])
