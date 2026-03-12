import os
import random
import sys
import importlib
import time
from assets.interfaz.login import LoginUI
from assets.interfaz.menu_principal import MainMenuUI
from assets.interfaz.seleccion_personajes import TeamSelectionUI
from assets.interfaz.tienda import ShopUI
from assets.interfaz.combate_ui import BattleUI
from assets.interfaz.win_loss_ui import WinLossUI
from assets.audio_manager import AudioManager
from assets.mecanicas.entidades import Account, Character
from assets.mecanicas.narrador import Narrador
from assets.utils import get_data_path, get_resource_path
import pygame

from assets.interfaz.loading_ui import LoadingUI
from assets.interfaz.pj_creation_ui import CharacterCreationUI
from assets.interfaz.settings_ui import SettingsUI

# Dynamic loading of mechanics as requested
def load_mechanic(module_path):
    # e.g. "assets.mecanicas.combate.combate_manager"
    return importlib.import_module(module_path)

class GameOrchestrator:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        # Requirement: Resizable and Fullscreen support
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.virtual_screen = pygame.Surface((800, 600))
        pygame.display.set_caption("War Brawl Arena")
        
        # Requirement: Set application icon
        icon_path = get_resource_path("assets/imagen/Icon.png")
        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
            
        self.clock = pygame.time.Clock()
        
        self.audio = AudioManager()
        self.narrador = Narrador()
        self.combate_mod = load_mechanic("assets.mecanicas.combate.combate_manager")
        self.progreso_mod = load_mechanic("assets.mecanicas.economia.progreso_manager")
        self.user1 = None
        self.user2 = None

    def run(self):
        self.show_splash_screen()
        LoadingUI.show(self.screen, self.clock)
        self.audio.play_music("menu")
        self.user1 = LoginUI.show(self.screen, self.clock)
        if not self.user1: return
        
        while True:
            self.audio.play_music("menu")
            choice = MainMenuUI.show_menu(self.screen, self.clock, self.user1, self.user2)
            
            if choice == "1": # PvP Local
                self.user2 = LoginUI.show(self.screen, self.clock, exclude_nickname=self.user1.nickname)
                if self.user2 and self.user2.nickname == self.user1.nickname and self.user1.nickname != "Invitado":
                    self.user2 = None
                    continue
                if self.user2:
                    self.start_pvp()
            
            elif choice == "10": # PvP Online Lobby
                from assets.interfaz.lobby_ui import LobbyUI
                token = LobbyUI.show(self.screen, self.clock, self.user1)
                if token:
                    # Simulamos entrada luego del matchmaking
                    if not self.user2: self.user2 = self.user1
                    self.start_pvp(is_online=True, token=token)
            
            elif choice == "2": # PvE
                self.start_pve()

            elif choice == "4": # Shop
                self.audio.play_music("tienda")
                ShopUI.show(self.screen, self.clock, self.user1, []) # Pass team if available
                self.audio.play_music("menu")
                self.user1.save()

            elif choice == "5": # Create Character
                self.create_character()

            elif choice == "7": # Settings (Ajustes)
                SettingsUI.show(self.screen, self.clock, self.audio)

            elif choice == "8": # Logout
                self.user1.save()
                self.user1 = LoginUI.show(self.screen, self.clock)
                if not self.user1: break

            elif choice == "9": # Exit
                self.user1.save()
                break

    def show_splash_screen(self):
        # Simplified splash since window is already open
        self.screen.fill((0, 0, 0))
        icon_path = get_resource_path("assets/imagen/Icon.png")
        if os.path.exists(icon_path):
            img = pygame.image.load(icon_path)
            img = pygame.transform.scale(img, (400, 400))
            self.screen.blit(img, (self.width//2 - 200, self.height//2 - 200))
            pygame.display.flip()
            time.sleep(1.5)

    def start_pvp(self, is_online=False, token=""):
        self.audio.play_music("seleccion")
        
        if is_online and token:
            random.seed(token)
            self.battle_ui_pvp_mode = "online"
        else:
            self.battle_ui_pvp_mode = True
        
        team1_res = TeamSelectionUI.select_team(self.screen, self.clock, self.user1.nickname, [], restrict_custom=is_online)
        if team1_res == (None, None) or not team1_res: return
        team1_name, team1 = team1_res
        
        team2_res = TeamSelectionUI.select_team(self.screen, self.clock, self.user2.nickname, [c.nombre for c in team1], restrict_custom=is_online)
        if team2_res == (None, None) or not team2_res: return
        team2_name, team2 = team2_res
        
        self.run_combat_loop(team1_name, team1, team2_name, team2, is_pvp=self.battle_ui_pvp_mode)

    def start_pve(self):
        self.audio.play_music("seleccion")
        from assets.mecanicas.combate.ai_manager import AIManager
        
        team1_res = TeamSelectionUI.select_team(self.screen, self.clock, self.user1.nickname, [])
        if team1_res == (None, None) or not team1_res: return
        team1_name, team1 = team1_res
        
        team2_name, team2 = AIManager.select_random_team(excluded_chars=[c.nombre for c in team1])
        
        self.run_combat_loop(team1_name, team1, team2_name, team2, is_pvp=False)

    def run_combat_loop(self, team1_name, team1, team2_name, team2, is_pvp=True):
        manager = self.combate_mod.CombateManager(team1, team2, self.narrador)
        manager.audio = self.audio
        self.battle_ui = BattleUI(self.screen, self.clock, team1_name, team2_name, is_pvp)
        self.battle_ui.intro_text = "¡PREPARATE PARA PELEAR!"
        self.battle_ui.intro_timer = self.battle_ui.intro_duration
        self.battle_ui.intro_icon = self.battle_ui.get_char_icon(manager.active1.nombre)
        
        if manager.hazard_zone:
            self.battle_ui.add_log(f"ZONA DE RIESGO: {manager.hazard_zone.upper()}! ¡Magia {manager.hazard_zone} potenciada!")
            self.narrador.narrar(f"¡Cuidado! Estamos en una zona de magma." if manager.hazard_zone == "fuego" else "¡El escenario está modificado!")
            
        current_turn = 1
        self.audio.play_music("combate")
        self.battle_ui.add_log(f"¡{team1_name} vs {team2_name}!")
        self.narrador.narrar(f"¡Prepárense! El equipo {team1_name} se enfrenta a {team2_name}!")
        
        last_active1 = None
        last_active2 = None
        
        # Initial Selection
        manager.active1 = self.battle_ui.select_fighter(team1, self.user1.nickname)
        if not manager.active1: return
        
        if is_pvp:
            manager.active2 = self.battle_ui.select_fighter(team2, self.user2.nickname if self.user2 else "Jugador 2")
            if not manager.active2: return
        else:
            vivos2 = [c for c in team2 if c.vida > 0]
            manager.active2 = random.choice(vivos2) if vivos2 else team2[0]

        match_aborted = False
        while any(c.vida > 0 for c in team1) and any(c.vida > 0 for c in team2) and not match_aborted:
            # Track stats for THIS round (until one falls)
            ronda_stats1 = {"ganada": False, "ko": False, "perfecta": False, "criticos_realizados": 0}
            ronda_stats2 = {"ganada": False, "ko": False, "perfecta": False, "criticos_realizados": 0}
            
            p1_start_hp = manager.active1.vida
            p2_start_hp = manager.active2.vida

            while manager.active1.vida > 0 and manager.active2.vida > 0:
                # Handle intros sequentially if they are new
                if manager.active1.nombre != last_active1:
                    self.narrador.narrar(f"¡Entrando al ring, {manager.active1.nombre}!")
                    dur = self.audio.play_character_entry(manager.active1.nombre)
                    self.battle_ui.start_intro(manager.active1.nombre, team1_name, dur)
                    last_active1 = manager.active1.nombre
                    # Wait/Draw for intro 1
                    while self.battle_ui.intro_timer > 0:
                        pygame.event.pump()
                        self.audio.update() # Resume battle music after entry song
                        self.battle_ui.draw_ui(manager.active1, manager.active2)
                        pygame.display.flip()
                        self.clock.tick(60)
                
                if manager.active2.nombre != last_active2:
                    self.narrador.narrar(f"¡Y su oponente, {manager.active2.nombre}!")
                    dur = self.audio.play_character_entry(manager.active2.nombre)
                    self.battle_ui.start_intro(manager.active2.nombre, team2_name, dur)
                    last_active2 = manager.active2.nombre
                    # Wait/Draw for intro 2
                    while self.battle_ui.intro_timer > 0:
                        self.battle_ui.draw_ui(manager.active1, manager.active2)
                        pygame.display.flip()
                        self.clock.tick(60)
                
                # ... rest of the turn ... (we need to pass stats to play_turn or handle them here)
                res = self.play_turn(manager, team1, team2, is_pvp, ronda_stats1, ronda_stats2)
                if res == "quit" or (isinstance(res, tuple) and res[0] == "quit"):
                    if isinstance(res, tuple) and res[1] == "save":
                        from assets.utils_persistence import save_game
                        import time
                        state = {
                            "team1": [c.nombre for c in team1],
                            "team2": [c.nombre for c in team2],
                            "active1_hp": manager.active1.vida,
                            "active2_hp": manager.active2.vida
                        }
                        save_name = f"Partida_{self.user1.nickname}_{int(time.time())}"
                        save_game(save_name, state)
                        self.battle_ui.add_log(f"¡Partida guardada: {save_name}!")
                        self.narrador.narrar("Partida Guardada.")
                        time.sleep(2)
                    match_aborted = True
                    break
                
                # Check if active characters fell during the turn
                if manager.active1.vida <= 0:
                    msg = f"¡{manager.active1.nombre} ha caído!"
                    self.battle_ui.add_log(msg)
                    self.narrador.narrar(msg)
                    vivos = [c for c in team1 if c.vida > 0]
                    if vivos:
                        manager.active1 = self.battle_ui.select_fighter(team1, self.user1.nickname)
                        self.battle_ui.add_log(f"¡Entra {manager.active1.nombre}!")
                        # Inter-round Shop/Wildcard Phase
                        from assets.interfaz.tienda import ShopUI
                        ShopUI.show(self.screen, self.clock, self.user1, team1)
                
                if manager.active2.vida <= 0:
                    msg = f"¡{manager.active2.nombre} ha caído!"
                    self.battle_ui.add_log(msg)
                    self.narrador.narrar(msg)
                    vivos = [c for c in team2 if c.vida > 0]
                    if vivos:
                        if is_pvp:
                            manager.active2 = self.battle_ui.select_fighter(team2, self.user2.nickname)
                            # Inter-round Shop
                            from assets.interfaz.tienda import ShopUI
                            ShopUI.show(self.screen, self.clock, self.user2, team2)
                        else:
                            manager.active2 = vivos[0] # AI just takes next
                        self.battle_ui.add_log(f"¡Entra {manager.active2.nombre}!")
            
            # Round ended (one died or swapped? swapping doesn't end round normally)
            if manager.active1.vida <= 0:
                ronda_stats2["ganada"] = True
                if manager.active1.ko: ronda_stats2["ko"] = True
                if manager.active2.vida == p2_start_hp: ronda_stats2["perfecta"] = True
                
                pts, xp = self.progreso_mod.ProgresoManager.calcular_progreso_ronda(ronda_stats2)
                if self.user2 and self.user2.nickname != "Invitado": self.user2.pts += pts; self.user2.xp += xp
            elif manager.active2.vida <= 0:
                ronda_stats1["ganada"] = True
                if manager.active2.ko: ronda_stats1["ko"] = True
                if manager.active1.vida == p1_start_hp: ronda_stats1["perfecta"] = True
                
                pts, xp = self.progreso_mod.ProgresoManager.calcular_progreso_ronda(ronda_stats1)
                self.user1.pts += pts; self.user1.xp += xp
                    
        # Outcome
        if match_aborted:
            self.battle_ui.add_log("¡Combate cancelado!")
        elif any(c.vida > 0 for c in team1):
            # Team 1 Wins (Player)
            self.audio.play_music("ganar")
            self.narrador.narrar(f"¡Victoria para {team1_name}!")
            self.progreso_mod.ProgresoManager.aplicar_victoria_final(self.user1, True)
            self.user1.xp = max(0, self.user1.xp - manager.misses1)
            # Show Victory Screen
            WinLossUI.show(self.screen, self.clock, "victory", team1_name, f"+PTS: {self.user1.level * 50}")
        else:
            # Team 2 Wins (Player 2 or AI)
            if is_pvp:
                self.audio.play_music("ganar")
                self.narrador.narrar(f"¡Victoria para {team2_name}!")
                if self.user2 and self.user2.nickname != "Invitado":
                    self.progreso_mod.ProgresoManager.aplicar_victoria_final(self.user2, True)
                    self.user2.xp = max(0, self.user2.xp - manager.misses2)
                # Show Victory Screen for P2
                WinLossUI.show(self.screen, self.clock, "victory", team2_name)
            else:
                # PvE Loss (Defeat)
                self.audio.play_music("perder")
                self.narrador.narrar("Has sido derrotado por la inteligencia artificial.")
                WinLossUI.show(self.screen, self.clock, "defeat", team2_name, "MEJORA TUS PERSONAJES EN LA TIENDA")

        self.user1.save()
        if is_pvp and self.user2 and self.user2.nickname != "Invitado": self.user2.save()
        time.sleep(2)
        self.audio.play_music("menu")

    def play_turn(self, manager, team1, team2, is_pvp, stats1, stats2):
        manager.active1.reset_turn()
        manager.active2.reset_turn()
        
        # Action for player 1
        vivos1 = [c for c in team1 if c.vida > 0 and c != manager.active1]
        res1 = self.battle_ui.get_action_gui(manager.active1, manager.active2, manager, vivos1, current_player_name=self.user1.nickname)
        if not res1: return # Window closed
        action1, detail1 = res1
        
        # Action for opponent
        if is_pvp:
            vivos2 = [c for c in team2 if c.vida > 0 and c != manager.active2]
            res2 = self.battle_ui.get_action_gui(manager.active2, manager.active1, manager, vivos2, current_player_name=self.user2.nickname)
            if not res2: return
            action2, detail2 = res2
        else:
            from assets.mecanicas.combate.ai_manager import AIManager
            action2 = AIManager.decide_action(manager.active2, manager.active1, manager)
            detail2 = None
            if action2 == "1": detail2 = list(manager.ATAQUES_FISICOS.keys())[0]
            elif action2 == "2": 
                ta = list(manager.ATAQUES_MAGICOS.get(manager.active2.tipo_magia, {}).keys())
                detail2 = ta[0] if ta else None

        if action1 == "quit":
            return ("quit", detail1)
        if action2 == "quit":
            return ("quit", detail2)
        
        # Order players by speed
        players = [
            (self.user1, manager.active1, action1, detail1, manager.active2, 1, stats1), 
            (self.user2 if is_pvp else None, manager.active2, action2, detail2, manager.active1, 2, stats2)
        ]
        players.sort(key=lambda p: p[1].velocidad, reverse=True)
        
        # Clash Mechanic Check (Both attack physically, speed diff < 5)
        clash_winner = None
        if action1 == "1" and action2 == "1" and abs(manager.active1.velocidad - manager.active2.velocidad) < 5.0:
            self.battle_ui.add_log("¡Ambos cargan al mismo tiempo! ¡Es un CHOQUE!")
            self.narrador.narrar("¡Un choque increíble de poderes!")
            self.battle_ui.draw_ui(manager.active1, manager.active2, manager)
            pygame.display.flip()
            time.sleep(1)
            
            # Autoresolve by Equilibrio & RNG
            eq1 = manager.active1.equilibrio * random.uniform(0.8, 1.2)
            eq2 = manager.active2.equilibrio * random.uniform(0.8, 1.2)
            if eq1 >= eq2:
                clash_winner = 1
                manager.hype1 = min(100.0, manager.hype1 + 20)
                self.battle_ui.add_log(f"¡{manager.active1.nombre} gana el choque! +20% Hype")
            else:
                clash_winner = 2
                manager.hype2 = min(100.0, manager.hype2 + 20)
                self.battle_ui.add_log(f"¡{manager.active2.nombre} gana el choque! +20% Hype")
            time.sleep(1)
        # Important: Pass comodines to manager
        manager.user_comodines = self.user1.comodines
        manager.audio = self.audio
        
        # Decrement Hype fatigue at start of turn resolving
        if manager.fatigue1 > 0: manager.fatigue1 -= 1
        if manager.fatigue2 > 0: manager.fatigue2 -= 1
        
        for user, char, action, detail, target, p_num, s_dict in players:
            if char.vida <= 0: continue
            
            # Desperation State Trigger
            if (char.vida / char.vida_max) <= 0.15 and not getattr(char, "desperation_active", False):
                char.desperation_active = True
                char.velocidad += 10
                char.fuerza_base *= 1.3
                char.magia_base *= 1.3
                self.battle_ui.add_log(f"¡ESTADO DE DESESPERACIÓN! El aura de {char.nombre} estalla.")
                self.narrador.narrar(f"¡{char.nombre} ha despertado su poder oculto!")
            
            if action == "1" and clash_winner is not None and clash_winner != p_num:
                self.battle_ui.add_log(f"¡{char.nombre} perdió el choque y fue empujado hacia atrás!")
                continue # Skip turn for loser
            
            if action == "1": # ATAQUE FISICO
                p_name = detail
                if p_num == 2 and not is_pvp:
                    from assets.mecanicas.combate.ai_manager import AIManager
                    p_name = AIManager.pick_physical_attack(manager.ATAQUES_FISICOS, char)
                
                if p_name:
                    dmg, msg, is_crit = manager.calcular_ataque_fisico(char, target, p_name)
                    if is_crit: s_dict["criticos_realizados"] += 1
                    self.battle_ui.add_log(msg)
                    self.narrador.narrar(msg)
            
            elif action == "2": # ATAQUE MAGICO
                m_name = detail
                ta = list(manager.ATAQUES_MAGICOS.get(char.tipo_magia, {}).keys())
                
                if p_num == 2 and not is_pvp:
                     from assets.mecanicas.combate.ai_manager import AIManager
                     m_name = AIManager.pick_magic_attack(manager.ATAQUES_MAGICOS.get(char.tipo_magia, {}), char)
                
                if m_name:
                    # Check Hype Finisher
                    if len(ta) > 3 and m_name == ta[3]:
                        # Hype Finisher Consumption
                        if p_num == 1:
                            manager.hype1 = 0
                            manager.fatigue1 = 2
                        else:
                            manager.hype2 = 0
                            manager.fatigue2 = 2
                        self.battle_ui.add_log(f"¡{char.nombre} ha liberado su Hype Finisher!")
                        self.narrador.narrar("¡Poder máximo liberado!")
                        
                    dmg, msg, is_crit = manager.calcular_ataque_magico(char, target, m_name)
                    if is_crit: s_dict["criticos_realizados"] += 1
                    self.battle_ui.add_log(msg)
                    self.narrador.narrar(msg)
                    
            elif action == "8": # HYPE CANCEL
                p_name = detail
                if p_name:
                    # Cost 50% hype
                    if p_num == 1: manager.hype1 -= 50
                    else: manager.hype2 -= 50
                    
                    self.battle_ui.add_log(f"¡HYPE CANCEL! {char.nombre} ataca y adopta posición defensiva instantáneamente.")
                    
                    # Attack
                    dmg, msg, is_crit = manager.calcular_ataque_fisico(char, target, p_name)
                    if is_crit: s_dict["criticos_realizados"] += 1
                    self.battle_ui.add_log(msg)
                    
                    # Bonus Defense
                    res, def_msg = manager.protegerse(char)
                    self.battle_ui.add_log(def_msg)
                    self.narrador.narrar("¡Técnica de cancelación perfecta!")
                    
            elif action == "3": # PROTEGERSE
                res, msg = manager.protegerse(char)
                self.battle_ui.add_log(msg)
                self.narrador.narrar(msg)
                
            elif action == "4": # ESQUIVAR
                success, msg = manager.esquivar(char)
                if success:
                    char.is_dodging = True
                self.battle_ui.add_log(msg)
            
            elif action == "5": # COMODINES
                msg = manager.aplicar_comodin(detail, char, user)
                self.battle_ui.add_log(msg)
                self.narrador.narrar(msg)
            
            # Update playlists
            self.audio.update()
            
            if action == "6": # CAMBIAR
                new_char = detail
                if p_num == 1: manager.active1 = new_char
                else: manager.active2 = new_char
                msg = f"¡{char.nombre} sale, entra {new_char.nombre}!"
                self.battle_ui.add_log(msg)
                self.narrador.narrar(msg)

            time.sleep(0.5)

    def create_character(self):
        self.audio.play_music("tienda")
        CharacterCreationUI.show(self.screen, self.clock, self.user1, self.user2)
        self.audio.play_music("menu")


if __name__ == "__main__":
    try:
        game = GameOrchestrator()
        game.run()
    except Exception as e:
        import traceback
        from assets.logger import log_error
        
        # The new logger handles timestamps, formatting, and flushing automatically.
        error_message = f"CRITICAL ERROR: {str(e)}\n{traceback.format_exc()}"
        log_error(error_message)
        log_error("-" * 80)
        
        print("Game crashed. Details saved in error_log.txt")
        pygame.quit()
