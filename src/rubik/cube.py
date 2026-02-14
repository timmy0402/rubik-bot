from rubik.utils import rotate_face
from rubik.draw import draw_rubiks_cube


class Cube:
    """
    Represents a Rubik's Cube with a variable size (default 3x3).
    Handles the internal state of the cube faces and performs scrambling moves.
    """

    def __init__(self, size=3) -> None:
        """
        Initializes the cube with solved faces.

        Args:
            size (int): The dimensions of the cube (e.g., 3 for 3x3x3).
        """
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

    def __createFace(self, color) -> list[list[str]]:
        """
        Creates a 2D array representing a cube face, initialized with a single color.

        Args:
            color (str): The color name to fill the face with.

        Returns:
            list[list[str]]: A 2D list of size self.size x self.size.
        """
        return [[color for _ in range(self.size)] for _ in range(self.size)]

    def scrambleCube(self, scrambleLine: str) -> None:
        """
        Applies a sequence of scramble moves to the cube.

        Args:
            scrambleLine (str): A space-separated string of WCA scramble notations (e.g., "R U R' U'").
        """
        commandList = scrambleLine.split()
        for command in commandList:
            # Default parameters for single character scramble
            seen_3 = False  # Track if '3' exists in the command for wide moves
            rotations = 1
            clockwise = True
            extra_layer = 0

            # Parse each command for face, direction, and layer depth
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

            # Execute the rotation move
            for _ in range(rotations):
                rotate_face(self, face, clockwise, extra_layer)