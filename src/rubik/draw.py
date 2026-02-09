from PIL import Image, ImageDraw
from io import BytesIO


def draw_rubiks_cube(rubik):
    """
    Generates a 2D net representation of the Rubik's Cube as a PNG image.

    Args:
        rubik (Cube): The Cube instance containing the current face states.

    Returns:
        BytesIO: A binary stream containing the generated PNG image.
    """
    cube_size = rubik.size

    # Map color names to RGB tuples for Pillow drawing
    color_map = {
        "white": (255, 255, 255),
        "green": (0, 255, 0),
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
    }

    # Drawing configuration parameters
    total_size = 150
    block_size = int(total_size / cube_size)
    gap = 5
    border_thickness = 5

    # Calculate image dimensions based on cube size and gaps
    img_width = block_size * cube_size * 4 + gap * 3
    img_height = block_size * cube_size * 3 + gap * 2

    # Create a new white canvas
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Define the 2D layout positions for each face in the net
    layout_positions = {
        "white": (block_size * cube_size + gap, 0),
        "blue": (block_size * cube_size * 3 + gap * 3, block_size * cube_size + gap),
        "red": (block_size * cube_size * 2 + gap * 2, block_size * cube_size + gap),
        "green": (block_size * cube_size + gap, block_size * cube_size + gap),
        "orange": (0, block_size * cube_size + gap),
        "yellow": (block_size * cube_size + gap, block_size * cube_size * 2 + gap * 2),
    }

    def draw_face(face, start_x, start_y):
        """
        Draws an individual face on the canvas at the specified coordinates.
        """
        for row in range(cube_size):
            for col in range(cube_size):
                x0 = start_x + col * block_size
                y0 = start_y + row * block_size
                x1 = x0 + block_size
                y1 = y0 + block_size
                color = rubik.faces[face][row][col]
                draw.rectangle(
                    [x0, y0, x1, y1],
                    fill=color_map[color],
                    outline="black",
                    width=border_thickness,
                )

    # Draw all faces of the cube
    for face, (start_x, start_y) in layout_positions.items():
        draw_face(face, start_x, start_y)

    # Save the final image to a bytes buffer
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes