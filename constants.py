# Configuration de la grille
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
BORDER_WIDTH = 1

# Couleurs pastels pour le mode normal
COLORS = {
    0: "#FFFFFF",  # Empty - Blanc
    1: "#B4BCFF",  #
    2: "#B4BCFF",  #
    3: "#B4BCFF",  #
    4: "#B4BCFF",  #
    5: "#B4BCFF",  #
    6: "#B4BCFF",  #
    7: "#B4BCFF",  #
    8: "#FFDDF3",  # Pièce spéciale - Rose pâle
    9: "#FFFFFF",  # Bordure
}

# Couleurs néons vives pour le mode arc-en-ciel
RAINBOW_COLORS = {
    0: "#111111",  # Empty - Noir pour contraste
    1: "#00FFFF",  # I - Cyan néon
    2: "#0066FF",  # J - Bleu néon
    3: "#FF6600",  # L - Orange néon
    4: "#FFFF00",  # O - Jaune néon
    5: "#00FF00",  # S - Vert néon
    6: "#FF00FF",  # T - Rose néon
    7: "#FF0000",  # Z - Rouge néon
    8: "#00FFAA",  # Pièce spéciale - Turquoise néon
    9: "#FFFFFF",  # Bordure - Blanc
}

# Eléments d'interface arcade
ARCADE_BACKGROUND = "#111122"  # Fond bleu très sombre
ARCADE_TEXT_COLOR = "#FFFF00"  # Texte jaune vif
ARCADE_BORDER_COLOR = "#FF00FF"  # Bordure rose néon
ARCADE_PANEL_BG = "#222244"  # Fond pour les panneaux
ARCADE_TITLE_FONT = ("Press Start 2P", 18, "bold")  # Police arcade
ARCADE_FONT = ("Press Start 2P", 12)  # Police normale arcade
ARCADE_SCORE_COLOR = "#00FFFF"  # Couleur cyan pour les scores

# Vitesses
BASE_FALL_SPEED = 1000  # ms
SPEED_INCREASE = 50     # ms
MIN_FALL_SPEED = 100    # ms

# Scores
POINTS_PER_LINE = 50
BONUS_2_LINES = 100
BONUS_3_LINES = 200
BONUS_4_LINES = 300
SPECIAL_PIECE_BONUS = 100

# Timing events
RAINBOW_INTERVAL = 120000  # 2 minutes en ms
RAINBOW_DURATION = 20000   # 20 secondes en ms
SLOW_DOWN_DURATION = 10000  # 10 secondes en ms
SLOW_DOWN_FACTOR = 0.8     # 20% de réduction
