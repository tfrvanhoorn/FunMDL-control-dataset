from PIL import Image, ImageDraw, ImageOps
import os

# Global Variables
NUM_TRAIN_SAMPLES_PER_CLASS = 200
NUM_TEST_SAMPLES_PER_CONDITION = 50
OUTPUT_DIR = "shape_texture_dataset"
IMG_SIZE = (128, 128)
TEXTURE_SCALE_FACTOR = 1
SHAPE_BOUNDARY_WIDTH = 2

# Helper function to ensure odd number 
def ensure_odd(value):
    return value + 1 if value % 2 == 0 else value

# Function to create texture images
def create_texture_image(texture_type, scale_factor):
    tex_img = Image.new("L", IMG_SIZE, "black")
    draw = ImageDraw.Draw(tex_img)

    # Define widhth and height of the image
    img_width, img_height = IMG_SIZE
    # Define center of the image
    img_center_x, img_center_y = img_width // 2, img_height // 2

    # Draw stripes texture if texture_type is "stripes"
    if texture_type == "stripes":
        base_stripe_width = 3
        base_stripe_spacing_total = 6

        # Apply scaling factor and ensure odd width for centering
        scaled_stripe_width = ensure_odd(max(1, int(base_stripe_width * scale_factor)))
        scaled_stripe_spacing_total = max(scaled_stripe_width + 1, int(base_stripe_spacing_total * scale_factor))
        
        # Calculate offset to center stripes
        num_stripes = img_width // scaled_stripe_spacing_total
        total_pattern_width = num_stripes * scaled_stripe_spacing_total
        start_offset = (img_width - total_pattern_width) // 2
        
        # Draw centered stripes with a white color
        for i in range(num_stripes + 1):
            x_coord = start_offset + (i * scaled_stripe_spacing_total)
            draw.line([(x_coord, 0), (x_coord, img_height)], fill="white", width=scaled_stripe_width)
    
    # Draw dots texture if texture_type is "dots"
    elif texture_type == "dots":
        base_dot_radius = 3
        base_dot_spacing = 10

        # Apply scaling factor and ensure odd diameter for centering
        scaled_dot_diameter = ensure_odd(max(2, int(2 * base_dot_radius * scale_factor)))
        scaled_dot_radius = scaled_dot_diameter // 2
        scaled_dot_spacing = max(scaled_dot_diameter + 1, int(base_dot_spacing * scale_factor))

        # Start from the center and calculate how many dots fit on each side
        dots_to_edge_x = (img_width // 2) // scaled_dot_spacing
        dots_to_edge_y = (img_height // 2) // scaled_dot_spacing
        
        # Calculate dots in both directions from center (including center dot)
        for i in range(-dots_to_edge_x, dots_to_edge_x + 1):
            for j in range(-dots_to_edge_y, dots_to_edge_y + 1):
                x_coord = img_center_x + (i * scaled_dot_spacing)
                y_coord = img_center_y + (j * scaled_dot_spacing)
                draw.ellipse(
                    [(x_coord - scaled_dot_radius, y_coord - scaled_dot_radius),
                     (x_coord + scaled_dot_radius, y_coord + scaled_dot_radius)],
                    fill="white"
                )
    # return the image containing the drawn texture
    return tex_img

# Function to generate images with shapes and textures
def generate_image(shape_type, texture_type_str, filename, texture_scale, boundary_width):
    width, height = IMG_SIZE
    # Create a blank image for the shape interior
    shape_interior_img = Image.new("L", IMG_SIZE, "white")
    shape_interior_draw = ImageDraw.Draw(shape_interior_img)

    # Draw the shape based on the type
    if shape_type == "triangle":
        shape_coords_triangle = [
            (width // 2, height // 4),
            (width // 4, 3 * height // 4),
            (3 * width // 4, 3 * height // 4),
        ]
        shape_interior_draw.polygon(shape_coords_triangle, fill="black")
    elif shape_type == "square":
        margin = width // 4
        shape_coords_square = [(margin, margin), (width - margin, height - margin)]
        shape_interior_draw.rectangle(shape_coords_square, fill="black")
    
    # Invert the shape interior image to create a mask
    # This mask will be used to paste the texture image
    shape_interior_mask = ImageOps.invert(shape_interior_img)
    texture_img = create_texture_image(texture_type_str, texture_scale)
    final_img = Image.new("L", IMG_SIZE, "white")
    final_img.paste(texture_img, (0,0), shape_interior_mask)

    # Draw a boundary for the shape if boundary width is greater than 0
    if boundary_width > 0:
        final_draw = ImageDraw.Draw(final_img)
        if shape_type == "triangle":
            final_draw.polygon(shape_coords_triangle, outline="black", width=boundary_width)
        elif shape_type == "square":
            final_draw.rectangle(shape_coords_square, outline="black", width=boundary_width)

    # Save the image to the specified filename    
    final_img.save(filename)

# Function to generate the dataset
def generate_dataset():
    # Create output directory if it does not exist yet or clear it if it does
    if os.path.exists(OUTPUT_DIR):
        # Remove all files in directory
        for filename in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        os.makedirs(OUTPUT_DIR)

    # Create training data images
    # Training Set A: Triangle + Stripes
    train_A_dir = os.path.join(OUTPUT_DIR, "train", "A_Triangle_Stripes")
    os.makedirs(train_A_dir, exist_ok=True)
    print("Generating training set A (Triangle + Stripes)...")
    for i in range(NUM_TRAIN_SAMPLES_PER_CLASS):
        fname = os.path.join(train_A_dir, f"triangle_stripes_{i:04d}.png")
        generate_image("triangle", "stripes", fname, TEXTURE_SCALE_FACTOR, SHAPE_BOUNDARY_WIDTH)

    # Training Set B: Square + Dots
    train_B_dir = os.path.join(OUTPUT_DIR, "train", "B_Square_Dots")
    os.makedirs(train_B_dir, exist_ok=True)
    print("Generating training set B (Square + Dots)...")
    for i in range(NUM_TRAIN_SAMPLES_PER_CLASS):
        fname = os.path.join(train_B_dir, f"square_dots_{i:04d}.png")
        generate_image("square", "dots", fname, TEXTURE_SCALE_FACTOR, SHAPE_BOUNDARY_WIDTH)

    # Create test data images
    test_dir = os.path.join(OUTPUT_DIR, "test")
    os.makedirs(test_dir, exist_ok=True)

    # Test Set: Congruent A (Triangle + Stripes)
    test_cong_A_dir = os.path.join(test_dir, "Congruent_A_Triangle_Stripes")
    os.makedirs(test_cong_A_dir, exist_ok=True)
    print("Generating test set: Congruent A (Triangle + Stripes)...")
    for i in range(NUM_TEST_SAMPLES_PER_CONDITION):
        fname = os.path.join(test_cong_A_dir, f"triangle_stripes_{i:04d}.png")
        generate_image("triangle", "stripes", fname, TEXTURE_SCALE_FACTOR, SHAPE_BOUNDARY_WIDTH)

    # Test Set: Congruent B (Square + Dots)
    test_cong_B_dir = os.path.join(test_dir, "Congruent_B_Square_Dots")
    os.makedirs(test_cong_B_dir, exist_ok=True)
    print("Generating test set: Congruent B (Square + Dots)...")
    for i in range(NUM_TEST_SAMPLES_PER_CONDITION):
        fname = os.path.join(test_cong_B_dir, f"square_dots_{i:04d}.png")
        generate_image("square", "dots", fname, TEXTURE_SCALE_FACTOR, SHAPE_BOUNDARY_WIDTH)
        
    # Test Set: Conflict (Triangle with Dots Texture)
    test_conf_TriangleDots_dir = os.path.join(test_dir, "Conflict_TriangleShape_DotsTexture")
    os.makedirs(test_conf_TriangleDots_dir, exist_ok=True)
    print("Generating test set: Conflict (Triangle with Dots Texture)...")
    for i in range(NUM_TEST_SAMPLES_PER_CONDITION):
        fname = os.path.join(test_conf_TriangleDots_dir, f"triangle_dots_{i:04d}.png")
        generate_image("triangle", "dots", fname, TEXTURE_SCALE_FACTOR, SHAPE_BOUNDARY_WIDTH)

    # Test Set: Conflict (Square with Stripes Texture)
    test_conf_SquareStripes_dir = os.path.join(test_dir, "Conflict_SquareShape_StripesTexture")
    os.makedirs(test_conf_SquareStripes_dir, exist_ok=True)
    print("Generating test set: Conflict (Square with Stripes Texture)...")
    for i in range(NUM_TEST_SAMPLES_PER_CONDITION):
        fname = os.path.join(test_conf_SquareStripes_dir, f"square_stripes_{i:04d}.png")
        generate_image("square", "stripes", fname, TEXTURE_SCALE_FACTOR, SHAPE_BOUNDARY_WIDTH)

    print(f"Dataset generation complete in '{OUTPUT_DIR}'")

if __name__ == "__main__":
    generate_dataset()