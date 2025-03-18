import tkinter as tk
import random
import time
from constants import *
from pieces import get_random_piece, get_easy_piece


class Tetris:
    def __init__(self, frame, player_type, opponent=None):
        """Initialise le jeu Tetris"""
        self.frame = frame
        self.player_type = player_type
        self.opponent = opponent
        self.canvas = tk.Canvas(
            self.frame,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="white"
        )
        self.canvas.pack()

        # Label pour afficher des informations
        self.info_label = tk.Label(
            self.frame, text=f"{player_type} - Next Piece")
        self.info_label.pack()

        # Canvas pour la prochaine pièce
        self.next_canvas = tk.Canvas(
            self.frame,
            width=4 * CELL_SIZE,
            height=4 * CELL_SIZE,
            bg="lightgray"
        )
        self.next_canvas.pack()

        # Variables du jeu
        self.score = 0
        self.grid = [[0 for _ in range(GRID_WIDTH)]
                     for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = get_random_piece()
        self.fall_speed = BASE_FALL_SPEED
        self.game_over = False
        self.paused = False
        self.special_mode = None
        self.special_mode_end_time = 0
        self.last_score_milestone = 0
        self.rainbow_mode = False
        self.rainbow_mode_end_time = 0
        self.rainbow_start_time = time.time()

        # Démarre le jeu
        self.spawn_new_piece()
        self.update()
        self.check_rainbow_mode()

    def set_opponent(self, opponent):
        """Définit l'adversaire pour interagir avec lui"""
        self.opponent = opponent

    def spawn_new_piece(self):
        """Fait apparaître une nouvelle pièce"""
        self.current_piece = self.next_piece

        # Vérifie si une pièce spéciale doit être créée (tous les 3000 points)
        if self.score >= 3000 and (self.score // 3000) > (self.last_score_milestone // 3000):
            self.next_piece = get_random_piece(special=True)
            self.info_label.config(text=f"{self.player_type} - Special Piece!")
        else:
            self.next_piece = get_random_piece()
            self.info_label.config(text=f"{self.player_type} - Next Piece")

        self.draw_next_piece()

        # Vérifie si le jeu est terminé (collision dès le départ)
        if self.check_collision():
            self.game_over = True
            self.info_label.config(text=f"{self.player_type} - Game Over!")

    def draw_next_piece(self):
        """Dessine la prochaine pièce dans le canvas secondaire"""
        self.next_canvas.delete("all")

        # Adapte la taille en fonction de la pièce
        shape = self.next_piece.shape[0]
        size = len(shape)
        cell_size = min(4 * CELL_SIZE // size, CELL_SIZE)

        offset_x = (4 * CELL_SIZE - size * cell_size) // 2
        offset_y = (4 * CELL_SIZE - size * cell_size) // 2

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    color = RAINBOW_COLORS[self.next_piece.color_id] if self.rainbow_mode else COLORS[self.next_piece.color_id]
                    self.next_canvas.create_rectangle(
                        offset_x + x * cell_size,
                        offset_y + y * cell_size,
                        offset_x + (x + 1) * cell_size,
                        offset_y + (y + 1) * cell_size,
                        fill=color,
                        outline="black"
                    )

    def draw_grid(self):
        """Dessine la grille de jeu et les pièces"""
        self.canvas.delete("all")

        # Dessine le fond de la grille
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = "white"
                if self.grid[y][x] > 0:
                    color_id = self.grid[y][x]
                    color = RAINBOW_COLORS[color_id] if self.rainbow_mode else COLORS[color_id]

                self.canvas.create_rectangle(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    (x + 1) * CELL_SIZE,
                    (y + 1) * CELL_SIZE,
                    fill=color,
                    outline="lightgray"
                )

        # Dessine la pièce actuelle
        if self.current_piece and not self.game_over:
            coords = self.current_piece.get_coords()
            color_id = self.current_piece.color_id
            color = RAINBOW_COLORS[color_id] if self.rainbow_mode else COLORS[color_id]

            for x, y in coords:
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        (x + 1) * CELL_SIZE,
                        (y + 1) * CELL_SIZE,
                        fill=color,
                        outline="black"
                    )

        # Affiche un message si le jeu est terminé
        if self.game_over:
            self.canvas.create_rectangle(
                GRID_WIDTH * CELL_SIZE // 4,
                GRID_HEIGHT * CELL_SIZE // 3,
                GRID_WIDTH * CELL_SIZE * 3 // 4,
                GRID_HEIGHT * CELL_SIZE * 2 // 3,
                fill="white"
            )
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2,
                GRID_HEIGHT * CELL_SIZE // 2,
                text="GAME OVER",
                fill="red",
                font=("Arial", 20, "bold")
            )

        # Affiche un message de pause si le jeu est en pause
        if self.paused:
            self.canvas.create_rectangle(
                GRID_WIDTH * CELL_SIZE // 4,
                GRID_HEIGHT * CELL_SIZE // 3,
                GRID_WIDTH * CELL_SIZE * 3 // 4,
                GRID_HEIGHT * CELL_SIZE * 2 // 3,
                fill="white"
            )
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2,
                GRID_HEIGHT * CELL_SIZE // 2,
                text="PAUSE",
                fill="blue",
                font=("Arial", 20, "bold")
            )

    def update(self):
        """Mise à jour du jeu à chaque frame"""
        if not self.game_over and not self.paused:
            # Vérifie si un mode spécial est actif et s'il doit se terminer
            current_time = time.time() * 1000

            if self.special_mode and current_time > self.special_mode_end_time:
                self.fall_speed = BASE_FALL_SPEED
                self.special_mode = None

            if self.rainbow_mode and current_time > self.rainbow_mode_end_time:
                self.rainbow_mode = False

            # Vérifie si une pause douceur doit s'activer (tous les 1000 points)
            if self.score >= 1000 and (self.score // 1000) > (self.last_score_milestone // 1000):
                self.activate_slow_down()
                self.last_score_milestone = self.score

            # Fait tomber la pièce
            self.move_piece("down")

        # Redessine la grille
        self.draw_grid()

        # Programme la prochaine mise à jour
        self.frame.after(self.fall_speed, self.update)

    def check_rainbow_mode(self):
        """Vérifie si le mode arc-en-ciel doit s'activer"""
        current_time = time.time() * 1000
        elapsed_time = current_time - self.rainbow_start_time * 1000

        if elapsed_time >= RAINBOW_INTERVAL:
            self.activate_rainbow_mode()
            self.rainbow_start_time = time.time()

        # Programme la prochaine vérification
        self.frame.after(1000, self.check_rainbow_mode)

    def activate_rainbow_mode(self):
        """Active le mode arc-en-ciel pendant 20 secondes"""
        self.rainbow_mode = True
        self.rainbow_mode_end_time = time.time() * 1000 + RAINBOW_DURATION
        self.info_label.config(text=f"{self.player_type} - Rainbow Mode!")

    def activate_slow_down(self):
        """Active la pause douceur pendant 10 secondes"""
        self.special_mode = "slow_down"
        self.fall_speed = int(self.fall_speed * SLOW_DOWN_FACTOR)
        self.special_mode_end_time = time.time() * 1000 + SLOW_DOWN_DURATION
        self.info_label.config(text=f"{self.player_type} - Slow Down Mode!")

    def check_collision(self):
        """Vérifie si la pièce actuelle entre en collision avec les bordures ou d'autres pièces"""
        if not self.current_piece:
            return False

        coords = self.current_piece.get_coords()

        for x, y in coords:
            # Vérifie si la pièce sort de la grille ou entre en collision avec une autre pièce
            if (x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or
                    (y >= 0 and self.grid[y][x] > 0)):
                return True

        return False

    def merge_piece(self):
        """Fusionne la pièce actuelle avec la grille"""
        coords = self.current_piece.get_coords()
        color_id = self.current_piece.color_id

        for x, y in coords:
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                self.grid[y][x] = color_id

        # Vérifie les lignes complètes
        self.check_lines()

        # Fait apparaître une nouvelle pièce
        self.spawn_new_piece()

    def move_piece(self, direction):
        """Déplace la pièce dans la direction spécifiée"""
        if not self.current_piece or self.game_over or self.paused:
            return False

        old_x, old_y = self.current_piece.x, self.current_piece.y

        # Applique le mouvement
        if direction == "left":
            self.current_piece.x -= 1
        elif direction == "right":
            self.current_piece.x += 1
        elif direction == "down":
            self.current_piece.y += 1

        # Vérifie les collisions
        if self.check_collision():
            # Annule le mouvement
            self.current_piece.x, self.current_piece.y = old_x, old_y

            # Si la pièce ne peut plus descendre, elle est fixée
            if direction == "down":
                self.merge_piece()

            return False

        return True

    def rotate_piece(self):
        """Fait tourner la pièce actuelle"""
        if not self.current_piece or self.game_over or self.paused:
            return False

        old_rotation = self.current_piece.rotation

        # Applique la rotation
        self.current_piece.rotate()

        # Vérifie les collisions
        if self.check_collision():
            # Annule la rotation
            self.current_piece.rotation = old_rotation
            return False

        return True

    def check_lines(self):
        """Vérifie les lignes complètes et les supprime"""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y][x] > 0 for x in range(GRID_WIDTH)):
                # Supprime la ligne
                for y2 in range(y, 0, -1):
                    for x in range(GRID_WIDTH):
                        self.grid[y2][x] = self.grid[y2-1][x]

                # Vide la ligne du haut
                for x in range(GRID_WIDTH):
                    self.grid[0][x] = 0

                lines_cleared += 1
            else:
                y -= 1

        # Attribue des points selon le nombre de lignes complétées
        if lines_cleared == 1:
            self.score += POINTS_PER_LINE
        elif lines_cleared == 2:
            self.score += POINTS_PER_LINE * 2 + BONUS_2_LINES
            # Cadeau surprise pour l'adversaire
            if self.opponent:
                self.opponent.give_easy_piece()
        elif lines_cleared == 3:
            self.score += POINTS_PER_LINE * 3 + BONUS_3_LINES
        elif lines_cleared == 4:
            self.score += POINTS_PER_LINE * 4 + BONUS_4_LINES

        # Bonus pour les pièces spéciales bien placées
        if self.current_piece and self.current_piece.color_id == 8 and lines_cleared > 0:
            self.score += SPECIAL_PIECE_BONUS
            self.info_label.config(text=f"{self.player_type} - Special Bonus!")

        return lines_cleared

    def give_easy_piece(self):
        """Donne une pièce facile au joueur (carré ou ligne)"""
        if self.next_piece:
            self.next_piece = get_easy_piece()
            self.draw_next_piece()
            self.info_label.config(
                text=f"{self.player_type} - Received Easy Piece!")

    def toggle_pause(self):
        """Met le jeu en pause ou le reprend"""
        self.paused = not self.paused
        status = "Paused" if self.paused else "Resumed"
        self.info_label.config(text=f"{self.player_type} - {status}")

    def reset(self):
        """Réinitialise le jeu"""
        self.score = 0
        self.grid = [[0 for _ in range(GRID_WIDTH)]
                     for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = get_random_piece()
        self.fall_speed = BASE_FALL_SPEED
        self.game_over = False
        self.paused = False
        self.special_mode = None
        self.last_score_milestone = 0
        self.rainbow_mode = False
        self.rainbow_start_time = time.time()
        self.spawn_new_piece()
        self.info_label.config(text=f"{self.player_type} - New Game")

    def drop_piece(self):
        """Fait tomber la pièce jusqu'en bas"""
        if not self.current_piece or self.game_over or self.paused:
            return False

        # Continue de descendre tant qu'il n'y a pas de collision
        dropped = False
        while self.move_piece("down"):
            dropped = True

        return dropped
