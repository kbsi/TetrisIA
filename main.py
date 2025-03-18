import tkinter as tk
from tkinter import font as tkfont
from tetris import Tetris
from ai_player import AIPlayer
from constants import *


class TetrisGame:
    def __init__(self, root):
        """Initialise le jeu de Tetris à deux joueurs"""
        self.root = root
        self.root.title("Tetris - Humain vs IA")
        self.root.configure(bg=ARCADE_BACKGROUND)
        # Permettre le redimensionnement horizontal et vertical
        self.root.resizable(True, True)

        # Configuration de la fenêtre
        # Espace pour deux grilles plus les scores
        window_width = (GRID_WIDTH * CELL_SIZE * 2) + 490
        window_height = GRID_HEIGHT * CELL_SIZE + 180
        self.root.geometry(f"{window_width}x{window_height}")

        # Frame principale qui contiendra tout
        main_frame = tk.Frame(self.root, bg=ARCADE_BACKGROUND)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Créer les frames pour chaque joueur
        human_frame = tk.Frame(main_frame, bg=ARCADE_PANEL_BG, padx=10, pady=10,
                               bd=3, relief="ridge", highlightbackground=ARCADE_BORDER_COLOR)
        human_frame.grid(row=0, column=0, sticky="nsew")

        ai_frame = tk.Frame(main_frame, bg=ARCADE_PANEL_BG, padx=10, pady=10,
                            bd=3, relief="ridge", highlightbackground=ARCADE_BORDER_COLOR)
        ai_frame.grid(row=0, column=2, sticky="nsew")

        # Frame centrale pour les scores
        score_frame = tk.Frame(main_frame, bg=ARCADE_BACKGROUND, width=200,
                               bd=2, relief="raised", highlightbackground=ARCADE_BORDER_COLOR)
        score_frame.grid(row=0, column=1, sticky="nsew", padx=20)

        # Configuration des colonnes pour que la frame centrale soit plus petite
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=3)

        # Configuration de la ligne pour qu'elle s'étende
        main_frame.rowconfigure(0, weight=1)

        # Initialiser les jeux
        self.human_player = Tetris(human_frame, "Humain")
        self.ai_player = AIPlayer(ai_frame, "IA")

        # Lier les joueurs entre eux pour les interactions
        self.human_player.set_opponent(self.ai_player)
        self.ai_player.set_opponent(self.human_player)

        # Configurer l'affichage des scores
        self.setup_score_display(score_frame)

        # Associer les touches du clavier pour le joueur humain
        self.bind_keys()

        # Démarrer la mise à jour des scores
        self.update_score_display()

    def setup_score_display(self, frame):
        """Configure l'affichage des scores"""
        # Titre
        try:
            title_font = tkfont.Font(
                family="Press Start 2P", size=16, weight="bold")
        except:
            title_font = tkfont.Font(family="Courier", size=16, weight="bold")

        title = tk.Label(frame, text="SCORES", font=title_font,
                         bg=ARCADE_BACKGROUND, fg=ARCADE_TEXT_COLOR)
        title.pack(pady=20)

        # Score du joueur humain
        try:
            game_font = tkfont.Font(family="Press Start 2P", size=14)
            score_font = tkfont.Font(
                family="Press Start 2P", size=24, weight="bold")
            small_font = tkfont.Font(
                family="Press Start 2P", size=10)  # Ajout de small_font
        except:
            game_font = tkfont.Font(family="Courier", size=14)
            score_font = tkfont.Font(family="Courier", size=24, weight="bold")
            small_font = tkfont.Font(
                family="Courier", size=10)  # Ajout de small_font

        human_label = tk.Label(frame, text="HUMAIN", font=game_font,
                               bg=ARCADE_BACKGROUND, fg=ARCADE_SCORE_COLOR)
        human_label.pack(pady=(20, 5))

        self.human_score_label = tk.Label(frame, text="0", font=score_font,
                                          bg=ARCADE_BACKGROUND, fg="white")
        self.human_score_label.pack()

        # Séparateur
        separator = tk.Frame(frame, height=2, width=150,
                             bg=ARCADE_BORDER_COLOR)
        separator.pack(pady=15)

        # Score de l'IA
        ai_label = tk.Label(frame, text="IA", font=game_font,
                            bg=ARCADE_BACKGROUND, fg=ARCADE_SCORE_COLOR)
        ai_label.pack(pady=(5, 5))

        self.ai_score_label = tk.Label(frame, text="0", font=score_font,
                                       bg=ARCADE_BACKGROUND, fg="white")
        self.ai_score_label.pack()

        # Niveau de l'IA
        ai_level_frame = tk.Frame(frame, bg=ARCADE_BACKGROUND)
        ai_level_frame.pack(pady=(15, 5), fill="x")

        ai_level_label = tk.Label(ai_level_frame, text="NIVEAU IA", font=game_font,
                                  bg=ARCADE_BACKGROUND, fg=ARCADE_SCORE_COLOR)
        ai_level_label.pack(pady=(0, 5))

        # Frame pour les boutons de niveau (maintenant vertical)
        self.level_buttons_frame = tk.Frame(frame, bg=ARCADE_BACKGROUND)
        self.level_buttons_frame.pack(pady=(0, 10))

        # Boutons pour les différents niveaux
        levels = [("1 - LENT", 1), ("2 - MOYEN", 2), ("3 - RAPIDE", 3)]

        self.level_buttons = []  # Pour stocker les références aux boutons

        for text, level in levels:
            button = tk.Button(self.level_buttons_frame,
                               text=text,
                               bg=ARCADE_PANEL_BG,
                               fg=ARCADE_TEXT_COLOR,
                               bd=2,
                               width=12,  # Largeur fixe
                               relief="raised",
                               padx=5,
                               pady=3,
                               command=lambda l=level: self.set_ai_level(l))
            button.pack(pady=2)  # Placement vertical avec espacement
            self.level_buttons.append(button)

        # Marquer le niveau 1 comme actif par défaut
        self.level_buttons[0].config(
            bg=ARCADE_SCORE_COLOR,
            fg=ARCADE_PANEL_BG,
            relief="sunken",
            font=small_font
        )

        # Contrôles
        controls_frame = tk.Frame(
            frame, bg=ARCADE_PANEL_BG, bd=2, relief="sunken")
        controls_frame.pack(pady=(15, 0), fill="x", padx=10)

        controls_title = tk.Label(controls_frame, text="CONTRÔLES", font=game_font,
                                  bg=ARCADE_PANEL_BG, fg=ARCADE_TEXT_COLOR)
        controls_title.pack(pady=(10, 10))

        controls = [
            "← → : Déplacer",
            "↑ : Tourner",
            "↓ : Descente rapide",
            "P : Pause",
            "R : Redémarrer"
        ]

        for control in controls:
            control_label = tk.Label(controls_frame, text=control, font=small_font,
                                     bg=ARCADE_PANEL_BG, fg=ARCADE_SCORE_COLOR)
            control_label.pack(anchor="w", pady=2, padx=10)

    def update_score_display(self):
        """Met à jour l'affichage des scores"""
        # Mettre à jour les scores
        self.human_score_label.config(text=str(self.human_player.score))
        self.ai_score_label.config(text=str(self.ai_player.score))

        # Mettre en évidence le leader
        if self.human_player.score > self.ai_player.score:
            self.human_score_label.config(fg=ARCADE_TEXT_COLOR)
            self.ai_score_label.config(fg="white")
        elif self.ai_player.score > self.human_player.score:
            self.ai_score_label.config(fg=ARCADE_TEXT_COLOR)
            self.human_score_label.config(fg="white")
        else:
            self.human_score_label.config(fg="white")
            self.ai_score_label.config(fg="white")

        # Planifier la prochaine mise à jour
        self.root.after(100, self.update_score_display)

    def bind_keys(self):
        """Associe les touches du clavier aux actions du joueur humain"""
        self.root.bind(
            "<Left>", lambda e: self.human_player.move_piece("left"))
        self.root.bind(
            "<Right>", lambda e: self.human_player.move_piece("right"))
        self.root.bind(
            "<Down>", lambda e: self.human_player.move_piece("down"))
        self.root.bind("<Up>", lambda e: self.human_player.rotate_piece())
        self.root.bind("p", lambda e: self.toggle_pause())
        self.root.bind("P", lambda e: self.toggle_pause())
        self.root.bind("r", lambda e: self.reset_game())
        self.root.bind("R", lambda e: self.reset_game())
        # Raccourcis pour changer le niveau de l'IA
        self.root.bind("1", lambda e: self.set_ai_level(1))
        self.root.bind("2", lambda e: self.set_ai_level(2))
        self.root.bind("3", lambda e: self.set_ai_level(3))

    def toggle_pause(self):
        """Met le jeu en pause ou le reprend"""
        self.human_player.toggle_pause()
        self.ai_player.toggle_pause()

    def reset_game(self):
        """Réinitialise le jeu"""
        self.human_player.reset()
        self.ai_player.reset()

    def set_ai_level(self, level):
        """Change le niveau de l'IA"""
        if self.ai_player.set_ai_level(level):
            # Mettre à jour l'apparence des boutons
            for i, button in enumerate(self.level_buttons):
                if i+1 == level:
                    # Style pour le bouton actif
                    button.config(
                        bg=ARCADE_SCORE_COLOR,
                        fg=ARCADE_PANEL_BG,
                        relief="sunken",
                        font=tkfont.Font(weight="bold", size=10)
                    )
                else:
                    # Style pour les boutons inactifs
                    button.config(
                        bg=ARCADE_PANEL_BG,
                        fg=ARCADE_TEXT_COLOR,
                        relief="raised",
                        font=tkfont.Font(size=10)
                    )


if __name__ == "__main__":
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()
