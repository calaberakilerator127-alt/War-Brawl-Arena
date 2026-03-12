import json
import os
import random

def main():
    path = "assets/personajes/"
    if not os.path.exists(path):
        os.makedirs(path)
        
    with open("tablas.json", "r", encoding="utf-8") as f:
        tablas = json.load(f)
        
    personajes = tablas.get("personajes", [])
    
    for p in personajes:
        # Example:
        # "Personaje": "Leonardo",
        # "Tipo Magia": "Roca",
        # "Inmunidad Total": "Eléctrico",
        # "Inmunidad Parcial": "Fuego",
        # "Vida": 900, "Fuerza": 82, "Magia": 55, "Velocidad": 65, "Peso": 95, "Precisión": 76,
        # "Res. Fís": 0.35, "Res. Mag": 0.25, "Equilibrio": 78
        name = p["Personaje"]
        magia = p["Tipo Magia"].lower()
        if magia == "eléctrico": magia = "electrico"
        elif magia == "magnético": magia = "magnetico"
        elif magia == "psíquico": magia = "psiquico"
        elif magia == "ácido": magia = "acido"

        inm_total = p.get("Inmunidad Total", "").lower()
        inm_parcial = p.get("Inmunidad Parcial", "").lower()
        
        # normalize
        for k in ["inm_total", "inm_parcial"]:
            val = locals()[k]
            if val == "eléctrico": locals()[k] = "electrico"
            elif val == "magnético": locals()[k] = "magnetico"
            elif val == "psíquico": locals()[k] = "psiquico"
            elif val == "ácido": locals()[k] = "acido"
            
        char_data = {
            "nombre": name,
            "vida": p["Vida"],
            "stamina": 100,
            "fuerza_base": p["Fuerza"],
            "magia_base": p["Magia"],
            "equilibrio": p["Equilibrio"],
            "velocidad": p["Velocidad"],
            "resistencia_fisica": p["Res. Fís"],
            "resistencia_magica": p["Res. Mag"],
            "peso": p["Peso"],
            "precision": p["Precisión"],
            "tipo_magia": magia,
            "inmunidad": inm_total, # For backwards compatibility (now will be handled as inmunidad_total in game or we just use inmunidad and inmunidad_parcial)
            "inmunidad_total": inm_total,
            "inmunidad_parcial": inm_parcial,
            "prob_fallo": 0.1,
            "prob_retorno_magia": 0.1,
            "prob_fallo_esquivar": 0.15,
            "prob_fallo_proteger": 0.15,
            "prob_critico": 0.1,
            "descripcion": f"Luchador de elemento {magia}."
        }
        with open(os.path.join(path, f"{name.lower()}.json"), "w", encoding="utf-8") as f:
            json.dump(char_data, f, indent=4, ensure_ascii=False)
            
    print(f"Generated {len(personajes)} characters from tablas_xlsx.")

if __name__ == "__main__":
    main()
