def rotate_90_counterClockwise(face):
    # Transpose
    transpose = [[face[row][col] for row in range(len(face))] for col in range(len(face[0]))]
    # Reverse each col
    rotated = transpose[::-1]
    return rotated

def rotate_90_clockwise(face):
    # Transpose 
    transpose = [[face[row][col] for row in range(len(face))] for col in range(len(face[0]))]
    # Reverse each row
    rotated = [row[::-1] for row in transpose]
    return rotated

def rotate_face(cube, face, clockwise=True):
    if face == "U":
        # Collect rows to be rotated (for U face, row 0)
        rows = [cube.faces['red'][0], cube.faces['blue'][0], cube.faces['orange'][0], cube.faces['green'][0]]
        
        if clockwise:
            # Clockwise 90-degree rotation
            cube.faces['white'] = rotate_90_clockwise(cube.faces['white'])
            # Clockwise: Rotate the rows to the right
            cube.faces['red'][0], cube.faces['blue'][0], cube.faces['orange'][0], cube.faces['green'][0] = \
                rows[1], rows[2], rows[3], rows[0]
        else:
            cube.faces['white'] = rotate_90_counterClockwise(cube.faces['white'])
            # Counterclockwise: Rotate the rows to the left
            cube.faces['red'][0], cube.faces['blue'][0], cube.faces['orange'][0], cube.faces['green'][0] = \
                rows[-1], rows[0], rows[1], rows[2]
            
    elif face == "D":
        # Collect rows to be rotated (for D face, row 2)
        rows = [cube.faces['green'][2], cube.faces['orange'][2], cube.faces['blue'][2], cube.faces['red'][2]]
        
        if clockwise:
            cube.faces['yellow'] = rotate_90_clockwise(cube.faces['yellow'])

            # Clockwise: Rotate the rows to the right
            cube.faces['green'][2], cube.faces['orange'][2], cube.faces['blue'][2], cube.faces['red'][2] = \
                rows[1], rows[2], rows[3], rows[0]
        else:
            cube.faces['yellow'] = rotate_90_counterClockwise(cube.faces['yellow'])
            # Counterclockwise: Rotate the rows to the left
            cube.faces['green'][2], cube.faces['orange'][2], cube.faces['blue'][2], cube.faces['red'][2] = \
                rows[-1], rows[0], rows[1], rows[2]
            
    if face == "R":
        if clockwise:
            cube.faces['red'] = rotate_90_clockwise(cube.faces['red'])
            # Temporary storage for the right column of the green face
            temp = [cube.faces['green'][i][2] for i in range(3)]
            
            for i in range(3):
                cube.faces['green'][i][2] = cube.faces['yellow'][i][2]
                cube.faces['yellow'][i][2] = cube.faces['blue'][2-i][0]
                cube.faces['blue'][2-i][0] = cube.faces['white'][i][2]
            for i in range(3):
                cube.faces['white'][i][2] = temp[i]

        else:
            cube.faces['red'] = rotate_90_counterClockwise(cube.faces['red'])
            # Counterclockwise rotation: reverse the order of rotations
            temp = [cube.faces['green'][i][2] for i in range(3)]
            
            for i in range(3):
                cube.faces['green'][i][2] = cube.faces['white'][i][2]
                cube.faces['white'][i][2] = cube.faces['blue'][2-i][0]
                cube.faces['blue'][2-i][0] = cube.faces['yellow'][i][2]
            for i in range(3):
                cube.faces['yellow'][i][2] = temp[i]
            
    if face == "L":
        if clockwise:
            cube.faces['orange'] = rotate_90_clockwise(cube.faces['orange'])
            # Temporary storage for the right column of the green face
            temp = [cube.faces['green'][i][0] for i in range(3)]

            for i in range(3):
                cube.faces['green'][i][0] = cube.faces['white'][i][0]
                cube.faces['white'][i][0] = cube.faces['blue'][2-i][2]
                cube.faces['blue'][2-i][2] = cube.faces['yellow'][i][0]               
            for i in range(3):
                cube.faces['yellow'][i][0] = temp[i]
        else:
            cube.faces['orange'] = rotate_90_counterClockwise(cube.faces['orange'])
            # Counterclockwise rotation: reverse the order of rotations
            temp = [cube.faces['green'][i][0] for i in range(3)]
            
            for i in range(3):
                cube.faces['green'][i][0] = cube.faces['yellow'][i][0]
                cube.faces['yellow'][i][0] = cube.faces['blue'][2-i][2]
                cube.faces['blue'][2-i][2] = cube.faces['white'][i][0]
            for i in range(3):
                cube.faces['white'][i][0] = temp[i]
            
    if face == "F":
        if clockwise:
            cube.faces['green'] = rotate_90_clockwise(cube.faces['green'])
            # Temporary storage for the bottom row of the U (Upper) face
            temp = [cube.faces['white'][2][i] for i in range(3)]
            
            for i in range(3):
                cube.faces['white'][2][i] = cube.faces['orange'][2 - i][2]  
                cube.faces['orange'][2 - i][2] = cube.faces['yellow'][0][2 - i] 
                cube.faces['yellow'][0][2 - i] = cube.faces['red'][i][0]
            for i in range(3):
                cube.faces['red'][i][0] = temp[i]    
        else:
            cube.faces['green'] = rotate_90_counterClockwise(cube.faces['green'])
            # Temporary storage for the bottom row of the U (Upper) face
            temp = cube.faces['white'][2][:]

            for i in range(3):
                cube.faces['white'][2][i] = cube.faces['red'][i][0]  
                cube.faces['red'][i][0] = cube.faces['yellow'][0][2 - i]  
                cube.faces['yellow'][0][2 - i] = cube.faces['orange'][2 - i][2]  
            for i in range(3):
                cube.faces['orange'][2 - i][2] = temp[i]  
    if face == "B":
        if clockwise:
            cube.faces['blue'] = rotate_90_clockwise(cube.faces['blue'])
            # Temporary storage for the bottom row of the U (Upper) face
            temp = cube.faces['white'][0][:]

            for i in range(3):
                cube.faces['white'][0][i] = cube.faces['red'][i][2]
                cube.faces['red'][i][2] = cube.faces['yellow'][2][2-i]
                cube.faces['yellow'][2][2-i] = cube.faces['orange'][2-i][0]
            for i in range(3):
                cube.faces['orange'][i][0] = temp[2-i]
        else:
            cube.faces['blue'] = rotate_90_counterClockwise(cube.faces['blue'])
            # Temporary storage for the bottom row of the U (Upper) face
            temp = cube.faces['white'][0][:]

            for i in range(3):
                cube.faces['white'][0][i] = cube.faces['orange'][2-i][0]
                cube.faces['orange'][2-i][0] = cube.faces['yellow'][2][2-i]
                cube.faces['yellow'][2][2-i] = cube.faces['red'][i][2]
            for i in range(3):
                cube.faces['red'][i][2] = temp[i]