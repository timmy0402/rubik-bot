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

def rotate_face(cube, face, clockwise, extra_layer):
    if face == "U":
        # Collect rows to be rotated (for U face, row 0)
        if extra_layer == 0: # For bigger cube
            rows = [cube.faces['red'][0], cube.faces['blue'][0], cube.faces['orange'][0], cube.faces['green'][0]]
        else:
            rows = [
                [cube.faces['red'][i], cube.faces['blue'][i], cube.faces['orange'][i], cube.faces['green'][i]]
                for i in range(extra_layer + 1)]
        if clockwise: #Clockwise
            # Clockwise 90-degree rotation
            cube.faces['white'] = rotate_90_clockwise(cube.faces['white'])
            if extra_layer > 0:
                for i in range(len(rows)):
                    cube.faces['red'][i], cube.faces['blue'][i], cube.faces['orange'][i], cube.faces['green'][i] = \
                    rows[i][1], rows[i][2], rows[i][3], rows[i][0]
            else:
                cube.faces['red'][0], cube.faces['blue'][0], cube.faces['orange'][0], cube.faces['green'][0] = \
                rows[1], rows[2], rows[3], rows[0]
            
        else: #CounterClockwise
            cube.faces['white'] = rotate_90_counterClockwise(cube.faces['white'])
            if extra_layer > 0:
                for i in range(len(rows)):
                    cube.faces['red'][i], cube.faces['blue'][i], cube.faces['orange'][i], cube.faces['green'][i] = \
                    rows[i][-1], rows[i][0], rows[i][1], rows[i][2]
            else:
                cube.faces['red'][0], cube.faces['blue'][0], cube.faces['orange'][0], cube.faces['green'][0] = \
                rows[-1], rows[0], rows[1], rows[2]
            
    elif face == "D":
        # Collect rows to be rotated (for D face, row 2)
        if extra_layer == 0: # For bigger cube
            rows = [cube.faces['green'][cube.size-1], cube.faces['orange'][cube.size-1], cube.faces['blue'][cube.size-1], cube.faces['red'][cube.size-1]]
        else:
            rows = [
                [cube.faces['green'][cube.size-1-i], cube.faces['orange'][cube.size-1-i], cube.faces['blue'][cube.size-1-i], cube.faces['red'][cube.size-1-i]]
                for i in range(extra_layer + 1)]
        if clockwise: # Clockwise
            cube.faces['yellow'] = rotate_90_clockwise(cube.faces['yellow'])
            if extra_layer > 0:
                for i in range(len(rows)):
                    cube.faces['green'][cube.size-1-i], cube.faces['orange'][cube.size-1-i], cube.faces['blue'][cube.size-1-i], cube.faces['red'][cube.size-1-i] = \
                    rows[i][1], rows[i][2], rows[i][3], rows[i][0]
            else:
                cube.faces['green'][cube.size-1], cube.faces['orange'][cube.size-1], cube.faces['blue'][cube.size-1], cube.faces['red'][cube.size-1] = \
                rows[1], rows[2], rows[3], rows[0]
        else: # CounterClockwise
            cube.faces['yellow'] = rotate_90_counterClockwise(cube.faces['yellow'])
            if extra_layer > 0:
                for i in range(len(rows)):
                    cube.faces['green'][cube.size-1-i], cube.faces['orange'][cube.size-1-i], cube.faces['blue'][cube.size-1-i], cube.faces['red'][cube.size-1-i] = \
                        rows[i][-1], rows[i][0], rows[i][1], rows[i][2]
            else:
                cube.faces['green'][2], cube.faces['orange'][2], cube.faces['blue'][2], cube.faces['red'][2] = \
                    rows[-1], rows[0], rows[1], rows[2]
            
    if face == "R":
        if clockwise:
            cube.faces['red'] = rotate_90_clockwise(cube.faces['red'])
            # Temporary storage for the right column of the green face
            temp = [cube.faces['green'][i][cube.size - 1] for i in range(cube.size)]
            
            for i in range(cube.size):
                cube.faces['green'][i][cube.size - 1] = cube.faces['yellow'][i][cube.size - 1]
                cube.faces['yellow'][i][cube.size - 1] = cube.faces['blue'][cube.size - 1 - i][0]
                cube.faces['blue'][cube.size - 1 - i][0] = cube.faces['white'][i][cube.size - 1]
            for i in range(cube.size):
                cube.faces['white'][i][cube.size - 1] = temp[i]

        else:
            cube.faces['red'] = rotate_90_counterClockwise(cube.faces['red'])
            # Counterclockwise rotation: reverse the order of rotations
            temp = [cube.faces['green'][i][cube.size - 1] for i in range(cube.size)]
            
            for i in range(cube.size):
                cube.faces['green'][i][cube.size - 1] = cube.faces['white'][i][cube.size - 1]
                cube.faces['white'][i][cube.size - 1] = cube.faces['blue'][cube.size - 1 - i][0]
                cube.faces['blue'][cube.size - 1 - i][0] = cube.faces['yellow'][i][cube.size - 1]
            for i in range(cube.size):
                cube.faces['yellow'][i][cube.size - 1] = temp[i]
            
    if face == "L":
        if clockwise:
            cube.faces['orange'] = rotate_90_clockwise(cube.faces['orange'])
            # Temporary storage for the right column of the green face
            temp = [cube.faces['green'][i][0] for i in range(cube.size)]

            for i in range(cube.size):
                cube.faces['green'][i][0] = cube.faces['white'][i][0]
                cube.faces['white'][i][0] = cube.faces['blue'][cube.size - 1 - i][cube.size - 1]
                cube.faces['blue'][cube.size - 1 - i][cube.size - 1] = cube.faces['yellow'][i][0]               
            for i in range(cube.size):
                cube.faces['yellow'][i][0] = temp[i]
        else:
            cube.faces['orange'] = rotate_90_counterClockwise(cube.faces['orange'])
            # Counterclockwise rotation: reverse the order of rotations
            temp = [cube.faces['green'][i][0] for i in range(cube.size)]
            
            for i in range(cube.size):
                cube.faces['green'][i][0] = cube.faces['yellow'][i][0]
                cube.faces['yellow'][i][0] = cube.faces['blue'][cube.size - 1 - i][cube.size - 1]
                cube.faces['blue'][cube.size - 1 - i][cube.size - 1] = cube.faces['white'][i][0]
            for i in range(cube.size):
                cube.faces['white'][i][0] = temp[i]
            
    if face == "F":
        if clockwise:
            cube.faces['green'] = rotate_90_clockwise(cube.faces['green'])
            # Temporary storage for the bottom row of the U (Upper) face
            temp = [cube.faces['white'][cube.size - 1][i] for i in range(cube.size)]
            
            for i in range(cube.size):
                cube.faces['white'][cube.size - 1][i] = cube.faces['orange'][cube.size - 1 - i][cube.size - 1]  
                cube.faces['orange'][cube.size - 1 - i][cube.size - 1] = cube.faces['yellow'][0][cube.size - 1 - i] 
                cube.faces['yellow'][0][cube.size - 1 - i] = cube.faces['red'][i][0]
            for i in range(cube.size):
                cube.faces['red'][i][0] = temp[i]    
        else:
            cube.faces['green'] = rotate_90_counterClockwise(cube.faces['green'])
            # Temporary storage for the bottom row of the U (Upper) face
            temp = cube.faces['white'][cube.size - 1][:]

            for i in range(cube.size):
                cube.faces['white'][cube.size - 1][i] = cube.faces['red'][i][0]  
                cube.faces['red'][i][0] = cube.faces['yellow'][0][cube.size - 1 - i]  
                cube.faces['yellow'][0][cube.size - 1 - i] = cube.faces['orange'][cube.size - 1 - i][cube.size - 1]  
            for i in range(cube.size):
                cube.faces['orange'][cube.size - 1 - i][cube.size - 1] = temp[i]  
    if face == "B":
        if clockwise:
            cube.faces['blue'] = rotate_90_clockwise(cube.faces['blue'])
            # Temporary storage for the bottom row of the U (Upper) face
            temp = cube.faces['white'][0][:]

            for i in range(cube.size):
                cube.faces['white'][0][i] = cube.faces['red'][i][cube.size - 1]
                cube.faces['red'][i][cube.size - 1] = cube.faces['yellow'][cube.size - 1][cube.size - 1 - i]
                cube.faces['yellow'][cube.size - 1][cube.size - 1 - i] = cube.faces['orange'][cube.size - 1 - i][0]
            for i in range(cube.size):
                cube.faces['orange'][i][0] = temp[cube.size - 1 - i]
        else:
            cube.faces['blue'] = rotate_90_counterClockwise(cube.faces['blue'])
            # Temporary storage for the bottom row of the U (Upper) face
            temp = cube.faces['white'][0][:]

            for i in range(cube.size):
                cube.faces['white'][0][i] = cube.faces['orange'][cube.size - 1 - i][0]
                cube.faces['orange'][cube.size - 1 - i][0] = cube.faces['yellow'][cube.size - 1][cube.size - 1 - i]
                cube.faces['yellow'][cube.size - 1][cube.size - 1 - i] = cube.faces['red'][i][cube.size - 1]
            for i in range(cube.size):
                cube.faces['red'][i][2] = temp[i]