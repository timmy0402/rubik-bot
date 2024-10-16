import unittest
import sys
sys.path.insert(0,'../src')

from cube import Cube

cube333_1 = Cube(size=3)
cube333_1.faces['white'] = [['green','blue','red'],['blue','white','white'],['blue','yellow','yellow']]
cube333_1.faces['orange'] = [['red','white','red'],['red','orange','orange'],['white','orange','yellow']]
cube333_1.faces['green'] = [['yellow','blue','orange'],['white','green','red'],['orange','orange','green']]
#cube333_1.faces['red'] = [['yellow','blue','orange'],['white','green','red'],['orange','orange','green']]

class TestCubeMethod(unittest.TestCase):
    def test_cube_creation(self):
        for i in range(2,8):
            sample = Cube(size=i)
            for face in sample.faces:
                row = [face] * i
                test_face = [row] * i
                self.assertEqual(sample.faces[face],test_face)
    def test_cube_scramble333(self):
        
if __name__ == '__main__':
    unittest.main()