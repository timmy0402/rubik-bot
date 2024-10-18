import unittest
import sys

sys.path.insert(0, '../src')

from cube import Cube

class TestCubeMethod(unittest.TestCase):

    def setUp(self):
        self.cube333_1 = Cube(size=3)
        self.cube333_1_scramble = "U2 D F D' B2 R2 F2 L U' F' D' L2 D' R2 F2 U B2 U2 L'"
        self.cube333_1.faces['white'] = [['green', 'blue', 'red'],
                                         ['blue', 'white', 'white'],
                                         ['blue', 'yellow', 'yellow']]
        self.cube333_1.faces['orange'] = [['red', 'white', 'red'],
                                          ['red', 'orange', 'orange'],
                                          ['white', 'orange', 'yellow']]
        self.cube333_1.faces['green'] = [['yellow', 'blue', 'orange'],
                                         ['white', 'green', 'red'],
                                         ['orange', 'orange', 'green']]
        self.cube333_1.faces['red'] = [['blue', 'green', 'blue'], 
                                       ['green', 'red', 'blue'],
                                       ['orange', 'green', 'blue']]
        self.cube333_1.faces['blue'] = [['white', 'orange', 'yellow'],
                                        ['red', 'blue', 'yellow'],
                                        ['white', 'white', 'green']]
        self.cube333_1.faces['yellow'] = [['green', 'yellow', 'white'],
                                          ['green', 'yellow', 'yellow'],
                                          ['red', 'red', 'orange']]

        self.cube333_2 = Cube(size=3)
        self.cube333_2_scramble = "R2 B2 D' B2 D2 L2 B' L2 F' U2 F2 U2 L2 R F2 D' L' B D' B2"
        self.cube333_2.faces['white'] = [['yellow', 'blue', 'white'],
                                         ['yellow', 'white', 'green'],
                                         ['blue', 'orange', 'white']]
        self.cube333_2.faces['orange'] = [['orange', 'green', 'orange'],
                                          ['white', 'orange', 'blue'],
                                          ['red', 'yellow', 'orange']]
        self.cube333_2.faces['green'] = [['white', 'green', 'red'],
                                         ['red', 'green', 'blue'],
                                         ['white', 'green', 'red']]
        self.cube333_2.faces['red'] = [['blue', 'white', 'green'], 
                                       ['orange', 'red', 'white'],
                                       ['yellow', 'white', 'blue']]
        self.cube333_2.faces['blue'] = [['red', 'yellow', 'green'],
                                        ['red', 'blue', 'orange'],
                                        ['orange', 'yellow', 'yellow']]
        self.cube333_2.faces['yellow'] = [['green', 'red', 'green'],
                                          ['orange', 'yellow', 'blue'],
                                          ['blue', 'red', 'yellow']]

        self.cube222_1 = Cube(size=2)
        self.cube222_1_scramble = "F R U R' F U' F U' F R U'"
        self.cube222_1.faces['white'] = [['blue', 'orange'],
                                         ['red', 'blue']]
        self.cube222_1.faces['orange'] = [['red', 'white'],
                                          ['orange', 'green']]
        self.cube222_1.faces['green'] = [['green', 'orange'],
                                         ['red', 'yellow']]
        self.cube222_1.faces['red'] = [['white', 'green'], 
                                       ['red', 'green']]
        self.cube222_1.faces['blue'] = [['white', 'white'],
                                        ['yellow', 'blue']]
        self.cube222_1.faces['yellow'] = [['yellow', 'blue'],
                                          ['yellow', 'orange']]

        self.cube222_2 = Cube(size=2)
        self.cube222_2_scramble = "U' R U2 R2 F R U' R' F' U R"
        self.cube222_2.faces['white'] = [['green', 'red'],
                                         ['green', 'orange']]
        self.cube222_2.faces['orange'] = [['white', 'orange'],
                                          ['orange', 'green']]
        self.cube222_2.faces['green'] = [['yellow', 'white'],
                                         ['red', 'white']]
        self.cube222_2.faces['red'] = [['blue', 'yellow'], 
                                       ['blue', 'orange']]
        self.cube222_2.faces['blue'] = [['blue', 'red'],
                                        ['white', 'blue']]
        self.cube222_2.faces['yellow'] = [['yellow', 'red'],
                                          ['yellow', 'green']]

    def test_cube_creation(self):
        for i in range(2, 8):
            sample = Cube(size=i)
            for face in sample.faces:
                row = [face] * i
                test_face = [row] * i
                self.assertEqual(sample.faces[face], test_face)

    def test_cube_scramble_333(self):
        self._test_scramble(self.cube333_1, self.cube333_1_scramble)
        self._test_scramble(self.cube333_2, self.cube333_2_scramble)

    def test_cube_scramble_222(self):
        self._test_scramble(self.cube222_1, self.cube222_1_scramble)
        self._test_scramble(self.cube222_2, self.cube222_2_scramble)

    def _test_scramble(self, cube, scramble):
        sample = Cube(size=cube.size)
        sample.scrambleCube(scramble)
        for face in sample.faces:
            self.assertEqual(sample.faces[face], cube.faces[face])

if __name__ == '__main__':
    unittest.main()
