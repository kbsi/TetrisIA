import random
import time
import threading
from tetris import Tetris
from constants import *


class AIPlayer(Tetris):
    """Classe pour l'IA du jeu Tetris, hérite de la classe Tetris"""

    def __init__(self, frame, player_type, opponent=None):
        """Initialise l'IA du jeu Tetris"""
        super().__init__(frame, player_type, opponent)

        # Paramètres spécifiques à l'IA
        # Niveau par défaut (1 = lent, 2 = moyen, 3 = rapide)
        self.ai_level = 1
        self.difficulty = 1.0  # Suppression de la randomisation pour plus d'efficacité

        # Configuration des timings selon le niveau
        self.level_timings = {
            1: {"thinking": 200, "move_delay": 0.04, "drop_delay": 0.1},
            2: {"thinking": 100, "move_delay": 0.02, "drop_delay": 0.03},
            3: {"thinking": 50, "move_delay": 0.01, "drop_delay": 0.01}
        }

        # Applique les paramètres du niveau initial
        self.set_ai_level(self.ai_level)

        # Poids optimisés pour l'évaluation des positions
        self.weights = {
            'height': -0.510066,      # Pénalité pour la hauteur moyenne
            'lines': 0.760666,        # Bonus pour les lignes complétées
            'holes': -0.35663,        # Pénalité pour les trous
            'bumpiness': -0.184483,   # Pénalité pour les différences de hauteur
            'wells': -0.3,            # Pénalité pour les puits
            'hole_depth': -0.4,       # Pénalité pour la profondeur des trous
            'cleared_lines': 1.0,     # Bonus pour les lignes effacées
            'tetris_ready': 0.5,      # Bonus pour préparation de Tetris
            'max_height': -0.1        # Pénalité pour la hauteur maximale
        }

        # Démarrer le thread de l'IA
        self.ai_thread = threading.Thread(target=self.run_ai)
        self.ai_thread.daemon = True
        self.ai_thread.start()

    def set_ai_level(self, level):
        """Change le niveau de difficulté de l'IA (1=lent, 2=moyen, 3=rapide)"""
        if level in [1, 2, 3]:
            self.ai_level = level
            timings = self.level_timings[level]
            self.thinking_time = timings["thinking"]
            self.move_delay = timings["move_delay"]
            self.drop_delay = timings["drop_delay"]
            return True
        return False

    def run_ai(self):
        """Exécute la logique de l'IA en continu"""
        while True:
            # Attend un peu pour ne pas surcharger le CPU
            time.sleep(0.05)

            # Ne joue que si le jeu est actif
            if not self.game_over and not self.paused and self.current_piece:
                # Cherche le meilleur mouvement
                best_move = self.find_best_move()

                # Applique le mouvement
                if best_move:
                    rotations, position = best_move

                    # Effectue les rotations nécessaires
                    for _ in range(rotations):
                        self.rotate_piece()
                        time.sleep(self.move_delay)

                    # Déplace la pièce à la position souhaitée
                    while self.current_piece.x < position:
                        self.move_piece("right")
                        time.sleep(self.move_delay)

                    while self.current_piece.x > position:
                        self.move_piece("left")
                        time.sleep(self.move_delay)

                    # Comportement différent selon le niveau
                    if self.ai_level == 1:
                        # Au niveau 1, n'utilise l'accélération que rarement (20% de chance)
                        if random.random() < 0.2:
                            # Parfois utilise l'accélération
                            self.drop_piece()
                        else:
                            # La plupart du temps, descente progressive
                            drop_delay = 0.08  # Un peu plus rapide que le délai standard mais pas instantané
                            while self.move_piece("down"):
                                # Attend un peu entre chaque mouvement vers le bas
                                time.sleep(drop_delay)
                    else:
                        # Aux niveaux 2 et 3, utilise toujours l'accélération
                        self.drop_piece()

                    # Pause entre les pièces
                    time.sleep(self.drop_delay)

                # Temps de réflexion configuré
                time.sleep(self.thinking_time / 1000)

    def drop_piece(self):
        """Fait tomber la pièce jusqu'en bas"""
        while self.move_piece("down"):
            pass

    def find_best_move(self):
        """Trouve le meilleur mouvement possible"""
        if not self.current_piece:
            return None

        best_score = float('-inf')
        best_move = None

        # Sauvegarde l'état actuel de la pièce
        original_x = self.current_piece.x
        original_y = self.current_piece.y
        original_rotation = self.current_piece.rotation

        # Essaie toutes les rotations possibles
        for rotation in range(len(self.current_piece.shape)):
            # Applique la rotation
            self.current_piece.rotation = rotation

            # Détermine la plage de positions horizontales possibles
            # Limitons la recherche aux positions qui ont une chance d'être valides
            min_x = -1
            max_x = GRID_WIDTH + 1  # Réduit un peu la plage

            # Essaie toutes les positions horizontales
            for pos_x in range(min_x, max_x):
                # Positionne la pièce
                self.current_piece.x = pos_x
                self.current_piece.y = 0

                # Simule la chute de la pièce
                landing_height = self.simulate_drop()

                if landing_height is not None:
                    # Évalue la position seulement si la pièce est au moins partiellement dans la grille
                    self.current_piece.y = landing_height
                    coords = self.current_piece.get_coords()

                    # Vérifie si au moins une partie de la pièce est dans la grille
                    valid_position = False
                    for x, y in coords:
                        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                            valid_position = True
                            break

                    if valid_position:
                        score = self.evaluate_position()

                        # Plus de randomisation, on veut une IA optimale
                        # if random.random() > self.difficulty:
                        #     score += random.uniform(-10, 10)

                        if score > best_score:
                            best_score = score
                            best_move = (rotation, pos_x)

        # Restaure l'état original de la pièce
        self.current_piece.x = original_x
        self.current_piece.y = original_y
        self.current_piece.rotation = original_rotation

        return best_move

    def simulate_drop(self):
        """Simule la chute d'une pièce et retourne sa hauteur d'atterrissage"""
        if not self.current_piece:
            return None

        # Simule la chute
        y = 0
        while not self.would_collide(self.current_piece.x, y + 1, self.current_piece.rotation):
            y += 1

        return y

    def would_collide(self, x, y, rotation):
        """Vérifie si une position provoquerait une collision"""
        # Sauvegarde l'état actuel
        original_x = self.current_piece.x
        original_y = self.current_piece.y
        original_rotation = self.current_piece.rotation

        # Applique la nouvelle position
        self.current_piece.x = x
        self.current_piece.y = y
        self.current_piece.rotation = rotation

        # Vérifie la collision
        collision = self.check_collision()

        # Restaure l'état original
        self.current_piece.x = original_x
        self.current_piece.y = original_y
        self.current_piece.rotation = original_rotation

        return collision

    def evaluate_position(self):
        """Évalue la qualité d'une position"""
        # Simule l'ajout de la pièce à la grille
        temp_grid = [row[:] for row in self.grid]
        coords = self.current_piece.get_coords()
        color_id = self.current_piece.color_id

        # Compte combien de blocs sont effectivement placés dans la grille
        blocks_in_grid = 0
        for x, y in coords:
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                temp_grid[y][x] = color_id
                blocks_in_grid += 1

        # Si moins de 2 blocs sont dans la grille, c'est une très mauvaise position
        if blocks_in_grid < 2:
            return float('-inf')

        # Calcule les métriques
        heights = self.get_heights(temp_grid)
        max_height = max(heights) if heights else 0
        avg_height = sum(heights) / len(heights) if heights else 0
        holes = self.count_holes(temp_grid, heights)
        completed_lines = self.count_completed_lines(temp_grid)
        bumpiness = self.calculate_bumpiness(heights)
        wells = self.calculate_wells(heights)
        hole_depth = self.calculate_hole_depth(temp_grid)
        tetris_ready = self.is_tetris_ready(temp_grid, heights)

        # Vérifie les positions adjacentes pour éviter les hauteurs isolées
        adjacent_height_penalty = 0
        for i in range(len(heights) - 1):
            if abs(heights[i] - heights[i + 1]) > 2:
                adjacent_height_penalty += abs(heights[i] - heights[i + 1])

        # Calcule le score en fonction des poids
        score = (
            self.weights['height'] * avg_height +
            self.weights['lines'] * completed_lines * 10 +  # Augmenté à 10
            # Doublé pour plus d'impact
            self.weights['holes'] * holes * 2 +
            self.weights['bumpiness'] * bumpiness +
            self.weights['wells'] * wells +
            self.weights['hole_depth'] * hole_depth +
            # Augmenté à 10
            self.weights['cleared_lines'] * completed_lines * 10 +
            self.weights['max_height'] * max_height +      # Nouveau facteur
            # Pénalité pour les hauteurs inégales
            adjacent_height_penalty * -0.2
        )

        # Bonus pour une position prête pour un Tetris
        if tetris_ready:
            score += self.weights['tetris_ready'] * 20  # Doublé

        # Bonus pour les positions qui complètent des lignes
        if completed_lines > 0:
            score += completed_lines ** 2 * 20  # Doublé
            # Bonus spécial pour Tetris (4 lignes)
            if completed_lines == 4:
                score += 100  # Doublé

        # Pénalité supplémentaire pour les positions très hautes
        if max_height > GRID_HEIGHT * 0.7:
            score -= (max_height - GRID_HEIGHT * 0.7) * 16  # Doublé

        # Pénalité accrue pour les trous
        score -= holes ** 1.5 * 8  # Doublé

        # Bonus pour placer des pièces au centre (favoriser une construction équilibrée)
        center_x = sum(x for x, _ in coords) / len(coords)
        center_bonus = -abs(center_x - GRID_WIDTH / 2) + GRID_WIDTH / 4
        score += center_bonus * 0.1  # Petit bonus pour placer au centre

        return score

    def calculate_wells(self, heights):
        """Calcule la somme des profondeurs des puits"""
        wells = 0
        heights_with_walls = [GRID_HEIGHT] + heights + [GRID_HEIGHT]

        for i in range(1, len(heights_with_walls) - 1):
            left = heights_with_walls[i-1]
            center = heights_with_walls[i]
            right = heights_with_walls[i+1]

            if center < left and center < right:
                wells += min(left - center, right - center)

        return wells

    def calculate_hole_depth(self, grid):
        """Calcule la profondeur moyenne des trous"""
        total_depth = 0
        hole_count = 0

        for x in range(GRID_WIDTH):
            blocks_above = 0
            for y in range(GRID_HEIGHT):
                if grid[y][x] == 0:
                    total_depth += blocks_above
                    hole_count += 1
                else:
                    blocks_above += 1

        return total_depth if hole_count == 0 else total_depth / hole_count

    def is_tetris_ready(self, grid, heights):
        """Vérifie si une colonne est prête pour un Tetris"""
        # Recherche une colonne qui est plus basse que ses voisines
        for x in range(GRID_WIDTH):
            if x > 0 and x < GRID_WIDTH - 1:
                if heights[x] <= heights[x-1] - 4 and heights[x] <= heights[x+1] - 4:
                    # Vérifie si les autres colonnes sont assez hautes pour un Tetris
                    other_cols_heights = heights[:x] + heights[x+1:]
                    if min(other_cols_heights) >= 4:
                        return True
        return False

    def get_heights(self, grid):
        """Retourne la hauteur de chaque colonne"""
        heights = []
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if grid[y][x] > 0:
                    heights.append(GRID_HEIGHT - y)
                    break
            else:
                heights.append(0)
        return heights

    def count_holes(self, grid, heights):
        """Compte le nombre de trous dans la grille"""
        holes = 0
        for x in range(GRID_WIDTH):
            if heights[x] == 0:
                continue

            for y in range(GRID_HEIGHT - heights[x], GRID_HEIGHT):
                if grid[y][x] == 0:
                    holes += 1

        return holes

    def count_completed_lines(self, grid):
        """Compte le nombre de lignes complètes"""
        completed = 0
        for y in range(GRID_HEIGHT):
            if all(grid[y][x] > 0 for x in range(GRID_WIDTH)):
                completed += 1
        return completed

    def calculate_bumpiness(self, heights):
        """Calcule les différences de hauteur entre colonnes adjacentes"""
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness
