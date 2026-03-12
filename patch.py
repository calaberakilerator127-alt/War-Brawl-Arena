import json
import re

with open("tablas.json", "r", encoding="utf-8") as f:
    tablas = json.load(f)

ataques = {}
for row in tablas["ataques"]:
    el = row["Elemento"].lower()
    if el == "eléctrico": el = "electrico"
    if el == "magnético": el = "magnetico"
    if el == "psíquico": el = "psiquico"
    if el == "ácido": el = "acido"
    
    ataques[el] = {}
    for k, v in row.items():
        if k == "Elemento": continue
        name = v.split(":")[0].strip().lower()
        if "Básico" in k: poder, stam = 1.0, 18
        elif "Estratégico" in k: poder, stam = 1.25, 24
        elif "Pesado" in k: poder, stam = 1.5, 30
        else: poder, stam = 2.0, 45 # Hype
        ataques[el][name] = {"stamina": stam, "resis_mag": 10, "base_dmg": 0, "poder": poder, "desc": v}

danos = {}
for row in tablas["danos"]:
    el = row["Ataque ↓ \ Defensa →"].lower()
    if el == "eléctrico": el = "electrico"
    if el == "magnético": el = "magnetico"
    if el == "psíquico": el = "psiquico"
    if el == "ácido": el = "acido"
    
    danos[el] = {}
    for k, v in row.items():
        if "Defensa" in k: continue
        k2 = k.lower()
        if k2 == "eléctrico": k2 = "electrico"
        if k2 == "magnético": k2 = "magnetico"
        if k2 == "psíquico": k2 = "psiquico"
        if k2 == "ácido": k2 = "acido"
        danos[el][k2] = float(v)

with open("assets/mecanicas/combate/combate_manager.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace ATAQUES_MAGICOS
ataques_str = "ATAQUES_MAGICOS = " + json.dumps(ataques, indent=8, ensure_ascii=False)
content = re.sub(r"ATAQUES_MAGICOS = \{.*?\n    \}", ataques_str, content, flags=re.DOTALL)

# Insert DANOS_MULTIPLIERS
danos_str = "DANOS_MULTIPLIERS = " + json.dumps(danos, indent=8, ensure_ascii=False)
if "DANOS_MULTIPLIERS =" not in content:
    content = content.replace("ATAQUES_MAGICOS =", danos_str + "\n\n    " + "ATAQUES_MAGICOS =")

with open("assets/mecanicas/combate/combate_manager.py", "w", encoding="utf-8") as f:
    f.write(content)

print("combate_manager.py patched with ATAQUES_MAGICOS and DANOS_MULTIPLIERS")
