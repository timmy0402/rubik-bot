from PIL import Image,ImageDraw
class Cube():
    def __init__(self,size = 3):
        self.size = size
    
    # Initialize each face of the cube using a dictionary
        self.faces = {
            'white': self.__createFace('white'),
            'green': self.__createFace('green'),
            'red': self.__createFace('red'),
            'blue': self.__createFace('blue'),
            'yellow': self.__createFace('yellow'),
            'orange': self.__createFace('orange')
        }


    def __createFace(self,color):
        return [[color for _ in range(self.size)] for _ in range(self.size)]
    
    def scrambleCube(self, scrambleLine : str):
        commandList = scrambleLine.split()
        for command in commandList:
            match command:
                case "U":
                    self.__rotate_face("U", clockwise=True)
                case "U'":
                    self.__rotate_face("U", clockwise=False)
                case "U2":
                    self.__rotate_face("U", clockwise=True)
                    self.__rotate_face("U", clockwise=True)
                case "D":
                    self.__rotate_face("D", clockwise=True)
                case "D'":
                    self.__rotate_face("D", clockwise=False)
                case "D2":
                    self.__rotate_face("D", clockwise=True)
                    self.__rotate_face("D", clockwise=True)

    def __rotate_face(self, face, clockwise=True):
        if face == "U":
            if clockwise:
                temp = self.faces['red'][0]
                self.faces['red'][0] = self.faces['blue'][0]
                self.faces['blue'][0] = self.faces['orange'][0]
                self.faces['orange'][0] = self.faces['green'][0]
                self.faces['green'][0] = temp
            else:
                temp = self.faces['green'][0]
                self.faces['green'][0] = self.faces['orange'][0]
                self.faces['orange'][0] = self.faces['blue'][0]
                self.faces['blue'][0] = self.faces['red'][0]
                self.faces['red'][0] = temp
        if face == "D":
            if clockwise:
                temp = self.faces['green'][2]
                self.faces['green'][2] = self.faces['orange'][2]
                self.faces['orange'][2] = self.faces['blue'][2]
                self.faces['blue'][2] = self.faces['red'][2]
                self.faces['red'][2] = temp
            else:
                temp = self.faces['red'][2]
                self.faces['red'][2] = self.faces['blue'][2]
                self.faces['blue'][2] = self.faces['orange'][2]
                self.faces['orange'][2] = self.faces['green'][2]
                self.faces['green'][2] = temp
            return 0
        return 0

    # Function to draw the Rubik's cube image
    def draw_rubiks_cube(self):
        # Color map for visualization
        color_map = {
            'white': (255, 255, 255),
            'green': (0, 255, 0),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'orange': (255, 165, 0)
        }

        # Set size for each small square
        block_size = 50
        gap = 5  # Gap between faces for better visual separation
        border_thickness = 5  # Thickness of the border

        # Image layout configuration for 6 faces
        # Image dimensions
        img_width = block_size * 12  # 12 blocks wide (for four faces in a row)
        img_height = block_size * 9  # 9 blocks high (including gaps)

        # Create a new blank image with white background
        img = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(img)

        # Coordinates for placing each face in the layout
        layout_positions = {
            'white': (block_size * 6, 0),               # Top (above green)
            'blue': (0, block_size * 3),                # Left of green
            'red': (block_size * 9, block_size * 3),    # Center (left of green)
            'green': (block_size * 6, block_size * 3),  # Center (main face)
            'orange': (block_size * 3, block_size * 3), # Right of green
            'yellow': (block_size * 6, block_size * 6)  # Bottom (below green)
        }

        # Function to draw a single face of the cube
        def draw_face(face, start_x, start_y):
            for row in range(self.size):
                for col in range(self.size):
                    x0 = start_x + col * block_size
                    y0 = start_y + row * block_size
                    x1 = x0 + block_size
                    y1 = y0 + block_size
                    color = self.faces[face][row][col]
                    draw.rectangle([x0, y0, x1, y1], fill=color_map[color], outline="black",width=border_thickness)

        # Draw each face using the layout positions
        for face, (start_x, start_y) in layout_positions.items():
            draw_face(face, start_x, start_y)

        # Save or show the image
        img.show()  # Display the image
        # img.save("rubiks_cube.png")  # Save the image if needed

# Create a 3x3 Rubik's Cube
rubik_cube = Cube(size=3)

rubik_cube.scrambleCube("D D' D' D2")
# Draw the cube's image
rubik_cube.draw_rubiks_cube()

