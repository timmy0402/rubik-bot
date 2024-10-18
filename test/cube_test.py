import unittest
import sys

sys.path.insert(0, '../src')

from cube import Cube

cube333_1 = Cube(size=3)
cube333_1_scramble = "U2 D F D' B2 R2 F2 L U' F' D' L2 D' R2 F2 U B2 U2 L'"
cube333_1.faces['white'] = [['green', 'blue', 'red'],
                            ['blue', 'white', 'white'],
                            ['blue', 'yellow', 'yellow']]
cube333_1.faces['orange'] = [['red', 'white', 'red'],
                             ['red', 'orange', 'orange'],
                             ['white', 'orange', 'yellow']]
cube333_1.faces['green'] = [['yellow', 'blue', 'orange'],
                            ['white', 'green', 'red'],
                            ['orange', 'orange', 'green']]
cube333_1.faces['red'] = [['blue', 'green', 'blue'], 
                          ['green', 'red', 'blue'],
                          ['orange', 'green', 'blue']]
cube333_1.faces['blue'] = [['white', 'orange', 'yellow'],
                           ['red', 'blue', 'yellow'],
                           ['white', 'white', 'green']]
cube333_1.faces['yellow'] = [['green', 'yellow', 'white'],
                             ['green', 'yellow', 'yellow'],
                             ['red', 'red', 'orange']]


cube333_2 = Cube(size=3)
cube333_2_scramble = "R2 B2 D' B2 D2 L2 B' L2 F' U2 F2 U2 L2 R F2 D' L' B D' B2"
cube333_2.faces['white'] = [['yellow', 'blue', 'white'],
                            ['yellow', 'white', 'green'],
                            ['blue', 'orange', 'white']]
cube333_2.faces['orange'] = [['orange', 'green', 'orange'],
                             ['white', 'orange', 'blue'],
                             ['red', 'yellow', 'orange']]
cube333_2.faces['green'] = [['white', 'green', 'red'],
                            ['red', 'green', 'blue'],
                            ['white', 'green', 'red']]
cube333_2.faces['red'] = [['blue', 'white', 'green'], 
                          ['orange', 'red', 'white'],
                          ['yellow', 'white', 'blue']]
cube333_2.faces['blue'] = [['red', 'yellow', 'green'],
                           ['red', 'blue', 'orange'],
                           ['orange', 'yellow', 'yellow']]
cube333_2.faces['yellow'] = [['green', 'red', 'green'],
                             ['orange', 'yellow', 'blue'],
                             ['blue', 'red', 'yellow']]

cube222_1 = Cube(size=2)
cube222_1_scramble = "F R U R' F U' F U' F R U'"
cube222_1.faces['white'] = [['blue', 'orange'],
                            ['red', 'blue']]
cube222_1.faces['orange'] = [['red', 'white'],
                             ['orange', 'green']]
cube222_1.faces['green'] = [['green', 'orange'],
                            ['red', 'yellow']]
cube222_1.faces['red'] = [['white', 'green'], 
                          ['red', 'green']]
cube222_1.faces['blue'] = [['white', 'white'],
                           ['yellow', 'blue']]
cube222_1.faces['yellow'] = [['yellow', 'blue'],
                             ['yellow', 'orange']]

cube222_2 = Cube(size=2)
cube222_2_scramble = "U' R U2 R2 F R U' R' F' U R"
cube222_2.faces['white'] = [['green', 'red'],
                            ['green', 'orange']]
cube222_2.faces['orange'] = [['white', 'orange'],
                             ['orange', 'green']]
cube222_2.faces['green'] = [['yellow', 'white'],
                            ['red', 'white']]
cube222_2.faces['red'] = [['blue', 'yellow'], 
                          ['blue', 'orange']]
cube222_2.faces['blue'] = [['blue', 'red'],
                           ['white', 'blue']]
cube222_2.faces['yellow'] = [['yellow', 'red'],
                             ['yellow', 'green']]

class TestCubeMethod(unittest.TestCase):

    def test_cube_creation(self):
        for i in range(2, 8):
            sample = Cube(size=i)
            for face in sample.faces:
                row = [face] * i
                test_face = [row] * i
                self.assertEqual(sample.faces[face], test_face)

    def test_cube_scramble333(self):
        sample_1 = Cube(size=3)
        sample_1.scrambleCube(cube333_1_scramble)
        for face in sample_1.faces:
            self.assertEqual(sample_1.faces[face], cube333_1.faces[face])

        sample_2 = Cube(size=3)
        sample_2.scrambleCube(cube333_2_scramble)
        for face in sample_2.faces:
            self.assertEqual(sample_2.faces[face], cube333_2.faces[face])

    def test_cube_scramble222(self):
        sample_1 = Cube(size=2)
        sample_1.scrambleCube(cube222_1_scramble)
        for face in sample_1.faces:
            self.assertEqual(sample_1.faces[face], cube222_1.faces[face])

        sample_2 = Cube(size=2)
        sample_2.scrambleCube(cube222_2_scramble)
        for face in sample_2.faces:
            self.assertEqual(sample_2.faces[face], cube222_2.faces[face])


if __name__ == '__main__':
    unittest.main()
