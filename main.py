import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", "-o", required=True)
    args = parser.parse_args()

    input_text = sys.stdin.read()

if __name__ == "__main__":
    main()
