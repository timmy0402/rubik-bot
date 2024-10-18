from utils import rotate_face
from draw import draw_rubiks_cube

class Cube:
    def __init__(self, size=3):
        self.size = size
        self.faces = {
            'white': self.__createFace('white'),
            'green': self.__createFace('green'),
            'red': self.__createFace('red'),
            'blue': self.__createFace('blue'),
            'yellow': self.__createFace('yellow'),
            'orange': self.__createFace('orange')
        }
        self.sides = ("F","D","U","R","L","B")

    # Create a 2d array with a color by nxn
    def __createFace(self, color):
        return [[color for _ in range(self.size)] for _ in range(self.size)]

    def scrambleCube(self, scrambleLine: str):
        commandList = scrambleLine.split()
        for command in commandList:
            # default paramenter for single character scramble
            rotations = 1
            clockwise = True
            two_layer = False
            three_layer = False
            # search for face and special notations
            for element in command:
                if element in self.sides:
                    face = element
                if element == "'":
                    clockwise = False
                if element == "2":
                    rotations = 2
                if element == "w":
                    two_layer = True
                if element == "3":
                    three_layer = True
            for _ in range(rotations):
                rotate_face(self, face, clockwise, two_layer, three_layer)
                
    def print_cube(self):
        def print_face(face):
            for row in face:
                print(' '.join(row))
        print("White (Top):")
        print_face(self.faces['white'])
        print("\nGreen (Front):")
        print_face(self.faces['green'])
        print("\nRed (Right):")
        print_face(self.faces['red'])
        print("\nBlue (Left):")
        print_face(self.faces['blue'])
        print("\nOrange (Back):")
        print_face(self.faces['orange'])
        print("\nYellow (Bottom):")
        print_face(self.faces['yellow'])
