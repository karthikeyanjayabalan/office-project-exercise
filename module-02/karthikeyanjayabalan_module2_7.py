import json
import os
import random

SAVE_FILE = "2048_session.json"

class Game2048:
    def __init__(self, resume=False):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.won = False
        
        # 1. Attempt to load existing session if requested
        if resume and os.path.exists(SAVE_FILE):
            self.load_game()
        else:
            # Otherwise initialize fresh baseline tiles
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
        
        for row in self.grid:
            print("|" + "|".join(f"{val if val > 0 else '':^7}" for val in row) + "|")
            print("-" * 33)
            
        print(" Controls: W (Up) | S (Down) | A (Left) | D (Right)")
        print(" Options:  Q (Save & Quit)")

    def _slide_and_merge_row(self, row):
        """Slides non-zero elements to the left and merges identical adjacent values."""
        non_zeros = [val for val in row if val != 0]
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
                
        new_row += [0] * (4 - len(new_row))
        return new_row

    def move(self, direction):
        """Applies matrix rotations/reflections to process moves using one sliding function."""
        old_grid = [row[:] for row in self.grid]
        
        if direction == 'A':  # LEFT
            self.grid = [self._slide_and_merge_row(row) for row in self.grid]
        elif direction == 'D':  # RIGHT
            self.grid = [self._slide_and_merge_row(row[::-1])[::-1] for row in self.grid]
        elif direction == 'W':  # UP
            for col_idx in range(4):
                col = [self.grid[row_idx][col_idx] for row_idx in range(4)]
                new_col = self._slide_and_merge_row(col)
                for row_idx in range(4):
                    self.grid[row_idx][col_idx] = new_col[row_idx]
        elif direction == 'S':  # DOWN
            for col_idx in range(4):
                col = [self.grid[row_idx][col_idx] for row_idx in range(4)][::-1]
                new_col = self._slide_and_merge_row(col)[::-1]
                for row_idx in range(4):
                    self.grid[row_idx][col_idx] = new_col[row_idx]

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

    # =========================================================================
    # 💾 NEW SESSION PERSISTENCE OPERATIONS
    # =========================================================================
    def save_game(self):
        """Writes current matrix composition and scoring parameters to a structural JSON file."""
        session_data = {
            "grid": self.grid,
            "score": self.score,
            "won": self.won
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(session_data, f)
        print("\n💾 Session saved successfully! You can resume next time.")

    def load_game(self):
        """Reconstructs state context variables directly out of file storage data blocks."""
        with open(SAVE_FILE, "r") as f:
            session_data = json.load(f)
        self.grid = session_data["grid"]
        self.score = session_data["score"]
        self.won = session_data["won"]

def delete_save_file():
    """Removes the save file when a game is over or won to ensure clean subsequent starts."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

def play_game():
    resume_choice = False
    
    # Check if a historical session file exists on host storage layout
    if os.path.exists(SAVE_FILE):
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input("💾 Found a saved game session! Continue playing? (Y/N): ").strip().upper()
        if choice == 'Y':
            resume_choice = True

    game = Game2048(resume=resume_choice)
    
    while True:
        game.display()
        
        if game.won:
            print("\n🎉 CONGRATULATIONS! You successfully reached the 2048 tile! 🎉")
            delete_save_file()
            break
            
        if game.is_game_over():
            print("\n💀 GAME OVER! No available moves left on the matrix grid. 💀")
            delete_save_file()
            break
            
        user_input = input("\nEnter Move: ").strip().upper()
        
        if user_input == 'Q':
            game.save_game()
            print("Exiting current session workspace loop. Goodbye!\n")
            break
            
        if user_input in ['W', 'A', 'S', 'D']:
            moved = game.move(user_input)
            if moved:
                game.add_new_tile()
                # Auto-save backup state progress after every successful turn movement
                game.save_game()

if __name__ == "__main__":
    play_game()
