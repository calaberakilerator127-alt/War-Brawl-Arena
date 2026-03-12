import pandas as pd
import json

def load_tablas():
    try:
        ataques = pd.read_excel("Tabla de Ataques.xlsx").to_dict(orient="records")
        danos = pd.read_excel("Tabla de Daños.xlsx").to_dict(orient="records")
        mecanicas = pd.read_excel("Tabla de Mecanicas.xlsx").to_dict(orient="records")
        personajes = pd.read_excel("Tabla de Personajes.xlsx").to_dict(orient="records")

        data = {
            "ataques": ataques,
            "danos": danos,
            "mecanicas": mecanicas,
            "personajes": personajes
        }
        with open("tablas.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Tablas exportadas a tablas.json exitosamente.")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    load_tablas()
