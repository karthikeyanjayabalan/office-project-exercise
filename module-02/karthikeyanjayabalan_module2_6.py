import os
import random

class Game2048:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.won = False
        # Add the first two starting tiles
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        """Finds all empty cells and randomly places a 2 (90% chance) or 4 (10% chance)."""
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def display(self):
        """Clears the console screen and renders a beautiful text-aligned board."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 33)
        print(f"       GAME 2048 TERMINAL       ")
        print(f"       SCORE: {self.score:<18}")
        print("=" * 33)
        
        # Build decorative borders and handle grid display padding
        for row in self.grid:
            print("|" + "|".join(f"{val if val > 0 else '':^7}" for val in row) + "|")
            print("-" * 33)
            
        print(" Controls: W (Up) | S (Down) | A (Left) | D (Right) | Q (Quit)")

    def _slide_and_merge_row(self, row):
        """Slides non-zero elements to the left and merges identical adjacent values."""
        # Step 1: Shift all numbers to the left side (remove zeros)
        non_zeros = [val for val in row if val != 0]
        
        # Step 2: Merge identical numbers side by side
        new_row = []
        skip = False
        for i in range(len(non_zeros)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zeros) and non_zeros[i] == non_zeros[i+1]:
                merged_val = non_zeros[i] * 2
                new_row.append(merged_val)
                self.score += merged_val
                if merged_val == 2048:
                    self.won = True
                skip = True
            else:
                new_row.append(non_zeros[i])
                
        # Step 3: Fill the remaining space with zeros to keep row size equal to 4
        new_row += [0] * (4 - len(new_row))
        return new_row

    def move(self, direction):
        """Applies matrix rotations/reflections to process moves using one sliding function."""
        old_grid = [row[:] for row in self.grid]
        
        if direction == 'A':  # LEFT
            self.grid = [self._slide_and_merge_row(row) for row in self.grid]
            
        elif direction == 'D':  # RIGHT
            # Flip rows horizontally, slide left, then flip back
            self.grid = [self._slide_and_merge_row(row[::-1])[::-1] for row in self.grid]
            
        elif direction == 'W':  # UP
            # Transpose columns to rows, slide left, then transpose back
            for col_idx in range(4):
                col = [self.grid[row_idx][col_idx] for row_idx in range(4)]
                new_col = self._slide_and_merge_row(col)
                for row_idx in range(4):
                    self.grid[row_idx][col_idx] = new_col[row_idx]
                    
        elif direction == 'S':  # DOWN
            # Transpose columns, reverse them, slide left, reverse back, transpose back
            for col_idx in range(4):
                col = [self.grid[row_idx][col_idx] for row_idx in range(4)][::-1]
                new_col = self._slide_and_merge_row(col)[::-1]
                for row_idx in range(4):
                    self.grid[row_idx][col_idx] = new_col[row_idx]

        # Returns True if something actually moved, allowing a new tile to spawn
        return self.grid != old_grid

    def is_game_over(self):
        """Checks if any valid moves remain on the board grid."""
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == 0:
                    return False
                if r + 1 < 4 and self.grid[r][c] == self.grid[r+1][c]:
                    return False
                if c + 1 < 4 and self.grid[r][c] == self.grid[r][c+1]:
                    return False
        return True

def play_game():
    game = Game2048()
    
    while True:
        game.display()
        
        if game.won:
            print("\n🎉 CONGRATULATIONS! You successfully reached the 2048 tile! 🎉")
            break
            
        if game.is_game_over():
            print("\n💀 GAME OVER! No available moves left on the matrix grid. 💀")
            break
            
        # Capture keystroke inputs from command line
        user_input = input("\nEnter Move: ").strip().upper()
        
        if user_input == 'Q':
            print("\nExiting current session grid layout. Goodbye!")
            break
            
        if user_input in ['W', 'A', 'S', 'D']:
            moved = game.move(user_input)
            if moved:
                game.add_new_tile()

if __name__ == "__main__":
    play_game()
