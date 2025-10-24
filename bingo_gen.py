import random
import itertools
import argparse
from typing import List, Set, Tuple

def get_rows(card: List[List[int]]) -> List[Tuple[int, ...]]:
    """Extract all rows from a card as sorted tuples (permutation-invariant)."""
    return [tuple(sorted(row)) for row in card]

def get_columns(card: List[List[int]]) -> List[Tuple[int, ...]]:
    """Extract all columns from a card as sorted tuples (permutation-invariant)."""
    return [tuple(sorted(card[i][j] for i in range(5))) for j in range(5)]

def get_diagonals(card: List[List[int]]) -> List[Tuple[int, ...]]:
    """Extract both diagonals from a card as sorted tuples (permutation-invariant)."""
    main_diag = tuple(sorted(card[i][i] for i in range(5)))
    anti_diag = tuple(sorted(card[i][4-i] for i in range(5)))
    return [main_diag, anti_diag]

def get_all_lines(card: List[List[int]]) -> Set[Tuple[int, ...]]:
    """Get all rows, columns, and diagonals as a set of sorted tuples.

    Lines are stored as sorted tuples so that permutations of the same
    5 numbers are treated as identical.
    """
    lines = set()
    lines.update(get_rows(card))
    lines.update(get_columns(card))
    lines.update(get_diagonals(card))
    return lines

def generate_random_card() -> List[List[int]]:
    """Generate a random 5x5 card with numbers 1-25."""
    numbers = list(range(1, 26))
    random.shuffle(numbers)
    card = [numbers[i*5:(i+1)*5] for i in range(5)]
    return card

def cards_share_line(card1: List[List[int]], card2: List[List[int]]) -> bool:
    """Check if two cards share any identical row, column, or diagonal.

    Lines are compared by their number sets (permutation-invariant), so
    [1,2,3,4,5] and [5,4,3,2,1] are considered the same line.
    """
    lines1 = get_all_lines(card1)
    lines2 = get_all_lines(card2)
    return len(lines1 & lines2) > 0

def generate_unique_cards(num_cards: int, max_attempts: int = 100000) -> List[List[List[int]]]:
    """Generate cards ensuring no two cards share any row, column, or diagonal.

    Lines are compared by their number sets (permutation-invariant).
    """
    cards = []
    attempts = 0
    
    while len(cards) < num_cards and attempts < max_attempts:
        attempts += 1
        new_card = generate_random_card()
        
        # Check if this card shares any line with existing cards
        valid = True
        for existing_card in cards:
            if cards_share_line(new_card, existing_card):
                valid = False
                break
        
        if valid:
            cards.append(new_card)
            print(f"Generated card {len(cards)}/{num_cards} (attempts: {attempts})")
            attempts = 0  # Reset attempts counter
    
    if len(cards) < num_cards:
        print(f"\nWarning: Could only generate {len(cards)} cards after {max_attempts} attempts.")
    
    return cards

def print_card(card: List[List[int]], card_num: int):
    """Print a card in a formatted way."""
    print(f"\n{'='*27}")
    print(f"  CARD {card_num:2d}")
    print(f"{'='*27}")
    for row in card:
        print("  " + "  ".join(f"{num:2d}" for num in row))
    print(f"{'='*27}")

def save_cards_to_file(cards: List[List[List[int]]], filename: str):
    """Save cards to a text file."""
    with open(filename, 'w') as f:
        for i, card in enumerate(cards, 1):
            f.write(f"{'='*27}\n")
            f.write(f"  CARD {i:2d}\n")
            f.write(f"{'='*27}\n")
            for row in card:
                f.write("  " + "  ".join(f"{num:2d}" for num in row) + "\n")
            f.write(f"{'='*27}\n\n")
    print(f"\nCards saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate unique bingo cards')
    parser.add_argument('--seed', type=int, help='Seed value for random number generator (optional, defaults to time-based seeding)')
    args = parser.parse_args()

    print("Generating 20 unique 5x5 cards with numbers 1-25...")
    print("Ensuring no two cards share any row, column, or diagonal.")
    print("(Lines are compared by number sets, ignoring order)\n")

    # Use provided seed or default to time-based seeding
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Using seed: {args.seed}\n")
    else:
        random.seed()  # Use system time for randomness
        print("Using time-based seeding\n")

    cards = generate_unique_cards(20)
    
    if len(cards) == 20:
        print(f"\nSuccessfully generated all 20 cards!")
        
        # Print all cards
        for i, card in enumerate(cards, 1):
            print_card(card, i)
        
        # Save to file
        save_cards_to_file(cards, '/mnt/user-data/outputs/bingo_cards.txt')
        
        # Verify uniqueness
        print("\n" + "="*50)
        print("VERIFICATION")
        print("="*50)
        all_lines = []
        for i, card in enumerate(cards, 1):
            lines = get_all_lines(card)
            all_lines.extend(lines)
        
        total_lines = len(all_lines)
        unique_lines = len(set(all_lines))
        print(f"Total lines (rows, cols, diags): {total_lines}")
        print(f"Unique lines: {unique_lines}")
        print(f"All lines are unique: {total_lines == unique_lines}")
    else:
        print(f"Could only generate {len(cards)} cards. You may need to adjust parameters or try again.")

if __name__ == "__main__":
    main()