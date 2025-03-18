class Piece:
    """Classe représentant une pièce de Tetris"""

    def __init__(self, shape, color_id):
        self.shape = shape
        self.color_id = color_id
        self.rotation = 0
        self.x = 3  # Position initiale au centre supérieur
        self.y = 0

    def get_coords(self):
        """Retourne les coordonnées des blocs de la pièce selon sa rotation actuelle"""
        rotated_shape = self.rotate_shape(self.shape, self.rotation)
        coords = []
        for y, row in enumerate(rotated_shape):
            for x, cell in enumerate(row):
                if cell:
                    coords.append((self.x + x, self.y + y))
        return coords

    def rotate(self):
        """Tourne la pièce à 90 degrés dans le sens horaire"""
        self.rotation = (self.rotation + 1) % len(self.shape)

    @staticmethod
    def rotate_shape(shape, rotation):
        """Applique une rotation à la forme de la pièce"""
        return shape[rotation]


class IPiece(Piece):
    """Pièce I (forme de ligne)"""

    def __init__(self):
        shape = [
            [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0]
            ],
            [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ]
        ]
        super().__init__(shape, 1)


class JPiece(Piece):
    """Pièce J"""

    def __init__(self):
        shape = [
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 1],
                [0, 1, 0],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]
            ]
        ]
        super().__init__(shape, 2)


class LPiece(Piece):
    """Pièce L"""

    def __init__(self):
        shape = [
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 0, 0]
            ],
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ]
        ]
        super().__init__(shape, 3)


class OPiece(Piece):
    """Pièce O (carré)"""

    def __init__(self):
        shape = [
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ]
        ]
        super().__init__(shape, 4)


class SPiece(Piece):
    """Pièce S"""

    def __init__(self):
        shape = [
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 0]
            ],
            [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
        ]
        super().__init__(shape, 5)


class TPiece(Piece):
    """Pièce T"""

    def __init__(self):
        shape = [
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
        ]
        super().__init__(shape, 6)


class ZPiece(Piece):
    """Pièce Z"""

    def __init__(self):
        shape = [
            [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0]
            ]
        ]
        super().__init__(shape, 7)


class HeartPiece(Piece):
    """Pièce spéciale en forme de cœur"""

    def __init__(self):
        shape = [
            [
                [0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0]
            ],
            [
                [0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0]
            ],
            [
                [0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0]
            ],
            [
                [0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0]
            ]
        ]
        super().__init__(shape, 8)


class StarPiece(Piece):
    """Pièce spéciale en forme d'étoile"""

    def __init__(self):
        shape = [
            [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0]
            ],
            [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 0, 0]
            ],
            [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0]
            ],
            [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 1, 1, 0],
                [0, 0, 1, 0, 0]
            ]
        ]
        super().__init__(shape, 8)


def get_random_piece(special=False):
    """Retourne une pièce aléatoire"""
    import random

    if special:
        return random.choice([HeartPiece(), StarPiece()])
    else:
        return random.choice([IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()])


def get_easy_piece():
    """Retourne une pièce facile (I ou O)"""
    import random
    return random.choice([IPiece(), OPiece()])
