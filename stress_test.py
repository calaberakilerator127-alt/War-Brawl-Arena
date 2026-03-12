import os
import sys
import pygame
import random
import time
from assets.mecanicas.entidades import Character, Account
from assets.mecanicas.combate.combate_manager import CombateManager
from assets.mecanicas.economia.progreso_manager import ProgresoManager

def run_stress_test():
    print("Iniciando Pruebas de Estrés Automáticas...")
    pygame.init()
    
    # 1. Test Entity Loading
    print("- Verificando carga de personajes...")
    try:
        from assets.utils import get_resource_path
        import glob
        files = glob.glob("assets/personajes/*.json")
        for f in files:
            c = Character.load_from_json(f)
            assert c.nombre, f"Personaje {f} sin nombre"
        print(f"  [OK] {len(files)} personajes validados.")
    except Exception as e:
        print(f"  [ERROR] Carga de personajes: {e}")

    # 2. Simulate Intensive Combat Calculations
    print("- Simulando 1000 cálculos de combate rápidos...")
    try:
        c1 = Character("T1", "fuego", 1000, 100, 50, 50, 30, 0.3, 0.3, 80)
        c2 = Character("T2", "agua", 1000, 100, 50, 50, 30, 0.3, 0.3, 80)
        manager = CombateManager(c1, c2)
        
        for _ in range(1000):
            action = random.choice(["ataque_fisico", "ataque_magico", "esquivar", "protegerse"])
            if action == "ataque_fisico":
                manager.calcular_ataque_fisico(c1, c2)
            elif action == "ataque_magico":
                manager.calcular_ataque_magico(c1, c2)
            elif action == "esquivar":
                manager.esquivar(c1)
            elif action == "protegerse":
                manager.protegerse(c1)
        print("  [OK] Combate simulado correctamente.")
    except Exception as e:
        print(f"  [ERROR] Simulación de combate: {e}")

    # 3. Test Progress / Economy Integrity
    print("- Verificando integridad de economía...")
    try:
        acc = Account("Tester", "pass", pts=100)
        char = Character("C", "aire", 500, 50, 30, 30, 30, 0.2, 0.2, 50)
        
        ProgresoManager.generar_mejora_aleatoria(char)
        ProgresoManager.calcular_monedas_ganadas(True, 1)
        print("  [OK] Lógica de progreso verificada.")
    except Exception as e:
        print(f"  [ERROR] Economía: {e}")

    # 4. Test UI Components Initialization (No display)
    print("- Verificando inicialización de componentes UI...")
    try:
        from assets.interfaz.gui_components import Button, Panel, InputBox
        font = pygame.font.SysFont("Arial", 12)
        Button(0, 0, 100, 50, "Test", font)
        InputBox(0, 0, 100, 50, "Test", font)
        Panel(0, 0, 100, 50, "Test", font)
        print("  [OK] Componentes UI inicializados.")
    except Exception as e:
        print(f"  [ERROR] UI: {e}")

    print("\nResumen: Estrés de lógica completado.")
    pygame.quit()

if __name__ == "__main__":
    run_stress_test()
