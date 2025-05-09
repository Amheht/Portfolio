# utils/prepare_corpus.py

import os
import re
import urllib.request
from pathlib import Path
from typing import List, Tuple

# === Paths ===
input_dir  = Path("data/raw_books")
output_file = Path("data/corpus.txt")

# === List of (filename, URL) pairs ===
books = [
    ("frankenstein.txt", "https://www.gutenberg.org/files/84/84-0.txt"),
    ("moby_dick.txt", "https://www.gutenberg.org/files/2701/2701-0.txt"),
    ("pride_and_prejudice.txt", "https://www.gutenberg.org/files/1342/1342-0.txt"),
    ("alice_in_wonderland.txt", "https://www.gutenberg.org/files/11/11-0.txt"),
    ("romeo_and_juliet.txt", "https://www.gutenberg.org/files/1513/1513-0.txt"),
    ("gatsby.txt", "https://www.gutenberg.org/files/64317/64317-0.txt"),
    ("importance_of_being_earnest.txt", "https://www.gutenberg.org/files/844/844-0.txt"),
    ("middlemarch.txt", "https://www.gutenberg.org/files/145/145-0.txt"),
    ("little_women.txt", "https://www.gutenberg.org/files/514/514-0.txt"),
    ("dracula.txt", "https://www.gutenberg.org/files/345/345-0.txt"),
]

def get_books(input_dir: Path, books: List[Tuple[str, str]]) -> None:
    """
    Downloads books from Project Gutenberg if they are not already present.
    """

    input_dir.mkdir(parents=True, exist_ok=True)
    for name, url in books:
        dest_path = input_dir / name
        if dest_path.exists():
            print(f"   {name} already exists. Skipping download.")
            continue
        print(f"   Downloading {name}...", end='')
        urllib.request.urlretrieve(url, dest_path)
        print("Done")
    print("Book downloads complete.")

def clean_gutenberg_text(file_path: str) -> str:
    """
    Cleans up Project Gutenberg etexts for use from the given file.
    
    Args:
        file_path: the books location on the disk.

    Returns:
        A cleaned text string.
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start = 0
    end = len(lines)
    for i, line in enumerate(lines):
        if '*** START OF THE PROJECT GUTENBERG EBOOK' in line:
            start = i + 1
        elif '*** END OF THE PROJECT GUTENBERG EBOOK' in line:
            end = i
            break
    
    text = ''.join(lines[start:end])

    # Fix any unicode artefacts.
    text = fix_unicode(text)
    
    # Remove lines that are mostly special chars.
    text = re.sub(r'^[\s\*\-_=]{3,}$', '', text, flags=re.MULTILINE)

    # Remove excessive newlines.
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove any trailing whitespace
    text = text.strip()

    return text
	
def fix_unicode(text: str) -> str:
    """
    Fix common Unicode artifacts from poorly encoded sources.
    
    Args:
        text: String to fix.
    
    Returns:
        Cleaned text with corrected Unicode characters.
    """
    replacements = {
        "â€”": "—",  # em dash
        "â€“": "–",  # en dash
        "â€˜": "‘",  # left single quote
        "â€™": "’",  # right single quote
        "â€œ": "“",  # left double quote
        "â€�": "”", # right double quote
        "â€¦": "…",  # ellipsis
        "Â ": "",    # stray non-breaking space
    }
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    return text

def merge_books(input_dir: Path, output_file: Path) -> None:
    """
    Cleans and merges all book files into a single corpus file.
    """

    output_file.parent.mkdir(parents=True, exist_ok=True)
    book_files = sorted(input_dir.glob("*.txt"))

    if not book_files:
        print("No books found. Cannot merge nothing.")
        return
			
    with open(output_file, "w", encoding="utf-8") as out:
    	for book_file in book_files:
            title = book_file.stem.replace("_", " ").title()
            print(f"   Processing: {title}")
            cleaned_text = clean_gutenberg_text(book_file)
            out.write(f"   [TITLE: {title}]\n")
            out.write(cleaned_text + "\n\n")
    print(f"Books cleaned and merged into {output_file}")
							
def main():
    print("Preparing corpus...")
    get_books(input_dir, books)
    merge_books(input_dir, output_file)

if __name__ == "__main__":
    main()
