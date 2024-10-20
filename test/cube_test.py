import unittest
import sys

sys.path.insert(0,'../src')

from cube import Cube

class TestCubeMethod(unittest.TestCase):

    def setUp(self):
        self.cube333_1 = Cube(size=3)
        self.cube333_1_scramble = "U2 D F D' B2 R2 F2 L U' F' D' L2 D' R2 F2 U B2 U2 L'"
        self.cube333_1.faces['white'] = [['green','blue','red'],
                                         ['blue','white','white'],
                                         ['blue','yellow','yellow']]
        self.cube333_1.faces['orange'] = [['red','white','red'],
                                          ['red','orange','orange'],
                                          ['white','orange','yellow']]
        self.cube333_1.faces['green'] = [['yellow','blue','orange'],
                                         ['white','green','red'],
                                         ['orange','orange','green']]
        self.cube333_1.faces['red'] = [['blue','green','blue'], 
                                       ['green','red','blue'],
                                       ['orange','green','blue']]
        self.cube333_1.faces['blue'] = [['white','orange','yellow'],
                                        ['red','blue','yellow'],
                                        ['white','white','green']]
        self.cube333_1.faces['yellow'] = [['green','yellow','white'],
                                          ['green','yellow','yellow'],
                                          ['red','red','orange']]

        self.cube333_2 = Cube(size=3)
        self.cube333_2_scramble = "R2 B2 D' B2 D2 L2 B' L2 F' U2 F2 U2 L2 R F2 D' L' B D' B2"
        self.cube333_2.faces['white'] = [['yellow','blue','white'],
                                         ['yellow','white','green'],
                                         ['blue','orange','white']]
        self.cube333_2.faces['orange'] = [['orange','green','orange'],
                                          ['white','orange','blue'],
                                          ['red','yellow','orange']]
        self.cube333_2.faces['green'] = [['white','green','red'],
                                         ['red','green','blue'],
                                         ['white','green','red']]
        self.cube333_2.faces['red'] = [['blue','white','green'], 
                                       ['orange','red','white'],
                                       ['yellow','white','blue']]
        self.cube333_2.faces['blue'] = [['red','yellow','green'],
                                        ['red','blue','orange'],
                                        ['orange','yellow','yellow']]
        self.cube333_2.faces['yellow'] = [['green','red','green'],
                                          ['orange','yellow','blue'],
                                          ['blue','red','yellow']]

        self.cube222_1 = Cube(size=2)
        self.cube222_1_scramble = "F R U R' F U' F U' F R U'"
        self.cube222_1.faces['white'] = [['blue','orange'],
                                         ['red','blue']]
        self.cube222_1.faces['orange'] = [['red','white'],
                                          ['orange','green']]
        self.cube222_1.faces['green'] = [['green','orange'],
                                         ['red','yellow']]
        self.cube222_1.faces['red'] = [['white','green'], 
                                       ['red','green']]
        self.cube222_1.faces['blue'] = [['white','white'],
                                        ['yellow','blue']]
        self.cube222_1.faces['yellow'] = [['yellow','blue'],
                                          ['yellow','orange']]

        self.cube222_2 = Cube(size=2)
        self.cube222_2_scramble = "U' R U2 R2 F R U' R' F' U R"
        self.cube222_2.faces['white'] = [['green','red'],
                                         ['green','orange']]
        self.cube222_2.faces['orange'] = [['white','orange'],
                                          ['orange','green']]
        self.cube222_2.faces['green'] = [['yellow','white'],
                                         ['red','white']]
        self.cube222_2.faces['red'] = [['blue','yellow'], 
                                       ['blue','orange']]
        self.cube222_2.faces['blue'] = [['blue','red'],
                                        ['white','blue']]
        self.cube222_2.faces['yellow'] = [['yellow','red'],
                                          ['yellow','green']]
        
        self.cube444_1 = Cube(size=4)
        self.cube444_1_scramble = "L' U' L' R' F L2 F' R2 D F2 D' U' R2 D R2 B2 L2 F' L Rw2 B' R2 L' D2 " \
                                    "B U2 Rw2 Fw2 F2 L' B' Uw' R' Uw2 B2 U' Fw R' L' Uw' U Rw2 F"
        self.cube444_1.faces['white'] = [['red','white','red','orange'],
                                         ['orange','yellow','blue','orange'],
                                         ['blue','orange','white','green'],
                                         ['red','red','red','green']]
        self.cube444_1.faces['orange'] = [['yellow','green','orange','white'],
                                          ['white','blue','blue','green'],
                                          ['white','green','orange','blue'],
                                          ['red','white','yellow','orange']]
        self.cube444_1.faces['green'] = [['green','white','white','white'],
                                         ['yellow','green','yellow','blue'],
                                         ['yellow','blue','red','white'],
                                         ['green','green','red','blue']]
        self.cube444_1.faces['red'] = [['orange','orange','yellow','white'], 
                                       ['red','white','white','yellow'],
                                       ['orange','orange','green','blue'],
                                       ['orange','yellow','yellow','blue']]
        self.cube444_1.faces['blue'] = [['blue','green','blue','green'],
                                        ['orange','red','orange','green'],
                                        ['orange','yellow','red','green'],
                                        ['yellow','yellow','white','blue']]
        self.cube444_1.faces['yellow'] = [['yellow','red','blue','yellow'],
                                          ['red','green','yellow','red'],
                                          ['blue','white','red','green'],
                                          ['white','orange','blue','red']]

        self.cube444_2 = Cube(size=4)
        self.cube444_2_scramble = "L' F' L2 U' L2 D L2 U' R2 D L2 D2 R B D2 F U2 R D2 F Fw2 Rw2 L D2 " \
                                    "L2 Uw2 L B2 Rw2 B F2 R Fw2 D' B2 L' Uw B2 Rw' F2 Uw' R2 Fw2 Rw' B' L2"
        self.cube444_2.faces['white'] = [['yellow','white','blue','white'],
                                         ['green','red','white','yellow'],
                                         ['orange','orange','green','red'],
                                         ['blue','orange','red','yellow']]
        self.cube444_2.faces['orange'] = [['green','red','yellow','white'],
                                          ['blue','red','orange','white'],
                                          ['blue','green','white','orange'],
                                          ['white','red','blue','blue']]
        self.cube444_2.faces['green'] = [['red','blue','blue','blue'],
                                         ['orange','orange','blue','orange'],
                                         ['green','blue','white','orange'],
                                         ['orange','white','green','orange']]
        self.cube444_2.faces['red'] = [['red','green','green','blue'], 
                                       ['white','green','yellow','green'],
                                       ['yellow','orange','blue','green'],
                                       ['green','green','white','green']]
        self.cube444_2.faces['blue'] = [['orange','orange','blue','red'],
                                        ['white','red','red','yellow'],
                                        ['white','blue','yellow','white'],
                                        ['white','red','red','orange']]
        self.cube444_2.faces['yellow'] = [['yellow','red','yellow','yellow'],
                                          ['yellow','yellow','yellow','orange'],
                                          ['yellow','white','green','red'],
                                          ['green','yellow','blue','red']]
        
        self.cube555_1 = Cube(size=5)
        self.cube555_1_scramble = "F Bw' R' Uw F' B Bw2 Rw' Fw Uw' Bw2 B2 D2 Dw Bw2 F L2 Fw' R2 Fw2 Uw2 R' " \
                                "Uw F' L' Bw2 Lw' L2 U' Lw D' R U D2 L' Fw' F R2 B Uw2 Dw2 F2 Dw U F' U2 Uw' " \
                                "Lw2 Bw Uw' Fw' Bw' Dw Bw D2 Dw Fw2 U F2 L'"
        self.cube555_1.faces['white'] = [['orange','green','green','yellow','red'],
                                         ['white','red','blue','yellow','yellow'],
                                         ['white','yellow','white','red','red'],
                                         ['white','white','white','red','white'],
                                         ['yellow','white','white','yellow','yellow']]
        self.cube555_1.faces['orange'] = [['white','green','red','red','red'],
                                          ['blue','red','white','white','orange'],
                                          ['green','orange','orange','blue','yellow'],
                                          ['yellow','blue','yellow','orange','orange'],
                                          ['yellow','blue','white','white','red']]
        self.cube555_1.faces['green'] = [['green','blue','green','orange','green'],
                                         ['blue','yellow','blue','green','blue'],
                                         ['orange','green','green','green','orange'],
                                         ['white','red','blue','white','yellow'],
                                         ['white','red','orange','red','blue']]
        self.cube555_1.faces['red'] = [['orange','red','blue','red','yellow'], 
                                       ['orange','green','red','orange','orange'],
                                       ['blue','red','red','orange','yellow'],
                                       ['red','orange','green','orange','green'],
                                       ['white','yellow','white','orange','red']]
        self.cube555_1.faces['blue'] = [['blue','blue','yellow','orange','green'],
                                        ['white','green','white','blue','white'],
                                        ['red','yellow','blue','white','red'],
                                        ['red','green','yellow','blue','green'],
                                        ['green','red','blue','orange','orange']]
        self.cube555_1.faces['yellow'] = [['blue','green','green','blue','orange'],
                                          ['green','white','orange','yellow','green'],
                                          ['blue','green','yellow','red','orange'],
                                          ['yellow','blue','orange','yellow','green'],
                                          ['blue','yellow','yellow','blue','white']]

        self.cube555_2 = Cube(size=5)
        self.cube555_2_scramble = "F2 U' Rw' D Bw Lw B' U2 F Fw2 Bw2 U Dw2 Bw2 L' Lw' Bw R Fw' Rw2 Fw R2 Fw2 Uw2 " \
                                "Dw2 F L Dw R2 U' Lw' F' B2 Lw' B' Uw2 B' U R' Rw Lw Bw' L' U2 L2 U Rw' Bw Lw' U2 " \
                                "Bw' Rw Lw Fw2 D U F Dw F' Dw"
        self.cube555_2.faces['white'] = [['white','yellow','red','white','blue'],
                                         ['yellow','yellow','white','red','red'],
                                         ['white','orange','white','blue','yellow'],
                                         ['white','green','green','green','orange'],
                                         ['red','yellow','blue','blue','yellow']]
        self.cube555_2.faces['orange'] = [['blue','red','red','red','white'],
                                          ['green','green','blue','orange','orange'],
                                          ['yellow','white','orange','orange','yellow'],
                                          ['green','white','red','white','green'],
                                          ['green','yellow','white','yellow','red']]
        self.cube555_2.faces['green'] = [['green','green','white','yellow','orange'],
                                         ['green','white','blue','blue','white'],
                                         ['blue','red','green','yellow','green'],
                                         ['red','yellow','green','blue','blue'],
                                         ['yellow','blue','yellow','yellow','blue']]
        self.cube555_2.faces['red'] = [['blue','blue','red','white','red'], 
                                       ['orange','white','white','yellow','green'],
                                       ['red','orange','red','green','green'],
                                       ['red','red','yellow','green','green'],
                                       ['white','white','blue','white','yellow']]
        self.cube555_2.faces['blue'] = [['yellow','orange','blue','red','red'],
                                        ['orange','blue','red','red','yellow'],
                                        ['orange','green','blue','yellow','green'],
                                        ['white','yellow','blue','blue','red'],
                                        ['orange','white','orange','blue','white']]
        self.cube555_2.faces['yellow'] = [['green','orange','orange','blue','orange'],
                                          ['orange','orange','yellow','orange','blue'],
                                          ['green','red','yellow','orange','orange'],
                                          ['orange','orange','white','red','blue'],
                                          ['orange','red','white','green','green']]


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

    def test_cube_scramble_444(self):
        self._test_scramble(self.cube444_1, self.cube444_1_scramble)
        self._test_scramble(self.cube444_2, self.cube444_2_scramble)
    
    def test_cube_scramble_555(self):
        self._test_scramble(self.cube555_1, self.cube555_1_scramble)
        self._test_scramble(self.cube555_2, self.cube555_2_scramble)
        
    def _test_scramble(self, cube, scramble):
        sample = Cube(size=cube.size)
        sample.scrambleCube(scramble)
        for face in sample.faces:
            self.assertEqual(sample.faces[face], cube.faces[face])

if __name__ == '__main__':
    unittest.main()
