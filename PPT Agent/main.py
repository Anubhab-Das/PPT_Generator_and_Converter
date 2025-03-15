# main.py
import argparse
from ppt_generator import create_presentation

def main():
    
    parser = argparse.ArgumentParser(description="Generate a PowerPoint presentation using Gemini API.")
    parser.add_argument("topics", nargs="+", help="List of topics for the presentation")
    args = parser.parse_args()

    create_presentation(args.topics)

if __name__ == "__main__":
    main()
