# my_language/cli.py
import sys
from batlang.bat_interpreter import run_file

def main():
    if len(sys.argv) != 2:
        print("Usage: bat-lang <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    run_file(filename)

if __name__ == "__main__":
    main()
