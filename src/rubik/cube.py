from rubik.utils import rotate_face
from rubik.draw import draw_rubiks_cube


class Cube:
    def __init__(self, size=3):
        self.size = size
        self.faces = {
            "white": self.__createFace("white"),
            "green": self.__createFace("green"),
            "red": self.__createFace("red"),
            "blue": self.__createFace("blue"),
            "yellow": self.__createFace("yellow"),
            "orange": self.__createFace("orange"),
        }
        self.sides = ("F", "D", "U", "R", "L", "B")

    # Create a 2d array with a color by nxn
    def __createFace(self, color):
        return [[color for _ in range(self.size)] for _ in range(self.size)]

    def scrambleCube(self, scrambleLine: str):
        commandList = scrambleLine.split()
        for command in commandList:
            # default paramenter for single character scramble
            seen_3 = False  # see if 3 exist in the command
            rotations = 1
            clockwise = True
            extra_layer = 0
            # search for face and special notations
            for element in command:
                if element in self.sides:
                    face = element
                if element == "'":
                    clockwise = False
                if element == "2":
                    rotations = 2
                if element == "w" and not seen_3:
                    extra_layer = 1
                if element == "3":
                    extra_layer = 2
                    seen_3 = True
            for _ in range(rotations):
                rotate_face(self, face, clockwise, extra_layer)
