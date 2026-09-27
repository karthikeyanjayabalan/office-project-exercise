import sys

def main():
    print("🤖 Echo Bot initialized! Type something and press Enter (or type 'exit' to quit).", flush=True)
    
    while True:
        try:
            # sys.stdin.readline handles streamed runtime inputs cleanly inside Docker
            user_input = sys.stdin.readline().strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'exit':
                print("Goodbye! 👋", flush=True)
                break
                
            print(f"You said: {user_input}", flush=True)
            
        except KeyboardInterrupt:
            print("\nExiting...", flush=True)
            break

if __name__ == "__main__":
    main()
