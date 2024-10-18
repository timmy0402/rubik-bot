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

    def __createFace(self, color):
        return [[color for _ in range(self.size)] for _ in range(self.size)]

    def scrambleCube(self, scrambleLine: str):
        commandList = scrambleLine.split()
        for command in commandList:
            face = command[0]
            if len(command) == 1:
                rotations = 1
                clockwise = True
            elif command[1] == "'":
                rotations = 1
                clockwise = False
            elif command[1] == "2":
                rotations = 2
                clockwise = True
            for _ in range(rotations):
                rotate_face(self, face, clockwise)

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
