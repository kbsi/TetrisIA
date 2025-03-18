# Tetris - Humain vs IA

Ce projet est un jeu de Tetris à deux joueurs, où un joueur humain affronte une IA.

## Description

Le jeu comprend deux grilles de Tetris côte à côte, une pour le joueur humain et une pour l'IA.
Les deux joueurs s'affrontent en temps réel, avec des interactions spéciales entre eux.

### Fonctionnalités principales

- Deux grilles de jeu affichées côte à côte
- Système de score en temps réel
- IA avec différents niveaux de difficulté
- Fonctionnalités spéciales:
  - Cadeau surprise lorsqu'un joueur complète 2 lignes
  - Pause douceur tous les 1 000 points
  - Pièces spéciales tous les 3 000 points
  - Mode arc-en-ciel toutes les 2 minutes

## Installation

1. Assurez-vous d'avoir Python 3.6 ou supérieur installé.
2. Clonez ce dépôt:
   ```
   git clone <URL_du_dépôt>
   ```
3. Accédez au répertoire du projet:
   ```
   cd Tetris
   ```
4. Exécutez le jeu:
   ```
   python main.py
   ```

## Comment jouer

### Contrôles

- Flèches gauche/droite: Déplacer la pièce horizontalement
- Flèche haut: Faire pivoter la pièce
- Flèche bas: Faire descendre la pièce plus rapidement
- P: Mettre le jeu en pause
- R: Réinitialiser le jeu

## Règles du jeu

- Gagnez des points en complétant des lignes
- 50 points par ligne complétée
- Bonus de 100 points pour 2 lignes, 200 pour 3 lignes, 300 pour 4 lignes
- Quand un joueur complète 2 lignes, l'adversaire reçoit une pièce facile
- Tous les 1 000 points, la vitesse diminue temporairement
- Tous les 3 000 points, une pièce spéciale apparaît
- Toutes les 2 minutes, les couleurs des pièces changent

## Structure du projet

- `main.py`: Point d'entrée du jeu, interface utilisateur
- `tetris.py`: Classe principale du jeu Tetris
- `ai_player.py`: Logique de l'IA
- `pieces.py`: Classes pour les différentes pièces
- `constants.py`: Constantes et paramètres du jeu
