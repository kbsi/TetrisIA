# Prompts utilisés pour générer le projet

## Prompt 1 : Perplexity

```
Je dois créer un projet dans le cadre d'un cours sur l'IA générative et son utilisation pour la génération de code. Je vais te donner le sujet du projet et j'aimerai que tu écrives un prompt détaillé et bien structuré à destination de Claude afin qu'il me génère le projet dans vscode via Copilot. Tu dois me fournir un prompt sous forme de texte que je peux facilement copier/coller.
Voici le sujet du projet : "Projet : Tetris à deux joueurs (Humain vs
IA)
Vous devez coder un Tetris en Python avec Tkinter, avec deux joueurs : un humain et
une IA. Il faut une grille pour chaque joueur et un tableau des scores. Voici les
détails avec des règles originales :
Fonctionnalités principales
Deux grilles
Une pour le joueur humain, une pour l'IA, côte à côte.
Contrôles
Humain : flèches du clavier (gauche, droite, bas, haut pour tourner).
IA : joue automatiquement avec une logique simple (ex. : placer les pièces au
mieux sans trop réfléchir).
Tableau des scores
Points :
50 par ligne.
lignes).
Bonus : 100 pour 2 lignes, 200 pour 3 lignes, 300 pour un Tetris (4
Affiche les scores en direct pour les deux joueurs.
Règles fun
1. Cadeau surprise
Quand un joueur complète 2 lignes d'un coup, l'adversaire reçoit une "pièce
facile" (ex. : un carré ou une ligne droite) pour l'aider un peu.
2. Pause douceur
Tous les 1 000 points, les pièces tombent 20 % plus lentement pendant 10
secondes pour les deux joueurs – un petit répit pour souffler !
3. Pièce rigolote
Tous les 3 000 points, une pièce spéciale apparaît (ex. : une pièce en forme de
cœur ou d'étoile), qui vaut 100 points bonus si elle est bien placée.
4. Arc-en-ciel
Toutes les 2 minutes, les pièces changent de couleur pendant 20 secondes pour
rendre le jeu plus joli (pas de piège, juste du fun visuel).
Rendu du projet
Le projet complet doit être mis sur GitHub en dépôt public.
Le dépôt doit contenir :
Tout le code source du jeu
Un fichier PROMPTS.md documentant la liste des prompts utilisés pour
réaliser le projet
Un fichier README.md qui contient la procédure pour lancer le projet
Critères d'évaluation (20 points)
Qualité des prompts (10 points)
Pertinence et efficacité des prompts utilisés (4 points)
Créativité et originalité dans l'approche (3 points)
Documentation complète de tous les prompts dans un fichier PROMPTS.md (3
points)
Fonctionnalités du jeu (7 points)
Implémentation des deux grilles de jeu (1.5 points)
Contrôles du joueur humain et IA fonctionnels (1.5 points)
Système de score complet (1 point)
Implémentation des règles fun (3 points)
Documentation et utilisabilité (3 points)
README.md détaillé avec instructions claires pour lancer le projet (1.5
points)
Structure du code lisible et bien organisée (0.5 point)
Absence de bugs majeurs (1 point)"
```

## Prompt 2 -> VSCode + Copilot Edits / Claude 3.7

```
Tu es un assistant expert en programmation Python, spécialisé dans la création de jeux avec Tkinter. Ton objectif est de m’aider à coder un jeu de Tetris à deux joueurs (Humain vs IA). Voici les spécifications détaillées du projet que je souhaite réaliser :
		Contexte général :
	•	Le jeu doit être codé en Python en utilisant la bibliothèque Tkinter.
	•	Il doit comporter deux grilles de jeu côte à côte : une pour le joueur humain et une pour l’IA.
	•	Un tableau des scores doit afficher les points des deux joueurs en temps réel.
		Fonctionnalités principales :
	1.	Deux grilles : Une pour le joueur humain et une pour l’IA, affichées côte à côte dans la fenêtre Tkinter.
	2.	Contrôles :
	•	Joueur humain : Utilise les flèches du clavier pour déplacer les pièces (gauche, droite, bas) et les faire pivoter (flèche haut).
	•	IA : Joue automatiquement avec une logique simple pour placer les pièces de manière optimale.
	3.	Système de score :
	•	Points attribués :
	•	50 points par ligne complétée.
	•	Bonus : 100 points pour 2 lignes d’un coup, 200 points pour 3 lignes, et 300 points pour un Tetris (4 lignes).
	•	Les scores doivent être mis à jour en temps réel et affichés dans un tableau visible.
		Règles originales et fun :
	1.	Cadeau surprise : Lorsqu’un joueur complète 2 lignes d’un coup, l’adversaire reçoit une “pièce facile” (comme un carré ou une ligne droite).
	2.	Pause douceur : Tous les 1 000 points, la vitesse de chute des pièces diminue de 20 % pendant 10 secondes pour offrir un répit aux joueurs.
	3.	Pièce rigolote : Tous les 3 000 points, une pièce spéciale apparaît (exemple : en forme de cœur ou d’étoile). Si elle est bien placée, elle rapporte un bonus de 100 points.
	4.	Arc-en-ciel : Toutes les 2 minutes, les couleurs des pièces changent pendant 20 secondes pour ajouter une touche visuelle amusante.
		Contraintes techniques :
	•	Le projet doit être bien structuré avec des fonctions et classes claires.
	•	Le code doit être lisible, commenté et organisé.
		Rendu attendu :
	•	Un dépôt GitHub public contenant :
	•	Tout le code source du jeu.
	•	Un fichier `PROMPTS.md` documentant tous les prompts utilisés pour générer le projet.
	•	Un fichier `README.md` expliquant comment lancer le projet.
		Instructions spécifiques :
	•	Génère tout le code nécessaire pour ce projet en respectant ces spécifications.
	•	Inclue des commentaires détaillés dans le code pour expliquer chaque partie.
	•	Propose une structure de fichiers claire si nécessaire (par exemple, un fichier principal et des modules séparés).
		Format attendu :
		Fournis-moi le code complet prêt à être copié/collé dans Visual Studio Code (ou tout autre IDE Python), ainsi que toute explication utile si nécessaire.
```

## Prompt 3 -> VSCode + Copilot Chat / Claude 3.7

```
l'ia est très limité puisqu'elle met toutes les pièces à droite. De plus elle ne semble pas utiliser la descente rapide quand elle peut
```

## Prompt 4 -> VSCode + Copilot Chat / Claude 3.7

```
J'aimerai que l'IA ait 3 niveaux de rapidité, par défaut elle est au niveau 1 (la plus lente). Il faudrait pouvoir configurer sur l'interface cette rapidité.
```

## Prompt 5 -> VSCode + Copilot Edits / Claude 3.7

```
J'aimerai que l'interface ressemble à celui d'un jeu d'arcade. Et il faudrait des couleurs pastels pour les briques en mode normal, et des couleurs de type néons en mode arc-en-ciel afin de bien différencier les deux modes.
```

## Prompt 6 -> VSCode + Copilot Chat / Claude 3.7

```
j'aimerai qu'au niveau 1, l'ia n'utilise que rarement l'accélération de la descente
```
