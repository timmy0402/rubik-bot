import unittest
import sys
sys.path.insert(0,'../src')

from cube import Cube

cube333_1 = Cube(size=3)
cube333_1_scramble = "U2 D F D' B2 R2 F2 L U' F' D' L2 D' R2 F2 U B2 U2 L"
cube333_1.faces['white'] = [['green','blue','red'],['blue','white','white'],['blue','yellow','yellow']]
cube333_1.faces['orange'] = [['red','white','red'],['red','orange','orange'],['white','orange','yellow']]
cube333_1.faces['green'] = [['yellow','blue','orange'],['white','green','red'],['orange','orange','green']]
cube333_1.faces['red'] = [['white','green','blue'],['green','red','blue'],['orange','green','blue']]
cube333_1.faces['blue'] = [['white','orange','yellow'],['red','blue','yellow'],['white','white','green']]
cube333_1.faces['yellow'] = [['green','yellow','white'],['green','yellow','yellow'],['red','red','orange']]

class TestCubeMethod(unittest.TestCase):
    def test_cube_creation(self):
        for i in range(2,8):
            sample = Cube(size=i)
            for face in sample.faces:
                row = [face] * i
                test_face = [row] * i
                self.assertEqual(sample.faces[face],test_face)
    def test_cube_scramble333(self):
        sample = Cube(size=3)
        sample.scrambleCube(cube333_1_scramble)
        for face in sample.faces:
            print(sample.faces[face])
            print(cube333_1.faces[face])
            #self.assertEqual(sample.faces[face],cube333_1.faces[face])

if __name__ == '__main__':
    unittest.main()