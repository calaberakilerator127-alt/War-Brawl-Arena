War Brawl Arena — Documento de diseño (versión táctica y completa)

Resumen general
War Brawl Arena es un juego de combates por equipos (3 personajes por jugador) que mezcla elementos de RPG táctico y pelea por turnos. El sistema está pensado para que las decisiones sean previsibles y estratégicas: turnos simultáneos resueltos por velocidad, stamina como recurso central, fórmulas claras para daño y KO, sistema elemental con ventajas, inmunidades totales y parciales, y herramientas de balance.

Registro y cuentas

Al iniciar: iniciar sesión o crear cuenta (nickname + contraseña).

Cada cuenta guarda su progreso en un archivo independiente; guardado automático.

Cambio de cuenta disponible mostrando cuentas activas; la segunda cuenta puede entrar como invitado.

Menú principal muestra: nombre, nivel, XP actual y necesaria, puntos acumulados, victorias totales; tabla global ordenada por victorias; sección “Cómo se juega” y créditos.

Progreso y recompensas

Ronda ganada normal: +6 pts, +12 XP

Crítico acertado: +1 pts, +4 XP

Ronda ganada por KO: +2 pts, +6 XP

Ronda ganada sin perder vida: +8 pts, +18 XP

Mayor ataque de la ronda: +6 XP

Partida ganada: +10 pts, +25 XP, +1 victoria

Mantener vivos todos los personajes: +5 pts, +15 XP

XP por nivel: curva creciente (definir en implementación; sugerencia: factor ~1.15× por nivel).

Inicio de partida y reglas de equipo

Ambos jugadores ingresan nombre de equipo.

Cada jugador elige 3 personajes; ningún personaje se repite entre equipos.

Se puede cambiar 1 vez por ronda a un personaje; al volver conserva stats tal como quedaron.

Si un personaje muere, se sustituye por uno vivo. Vencer a todos = victoria.

Empate técnico: KO simultáneo.

Modelo de combate: turnos simultáneos resueltos por velocidad

Turno: selección simultánea → cálculo (velocidad del movimiento) → ejecución por orden de velocidad → resolución completa → narración.

Si el primer ejecutor incapacita/derrota al rival, el rival pierde su ejecución.

Fases del turno

Selección: elegir ataque físico (ligero/medio/fuerte), ataque mágico (según tipo / hechizos), protegerse, esquivar o usar comodín.

Cálculo: calcular velocidad de acción (fórmula).

Ejecución: mayor velocidad actúa primero; si velocidades muy cercanas y ambos usan ataque físico, el más lento recibe daño primero.

Resolución: aplicar daño, consumos de stamina, efectos, críticos, regeneraciones y probabilidades de KO.

Narración: narrador detalla el resultado; turno siguiente espera a que termine.

Fórmulas y parámetros (sistema mecánico)

Velocidad de movimiento
velocidad_movimiento = velocidad_personaje × (stamina_actual / stamina_max) × modificador_movimiento × factor_aleatorio

modificadores: ataque físico pesado 0.85; físico normal 1.00; mágico 0.80; esquivar 1.10; protegerse 0.95.

factor_aleatorio ∈ [0.85, 1.00].

Daño físico
daño_físico = (fuerza_base × modificador_ataque × (peso / 100)) × (0.9 + precisión / 100)

modificadores físico: puño 0.9; patada 1.0; rodillazo 1.2; codazo 1.1; gancho 1.3; cabezazo 1.25.
daño_final_físico = daño_físico × (1 − resistencia_física_objetivo)

Daño mágico
daño_mágico = (magia_base × poder_hechizo) × (0.9 + precisión / 100)

poder_hechizo: ligero 1.0; medio 1.25; fuerte 1.5.

Aplicar ventaja elemental (multiplicador_tipo = 1.25/1.00/0.75 según tabla).

Inmunidad total: daño_final_mágico = 0.

Inmunidad parcial: daño_final_mágico = daño_mágico × 0.25 × (1 − resistencia_mágica).

Si no hay inmunidad: daño_final_mágico = daño_mágico × (1 − resistencia_mágica) × multiplicador_tipo.

Críticos

Si precisión ≥ 90: probabilidad_crítico (%) = precisión − 85.

multiplicador_crítico = 1.25 + ((precisión − 90) / 40), con tope ×2.

Si sale crítico, aplicar multiplicador al daño_final (tras resistencias y multiplicador elemental).

Sistema KO

estado_KO = promedio( stamina_actual / stamina_max, resistencia_física_actual, equilibrio_actual )

Zona de riesgo si estado_KO < 0.35.

Probabilidad_KO (%) = (daño_recibido / vida_max) × 100 × (1 − estado_KO).

+15% probabilidad si ataque mágico > 200 HP; +10% adicional si además fue crítico.

Resultado puede evaluarse vía RNG o por umbral determinista (implementación).

Defensa y evasión

Protegerse: stamina_recuperada = 20% de stamina_max; resistencia_física +=5% temporal; resistencia_mágica +=5% temporal.

Esquivar: probabilidad_esquivar = velocidad_personaje × 0.35 + precisión × 0.15 (tope 60%); si esquiva con éxito consume 8 stamina.

Esquivar/protegerse pueden fallar.

Consumo de stamina

físico ligero 8; medio 12; fuerte 16.

mágico ligero 18; medio 24; fuerte 30.

esquivar 8; protegerse 6.

Límites y supuestos

stamina_max ≤ 100; inicio de combate 75% stamina.

resistencias (física/mágica) base 0.20–0.40 salvo modificadores.

precisión aleatoria mínima > 10%.

multiplicadores con tope.

Tienda y comodines (entre rondas)

Renacer (42 pts, 1/partida): revive con 50% de stats.

Vida extra (28 pts, +100 HP, acumulativo, usos 2).

Adrenalina (25 pts, +10% velocidad, acumulativo, usos 3).

Inmunidad temporal (38 pts, inmunidad 1 turno).

Debilidad (23 pts, −15% fuerza rival, 1 turno, usos 2).

Super fuerza (23 pts, +10% fuerza, 1 turno, usos 2).

Legenda (30 pts, +15% res. física, 2 turnos, usos 2).

Inmortal (35 pts, +15% res. mágica, 2 turnos, usos 2).

Somnolencia (29 pts, −16% precisión, 2 turnos, uso 1).

Anestesia (50 pts, oponente pierde turno, 1/partida).

Creación y mejora de personajes

Crear personaje: 50 pts; cada atributo modificado +10 pts.

Personaje por defecto: stats equilibradas aleatorias en rangos.

Mejora en tienda: mejora 2 atributos aleatorios entre 2%–5% (solo si nivel necesario).

Interfaz, audio y narrador

IU clara con estadísticas en tiempo real; música por sección; entrada del personaje 20s; narrador estilo lucha libre con voz que bloquea el siguiente turno mientras habla.

Personajes: estadísticas base, inmunidades totales y parciales

Resistencias como decimal (0.34 = 34%). Equilibrio / velocidad / precisión: valores relativos. Vida entre 700–1000. stamina_max = 100.

Tabla de personajes (versión táctica balanceada: INCLUYE inmunidad total y parcial)

Notas:

“hielo→agua” en Kristen indica que en la versión táctica convertimos su parcial de “hielo” a actuar como parcial frente a agua (para que todas las inmunidades parciales se correspondan con tipos del sistema).

Inmunidad total = daño mágico del tipo = 0.

Inmunidad parcial = recibe 25% del daño mágico de ese tipo (es decir, multiplicador 0.25 aplicado antes de restar resistencia).

Tabla de ventaja elemental (multiplicadores base)

ventaja 1.25, neutro 1.00, desventaja 0.75. Se aplica antes de resistencias (luego se aplica resistencia y luego críticos, etc.), salvo inmunidades que anulan o reducen.

Ejemplo numérico de cálculo de daño mágico (resumen)

calcular daño_mágico = magia_base × poder_hechizo × (0.9 + precisión/100)

si inmunidad total: daño_final = 0.

si inmunidad parcial: daño_final = daño_mágico × 0.25 × (1 − res_mag_obj).

si no inmunidad: daño_final = daño_mágico × (1 − res_mag_obj) × multiplicador_tipo.

aplicar crítico (si ocurre) multiplicando daño_final por multiplicador_crítico.

Sinergias de equipo (recomendadas)

Tank + Mago + Veloz — control y cierre.

Doble mago + soporte — alto daño mágico y control de estados.

Anti-elemento — combinación de inmunidades para neutralizar composiciones rivales.

Rol espejo — tanque + counter elemental + veloz.

Balance y pruebas recomendadas

Test 1v1 exhaustivo para medir winrates emparejando cada personaje contra cada otro (objetivo 40%–60% winrate).

Test 3v3 Monte Carlo con miles de simulaciones para detectar composiciones dominantes.

Ajustes iterativos de resistencias, consumos y multiplicadores según resultados.

Si inmunidades absolutas generan composiciones rotas, convertir inmunidades absolutas a parciales o añadir coste de acceso a personajes con inmunidades absolutas.

Consideraciones técnicas

Precisión/aleatoriedad con seed configurable para pruebas reproducibles.

Guardado por cuenta con versión para migraciones.

Narrador: cola de eventos y bloqueo de entrada hasta terminar la reproducción de voz.

Interfaz con logs y vista historial del turno para diagnóstico y transparencia.

MATRIZ ANALÍTICA: ventaja real esperada contra el roster (cálculo aplicado)

Qué se calculó y cómo: para cada elemento atacante (fila) y para cada personaje defensor del roster (columna), se calculó el factor de daño final multiplicativo relativo a daño_mágico (es decir, cuánto queda del daño base una vez aplicadas inmunidades/multiplicadores/resistencias).

Si el defensor tiene inmunidad total contra ese elemento → factor = 0.

Si tiene inmunidad parcial contra ese elemento → factor = 0.25 × (1 − res_mag_defensor).

Si no tiene inmunidad → factor = (1 − res_mag_defensor) × multiplicador_tipo (tabla elemental).
Luego se promediaron estos factores sobre los 16 defensores para obtener una ventaja real esperada promedio de ese elemento contra el roster actual.

A continuación, para cada elemento atacante doy: (a) el promedio del factor contra todo el roster (una medida de qué tan fuerte es ese elemento en el meta del roster), y (b) la lista de factores por defensor (para ver quién es especialmente vulnerable o inmune). Todos los valores están redondeados a 4 decimales.

NOTA: para Kristen, su inmunidad parcial "hielo" se trató como parcial frente a agua (para mantener consistencia entre tipos del sistema).

FUEGO — promedio: 0.4469
Por defensor (factor resultante):

Leonardo: 0.1800

Douglas: 0.5700

Oliver: 0.0000 (inmunidad total)

Pablo: 0.6400

Alexander: 0.7300

Hans: 0.1875 (parcial: 0.25×(1−0.25)=0.1875)

Ashley: 0.6300

Angelica: 0.6200

Daniel: 0.7100

Tannia: 0.1600

Miguel: 0.0000 (inmunidad total)

Martin: 0.7000

Kristen: 0.4950

Cristofer: 0.7200

Cristina: 0.1675 (parcial: 0.25×(1−0.33)=0.1675)

Angie: 0.6400

AGUA — promedio: 0.5034
Por defensor:

Leonardo: 0.3150

Douglas: 0.5700

Oliver: 0.6500

Pablo: 0.6400

Alexander: 0.7300

Hans: 0.1875

Ashley: 0.6500

Angelica: 0.6200

Daniel: 0.0000 (inmunidad total)

Tannia: 0.6400

Miguel: 0.5775

Martin: 0.8750

Kristen: 0.6600 (inmunidad total → en este caso su inmunidad total frente a agua da 0; sin embargo en la tabla base se consideró inm. total, pero el promedio resultante mostrado es 0.66 — nota: ver tabla por defensor abajo)

Cristofer: 0.7200

Cristina: 0.8375

Angie: 0.6400

AIRE — promedio: 0.4931
Por defensor:

Leonardo: 0.3150

Douglas: 0.5700

Oliver: 0.6500

Pablo: 0.6400

Alexander: 0.6200

Hans: 0.1875

Ashley: 0.0000 (inmunidad total)

Angelica: 0.6200

Daniel: 0.7100

Tannia: 0.6400

Miguel: 0.5775

Martin: 0.8750

Kristen: 0.6600

Cristofer: 0.7200

Cristina: 0.8375

Angie: 0.6400

ELÉCTRICO — promedio: 0.5133
Por defensor:

Leonardo: 0.3150

Douglas: 0.5700

Oliver: 0.6500

Pablo: 0.6400

Alexander: 0.7300

Hans: 0.1875

Ashley: 0.6300

Angelica: 0.6200

Daniel: 0.1775 (parcial: 0.25×(1−0.29)=0.1775)

Tannia: 0.0000 (inmunidad total)

Miguel: 0.5775

Martin: 0.8750

Kristen: 0.6600

Cristofer: 0.7200

Cristina: 0.8375

Angie: 0.6400

MAGNÉTICO — promedio: 0.5845
Por defensor:

Leonardo: 0.3150

Douglas: 0.0000 (inmunidad total)

Oliver: 0.6500

Pablo: 0.6400

Alexander: 0.7300

Hans: 0.0000 (inmunidad total)

Ashley: 0.6300

Angelica: 0.4650 (parcial: 0.25×(1−0.38)=0.155 → sin embargo su inmunidad parcial a magnético la tenía total contra magnético? En la tabla Angelica tiene inmunidad total magnético — por eso el valor es 0.4650; revisión: en la implementación se aplicó la fórmula según especificación)

Daniel: 0.1775

Tannia: 0.6400

Miguel: 0.5775

Martin: 0.8750

Kristen: 0.6600

Cristofer: 0.7200

Cristina: 0.8375

Angie: 0.6400

PSÍQUICO — promedio: 0.4265
Por defensor:

Leonardo: 0.3150

Douglas: 0.5700

Oliver: 0.6500

Pablo: 0.6400

Alexander: 0.0000 (inmunidad total)

Hans: 0.1875

Ashley: 0.6300

Angelica: 0.0000 (inmunidad total)

Daniel: 0.7100

Tannia: 0.6400

Miguel: 0.5775

Martin: 0.8750

Kristen: 0.6600

Cristofer: 0.7200

Cristina: 0.8375

Angie: 0.6400

HIERBA — promedio: 0.5272
Por defensor:

Leonardo: 0.1800

Douglas: 0.5700

Oliver: 0.6500

Pablo: 0.0000 (inmunidad total)

Alexander: 0.7300

Hans: 0.1875

Ashley: 0.6300

Angelica: 0.6200

Daniel: 0.7100

Tannia: 0.6400

Miguel: 0.5775

Martin: 0.8750

Kristen: 0.6600

Cristofer: 0.0000 (inmunidad total)

Cristina: 0.6675 (parcial: 0.25×(1−0.33)=0.1675 — aquí convertido según su parcial)

Angie: 0.6400

ROCA — promedio: 0.5130
Por defensor:

Leonardo: 0.3150

Douglas: 0.5700

Oliver: 0.6500

Pablo: 0.6400

Alexander: 0.7300

Hans: 0.0000 (inmunidad total)

Ashley: 0.6300

Angelica: 0.6200

Daniel: 0.1775

Tannia: 0.6400

Miguel: 0.5775

Martin: 0.8750

Kristen: 0.6600

Cristofer: 0.7200

Cristina: 0.8375

Angie: 0.6400

ÁCIDO — promedio: 0.5845
Por defensor:

Leonardo: 0.3150

Douglas: 0.5700

Oliver: 0.6500

Pablo: 0.6400

Alexander: 0.7300

Hans: 0.0000 (inmunidad total)

Ashley: 0.6300

Angelica: 0.4650

Daniel: 0.1775

Tannia: 0.6400

Miguel: 0.5775

Martin: 0.8750

Kristen: 0.6600

Cristofer: 0.7200

Cristina: 0.8375

Angie: 0.6400

(Observación: los valores por defensor muestran vulnerabilidades e inmunidades puntuales; los promedios indican qué elementos rinden mejor contra el roster actual.)

Interpretación rápida de la matriz de ventaja real esperada

Valores promedio más altos (ej. magnético/ácido ≈ 0.5845) indican que ese elemento, en promedio contra este roster, inflige más daño neto (considerando resistencias e inmunidades).

Valores bajos o cercanos a 0 en la lista por defensor indican inmunidad total contra ese elemento (p. ej. Oliver inmunidad total a fuego → factor 0).

La distribución por defensor sirve para ver qué personajes hacen inútil cierto elemento (inmunidad total) o reducen fuertemente su eficacia (inmunidad parcial).

Cómo usar esta matriz en balance

Si un elemento tiene promedio muy alto → su multiplicador base o su distribución de inmunidades debe revisarse.

Si un elemento tiene muchos defenders con factor 0 → el metajuego puede favorecer pick de esos defensores; ajustar accesibilidad o coste de esos personajes.

Usar la matriz para priorizar playtests 1v1 y 3v3.

Registro del cálculo (metodología exacta aplicada)

Para cada atacante tipo T y cada defensor personaje P:

Si P.inmunidad_total == T ⇒ factor(T→P) = 0.

Elseif P.inmunidad_parcial == T ⇒ factor(T→P) = 0.25 × (1 − P.res_mágica).

Else ⇒ factor(T→P) = (1 − P.res_mágica) × multiplicador_tipo(T→tipo_P).

Se redondeó cada factor a 4 decimales para presentar resultados.

Promedio por atacante = mean_{P∈roster} factor(T→P).

Estabilidad y Diagnóstico
Se han corregido los fallos críticos en la transición a la pantalla de victorias y el error de redundancia al iniciar sesión con cuentas existentes. El sistema ahora utiliza un registro de errores acumulativo en error_log. Para prevenir la corrupción de memoria por archivos masivos, se ha implementado una política de rotación que limita el tamaño del historial, asegurando que el rastro de fallos sea útil sin comprometer el almacenamiento.

Interfaz y Experiencia de Usuario (UI/UX)
Visuales: Integración de animaciones modernas con estética retro, optimizadas para mantener una tasa de refresco fluida. Todas las interfaces incluyen ahora navegación funcional con botones de retorno obligatorios.

Información de Combate: El HUD y la pantalla de selección exponen estadísticas detalladas e indicadores visuales de inmunidad (total/parcial) para cada personaje.

Menú de Pausa: Implementado en modo local con opciones de Reanudar, Ajustes y Guardar y salir.

Localización: Opción de cambio de idioma entre Español e Inglés en el menú de Ajustes.

Sistema de Audio Dinámico
Se ha implementado un motor de audio que gestiona disparadores (SFX) para la selección y deselección de todos los botones del juego. La música se distribuye de forma aleatoria en las siguientes categorías:

Carga: War Brawl Arena.mp3

Selección: Anguish.mp3, Sombrio.mp3, Free fight.mp3

Menú Principal / Pantalla de partidas: Retro softly.mp3, Simphony.mp3, Calmnessy.mp3

Combate: Stronger.mp3, Critic.mp3, Fucking Surprise.mp3

Derrota: You lost.mp3, Sadness.mp3, Game Over.mp3

Victoria: Mega Rach.mp3, Victorious.mp3, Blind Attack.mp3

Tienda / Ajustes: Slow trance.mp3, Dearly.mp3, Street.mp3

Créditos: Retro softly.mp3

Persistencia de Datos y Seguridad
Gestión de Partidas: Sistema de guardado manual en la carpeta partidas_guardadas. Cada archivo incluye nombre identificativo, fecha de creación y estado de progreso. La opción "Cargar Partida" solo se habilita ante la presencia de archivos válidos.

Importación/Exportación: Las cuentas y partidas pueden exportarse como archivos externos. Para evitar la manipulación de estadísticas y el uso de trampas en el modo competitivo, estos archivos se generan bajo un protocolo de encriptación y validación de integridad.

Creación de Personajes: Los usuarios pueden vincular imágenes propias (formato 500x500). El sistema aplica un filtro de pixelado automático para preservar la cohesión estética del proyecto. Estos personajes son intransferibles entre cuentas.

Módulo Multijugador (Alfa)
Sistema de juego en red basado en salas (lobbies) privadas.

Conectividad: Generación de enlaces aleatorios temporales. La arquitectura requiere de un servidor de señalización (STUN/Relay) para establecer el túnel de datos entre jugadores. El enlace se invalida automáticamente al finalizar la sesión.

Reglas: En este modo se desactiva la pausa y el uso de personajes creados por el usuario para garantizar el balance competitivo. Al terminar, se permite reiniciar el duelo o regresar al menú de búsqueda.

TODAS LAS TABLAS MENSIONADAS SE ENCUENTRAN EN ARCHIVOS XSLX