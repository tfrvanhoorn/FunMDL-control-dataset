# Shape-Texture Dataset Generator

This repository contains code to generate a controlled dataset of shapes with textures for machine learning experiments. The dataset consists of triangles and squares with stripe and dot textures in various combinations.

## Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository
   
2. Navigate to the repository folder in the terminal

3. Create a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

## Dataset Generation

The script `dataset_generation.py` generates a dataset with the following structure:

```
shape_texture_dataset/
├── train/
│   ├── A_Triangle_Stripes/
│   └── B_Square_Dots/
└── test/
    ├── Congruent_A_Triangle_Stripes/
    ├── Congruent_B_Square_Dots/
    ├── Conflict_TriangleShape_DotsTexture/
    └── Conflict_SquareShape_StripesTexture/
```

### Features
- Shapes: Triangle and Square
- Textures: Stripes and Dots
- Shape boundary width: 2 pixels (default)
- Centered textures within shapes

### Running the Generator

To generate the dataset:
```bash
python dataset_generation.py
```

### Output
The script will create:
1. Training set:
   - Triangle with stripes texture
   - Square with dots texture
2. Test set:
   - Congruent combinations (matching training)
   - Conflict combinations (mismatched shapes and textures)

## Configuration

You can modify the following parameters in `dataset_generation.py`:
- `NUM_TRAIN_SAMPLES_PER_CLASS`: Number of training images per class
- `NUM_TEST_SAMPLES_PER_CONDITION`: Number of test images per condition
- `IMG_SIZE`: Image dimensions (width, height)
- `TEXTURE_SCALE_FACTOR`: Scale factor for texture size
- `SHAPE_BOUNDARY_WIDTH`: Width of shape boundaries

### Default Settings
The following settings were used to generate the dataset described in the blog post:
```python
NUM_TRAIN_SAMPLES_PER_CLASS = 200
NUM_TEST_SAMPLES_PER_CONDITION = 50
IMG_SIZE = (128, 128)
TEXTURE_SCALE_FACTOR = 1
SHAPE_BOUNDARY_WIDTH = 2
```

These settings produce:
- Training set: 400 images total (200 per class)
- Test set: 200 images total (50 per condition × 4 conditions)
- All images are 128×128 pixels in grayscale
- Shapes have a 2-pixel black outline
- Textures are scaled to their base size (scale factor = 1)