import os
import json


class DataBase:
    def __init__(self,filename):
        self._caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), "../controllers/db", filename))    # Caminho do arquivo de database
        self._json = self._load_json()

    def _load_json(self):
        try:
            with open(self._caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError("Arquivo de database não encontrado")
        except json.JSONDecodeError:
            raise ValueError("Arquivo de database está corrompido") 

    def _save_to_json(self, data: list[dict]):
        with open(self._caminho, "w", encoding="utf-8") as f:
            return json.dump(data, f, indent=2, ensure_ascii=False)
