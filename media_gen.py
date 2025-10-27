import argparse
import os
from typing import List, Dict
from PIL import Image


def read_cards_from_file(filename: str) -> List[List[List[int]]]:
    """Read bingo cards from a text file.

    Args:
        filename: Path to the .txt file containing bingo cards

    Returns:
        List of cards, where each card is a 5x5 grid (list of 5 lists of 5 integers)
    """
    cards = []
    current_card = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # "=" marks the end of a card
            if line == '=':
                if current_card:
                    cards.append(current_card)
                    current_card = []
            else:
                # Parse the row of numbers
                row = [int(num) for num in line.split()]
                if len(row) == 5:  # Validate it's a 5-number row
                    current_card.append(row)

    # Add the last card if it wasn't followed by '='
    if current_card and len(current_card) == 5:
        cards.append(current_card)

    return cards


def load_images_from_folder(folder_path: str) -> Dict[int, str]:
    """Load all JPEG files from a folder and map them to numbers 1-25.

    Args:
        folder_path: Path to the folder containing JPEG images

    Returns:
        Dictionary mapping numbers (1-25) to image file paths
    """
    # Get all .jpg and .jpeg files
    image_files = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            image_files.append(os.path.join(folder_path, filename))

    if len(image_files) != 25:
        raise ValueError(f"Expected 25 images, but found {len(image_files)} in {folder_path}")

    # Map numbers 1-25 to image paths
    image_map = {i + 1: image_files[i] for i in range(25)}
    return image_map


def create_composite_image(card: List[List[int]], image_map: Dict[int, str],
                          cell_size: int = 200, border_size: int = 10) -> Image.Image:
    """Create a 5x5 composite image from a card grid and image mapping.

    Args:
        card: 5x5 grid of numbers
        image_map: Dictionary mapping numbers to image file paths
        cell_size: Size of each cell in pixels (default: 200)
        border_size: Size of border around and between cells in pixels (default: 10)

    Returns:
        PIL Image object of the composite
    """
    # Create a blank canvas (5x5 grid with borders)
    # Total size includes: outer border + 5 cells + 4 inner borders + outer border
    # Which equals: 6 borders + 5 cells
    composite_width = (cell_size * 5) + (border_size * 6)
    composite_height = (cell_size * 5) + (border_size * 6)
    composite = Image.new('RGB', (composite_width, composite_height), 'white')

    # Place each image in the grid
    for row_idx, row in enumerate(card):
        for col_idx, number in enumerate(row):
            # Load and resize the image
            img_path = image_map[number]
            img = Image.open(img_path)
            img = img.resize((cell_size, cell_size), Image.Resampling.LANCZOS)

            # Calculate position with borders
            # Each cell starts after: outer border + (cell + border) * position
            x = border_size + col_idx * (cell_size + border_size)
            y = border_size + row_idx * (cell_size + border_size)

            # Paste the image
            composite.paste(img, (x, y))

    return composite


def generate_card_images(cards: List[List[List[int]]], image_map: Dict[int, str],
                        output_folder: str, cell_size: int = 200, border_size: int = 10):
    """Generate composite images for all cards.

    Args:
        cards: List of 5x5 card grids
        image_map: Dictionary mapping numbers to image file paths
        output_folder: Folder to save the generated images
        cell_size: Size of each cell in pixels
        border_size: Size of border around and between cells in pixels
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    total_size = (cell_size * 5) + (border_size * 6)

    print(f"\nGenerating {len(cards)} bingo card images...")
    print(f"Cell size: {cell_size}x{cell_size} pixels")
    print(f"Border size: {border_size} pixels")
    print(f"Total image size: {total_size}x{total_size} pixels")
    print(f"Output folder: {output_folder}\n")

    for i, card in enumerate(cards, 1):
        print(f"Creating card {i}/{len(cards)}...", end=' ')

        # Create composite image
        composite = create_composite_image(card, image_map, cell_size, border_size)

        # Save the image
        output_path = os.path.join(output_folder, f'bingo_card_{i:02d}.jpg')
        composite.save(output_path, 'JPEG', quality=95)

        print(f"✓ Saved to {output_path}")

    print(f"\n✓ Successfully generated {len(cards)} bingo card images!")


def print_image_mapping(image_map: Dict[int, str]):
    """Print the mapping of numbers to image files."""
    print("\n" + "="*60)
    print("IMAGE MAPPING (Number → Filename)")
    print("="*60)
    for num in sorted(image_map.keys()):
        filename = os.path.basename(image_map[num])
        print(f"{num:2d} → {filename}")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Generate bingo card composite images from number grids and JPEG files'
    )
    parser.add_argument('--cards-file', type=str, default='bingo_cards.txt',
                        help='Path to the bingo cards text file (default: bingo_cards.txt)')
    parser.add_argument('--media-folder', type=str, default='media286',
                        help='Folder containing 25 JPEG images (default: media286)')
    parser.add_argument('--output-folder', type=str, default='output_cards',
                        help='Folder to save generated card images (default: output_cards)')
    parser.add_argument('--cell-size', type=int, default=200,
                        help='Size of each cell in pixels (default: 200)')
    parser.add_argument('--border-size', type=int, default=10,
                        help='Size of border around and between cells in pixels (default: 10)')
    parser.add_argument('--show-mapping', action='store_true',
                        help='Display the number-to-image mapping')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Resolve cards file path
    if not os.path.isabs(args.cards_file):
        cards_file_path = os.path.join(script_dir, args.cards_file)
    else:
        cards_file_path = args.cards_file

    # Resolve media folder path
    if not os.path.isabs(args.media_folder):
        media_folder_path = os.path.join(script_dir, args.media_folder)
    else:
        media_folder_path = args.media_folder

    # Resolve output folder path
    if not os.path.isabs(args.output_folder):
        output_folder_path = os.path.join(script_dir, args.output_folder)
    else:
        output_folder_path = args.output_folder

    # Check if files/folders exist
    if not os.path.exists(cards_file_path):
        print(f"Error: Cards file not found: {cards_file_path}")
        return

    if not os.path.exists(media_folder_path):
        print(f"Error: Media folder not found: {media_folder_path}")
        return

    print("="*60)
    print("BINGO CARD IMAGE GENERATOR")
    print("="*60)

    # Load images and create mapping
    print(f"\nLoading images from: {media_folder_path}")
    try:
        image_map = load_images_from_folder(media_folder_path)
        print(f"✓ Loaded {len(image_map)} images")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Show mapping if requested
    if args.show_mapping:
        print_image_mapping(image_map)

    # Read cards from file
    print(f"\nReading cards from: {cards_file_path}")
    cards = read_cards_from_file(cards_file_path)
    print(f"✓ Loaded {len(cards)} cards")

    # Generate composite images
    generate_card_images(cards, image_map, output_folder_path, args.cell_size, args.border_size)


if __name__ == "__main__":
    main()
