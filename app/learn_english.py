#!/usr/bin/env python3
"""
Vocabulary Learning Tool
A command-line application for managing and testing vocabulary words.
"""

import os
import re
import random
import threading
import subprocess
import sys
import json
import signal
from typing import Dict, Optional, List, Tuple, Generator
from dataclasses import dataclass
from pathlib import Path
import argparse

# Constants
DEFAULT_LINE_LENGTH = 80
DEFAULT_DATA_FILE = Path.home() / ".words.dat"
SUPPORTED_LANGUAGES = ['en', 'zh', 'ja', 'ko']

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def is_cjk(char: str) -> bool:
    """
    Check if a character is CJK (Chinese, Japanese, Korean)
    
    Args:
        char: Single character to check
        
    Returns:
        True if character is CJK, False otherwise
    """
    # CJK Unified Ideographs
    if '\u4e00' <= char <= '\u9fff':
        return True
    # Hiragana
    if '\u3040' <= char <= '\u309f':
        return True
    # Katakana
    if '\u30a0' <= char <= '\u30ff':
        return True
    # Hangul
    if '\uac00' <= char <= '\ud7af':
        return True
    return False

def get_char_width(char: str) -> int:
    """
    Get the display width of a character (2 for CJK, 1 for others)
    
    Args:
        char: Character to check
        
    Returns:
        Display width of the character
    """
    return 2 if is_cjk(char) else 1

@dataclass
class WordEntry:
    """Data class for word entries"""
    word: str
    meaning: str
    tags: List[str] = None
    examples: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.examples is None:
            self.examples = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'word': self.word,
            'meaning': self.meaning,
            'tags': self.tags,
            'examples': self.examples
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'WordEntry':
        """Create from dictionary"""
        return cls(
            word=data['word'],
            meaning=data['meaning'],
            tags=data.get('tags', []),
            examples=data.get('examples', [])
        )

class VocabularyError(Exception):
    """Custom exception for vocabulary application"""
    pass

class WordFormatter:
    """Handles formatting of words for display"""
    
    def __init__(self, line_length: int = DEFAULT_LINE_LENGTH):
        self.line_length = line_length
    
    def center_text(self, text: str, border_char: str = "=", 
                   border_type: int = 1) -> str:
        """
        Center text within bordered lines
        
        Args:
            text: Text to center
            border_char: Character to use for border
            border_type: 1 for solid border, 2 for dashed
            
        Returns:
            Formatted string
        """
        # Calculate display width considering CJK characters
        display_width = sum(get_char_width(c) for c in text)
        
        # Calculate padding
        total_padding = self.line_length - display_width - 2  # -2 for borders
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        
        # Determine inner character
        inner_char = border_char if border_type == 1 else " "
        
        # Build the formatted line
        result = border_char
        result += inner_char * left_padding
        result += text
        result += inner_char * right_padding
        result += border_char
        
        return result
    
    def format_word_display(self, word: str, meaning: str) -> str:
        """Format word and meaning for display"""
        lines = []
        lines.append(self.center_text("WORD", "="))
        lines.append(self.center_text(word, "=", 2))
        lines.append(self.center_text(meaning, "=", 2))
        lines.append(self.center_text("", "="))
        return "\n".join(lines)

class VocabularyDatabase:
    """Manages persistence of vocabulary data"""
    
    def __init__(self, data_file: Path = DEFAULT_DATA_FILE):
        self.data_file = data_file
        self.words: Dict[str, WordEntry] = {}
    
    def save(self, filename: Optional[Path] = None) -> None:
        """Save vocabulary to file"""
        save_file = filename or self.data_file
        
        try:
            # Convert to serializable format
            data = {
                word: entry.to_dict() 
                for word, entry in self.words.items()
            }
            
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"{Colors.GREEN}✓ Dictionary saved to {save_file}{Colors.END}")
            print(f"Total words: {len(self.words)}")
            
        except IOError as e:
            raise VocabularyError(f"Failed to save dictionary: {e}")
    
    def load(self, filename: Optional[Path] = None) -> None:
        """Load vocabulary from file"""
        load_file = filename or self.data_file
        
        if not load_file.exists():
            print(f"{Colors.WARNING}! {load_file} doesn't exist.{Colors.END}")
            return
        
        try:
            with open(load_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clear current data and load new
            self.words.clear()
            for word, entry_data in data.items():
                self.words[word] = WordEntry.from_dict(entry_data)
            
            print(f"{Colors.GREEN}✓ Dictionary loaded from {load_file}{Colors.END}")
            print(f"Total words: {len(self.words)}")
            
        except json.JSONDecodeError:
            raise VocabularyError(f"Invalid JSON format in {load_file}")
        except IOError as e:
            raise VocabularyError(f"Failed to load dictionary: {e}")
    
    def export_csv(self, filename: Path) -> None:
        """Export vocabulary to CSV format"""
        import csv
        
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Word', 'Meaning', 'Tags', 'Examples'])
                
                for entry in self.words.values():
                    writer.writerow([
                        entry.word,
                        entry.meaning,
                        '|'.join(entry.tags),
                        '|'.join(entry.examples)
                    ])
            
            print(f"{Colors.GREEN}✓ Exported to {filename}{Colors.END}")
            
        except IOError as e:
            raise VocabularyError(f"Failed to export: {e}")

class VocabularyApp:
    """Main application class"""
    
    def __init__(self, data_file: Optional[Path] = None):
        self.db = VocabularyDatabase(data_file or DEFAULT_DATA_FILE)
        self.formatter = WordFormatter()
        self.running = True
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Load default data file if it exists
        if DEFAULT_DATA_FILE.exists():
            self.db.load()
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n{Colors.WARNING}Interrupted. Exiting...{Colors.END}")
        self.running = False
        sys.exit(0)
    
    def add_word(self, word: str, meaning: str, 
                tags: Optional[List[str]] = None,
                examples: Optional[List[str]] = None) -> None:
        """
        Add a new word to the vocabulary
        
        Args:
            word: The word to add
            meaning: The meaning/translation
            tags: Optional list of tags
            examples: Optional list of example sentences
        """
        if not word or not meaning:
            raise VocabularyError("Word and meaning are required")
        
        # Check for duplicates
        if word in self.db.words:
            print(f"{Colors.WARNING}Warning: '{word}' already exists.{Colors.END}")
            response = input("Overwrite? (y/n): ").lower()
            if response != 'y':
                print("Addition cancelled.")
                return
        
        entry = WordEntry(word=word, meaning=meaning, tags=tags, examples=examples)
        self.db.words[word] = entry
        print(f"{Colors.GREEN}✓ Added: {word} -> {meaning}{Colors.END}")
    
    def search_words(self, pattern: str, use_regex: bool = False) -> List[str]:
        """
        Search for words matching pattern
        
        Args:
            pattern: Search pattern
            use_regex: Whether to treat pattern as regex
            
        Returns:
            List of matching words
        """
        matches = []
        
        try:
            if use_regex:
                regex = re.compile(pattern, re.IGNORECASE)
                matches = [w for w in self.db.words.keys() if regex.search(w)]
            else:
                # Simple case-insensitive substring search
                pattern_lower = pattern.lower()
                matches = [w for w in self.db.words.keys() 
                          if pattern_lower in w.lower()]
        except re.error as e:
            raise VocabularyError(f"Invalid regex pattern: {e}")
        
        return matches
    
    def display_word(self, word: str, play_sound: bool = False) -> None:
        """Display a single word with formatting"""
        if word not in self.db.words:
            print(f"{Colors.FAIL}✗ Word '{word}' not found{Colors.END}")
            return
        
        entry = self.db.words[word]
        
        # Clear screen for better visibility
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Display word
        print(self.formatter.format_word_display(entry.word, entry.meaning))
        
        # Display tags if any
        if entry.tags:
            print(f"\n{Colors.CYAN}Tags: {', '.join(entry.tags)}{Colors.END}")
        
        # Display examples if any
        if entry.examples:
            print(f"\n{Colors.BLUE}Examples:{Colors.END}")
            for i, example in enumerate(entry.examples, 1):
                print(f"  {i}. {example}")
        
        # Play sound if requested
        if play_sound:
            self.speak_word(word)
    
    def speak_word(self, text: str) -> None:
        """Speak text using text-to-speech"""
        def speak():
            try:
                if sys.platform == 'darwin':  # macOS
                    subprocess.run(['say', text], check=False)
                elif sys.platform == 'linux':  # Linux (requires espeak)
                    subprocess.run(['espeak', text], check=False)
                elif sys.platform == 'win32':  # Windows
                    import win32com.client
                    speaker = win32com.client.Dispatch("SAPI.SpVoice")
                    speaker.Speak(text)
            except Exception as e:
                print(f"{Colors.WARNING}Speech failed: {e}{Colors.END}")
        
        threading.Thread(target=speak, daemon=True).start()
    
    def test_session(self, num_words: Optional[int] = None, 
                    play_sound: bool = False) -> None:
        """
        Run an interactive test session
        
        Args:
            num_words: Number of words to test (None for all)
            play_sound: Whether to play sounds
        """
        if not self.db.words:
            print(f"{Colors.WARNING}No words to test!{Colors.END}")
            return
        
        # Select words to test
        words = list(self.db.words.keys())
        random.shuffle(words)
        
        if num_words:
            words = words[:min(num_words, len(words))]
        
        total = len(words)
        correct = 0
        
        print(f"\n{Colors.HEADER}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}Starting test session with {total} words{Colors.END}")
        print(f"{Colors.HEADER}{'='*50}{Colors.END}\n")
        
        for i, word in enumerate(words, 1):
            entry = self.db.words[word]
            
            print(f"\n{Colors.CYAN}Word {i}/{total}{Colors.END}")
            print(f"Meaning: {entry.meaning}")
            
            if play_sound:
                self.speak_word(word)
            
            response = input("Your answer (or 'q' to quit): ").strip()
            
            if response.lower() == 'q':
                break
            
            if response.lower() == word.lower():
                print(f"{Colors.GREEN}✓ Correct!{Colors.END}")
                correct += 1
            else:
                print(f"{Colors.FAIL}✗ Wrong. Correct answer: {word}{Colors.END}")
        
        # Show results
        if i > 0:
            percentage = (correct / i) * 100
            print(f"\n{Colors.HEADER}{'='*50}{Colors.END}")
            print(f"Results: {correct}/{i} correct ({percentage:.1f}%)")
            print(f"{Colors.HEADER}{'='*50}{Colors.END}")
    
    def show_stats(self) -> None:
        """Display statistics about the vocabulary"""
        if not self.db.words:
            print("No words in dictionary.")
            return
        
        total = len(self.db.words)
        
        # Calculate word length statistics
        word_lengths = [len(w) for w in self.db.words.keys()]
        avg_length = sum(word_lengths) / total if total > 0 else 0
        
        # Count CJK characters
        cjk_count = sum(
            1 for w in self.db.words.keys() 
            for c in w if is_cjk(c)
        )
        
        # Tag statistics
        all_tags = []
        for entry in self.db.words.values():
            all_tags.extend(entry.tags)
        tag_counts = {tag: all_tags.count(tag) for tag in set(all_tags)}
        
        print(f"\n{Colors.HEADER}📊 Vocabulary Statistics{Colors.END}")
        print(f"{'='*40}")
        print(f"Total words: {total}")
        print(f"Words with CJK characters: {cjk_count}")
        print(f"Average word length: {avg_length:.1f} characters")
        
        if tag_counts:
            print(f"\n{Colors.CYAN}Tags:{Colors.END}")
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {tag}: {count}")
        
        # Show sample of words
        print(f"\n{Colors.CYAN}Sample words:{Colors.END}")
        sample = random.sample(list(self.db.words.keys()), min(5, total))
        for word in sample:
            print(f"  • {word}: {self.db.words[word].meaning}")
    
    def run_interactive(self) -> None:
        """Run interactive command-line interface"""
        help_text = f"""
{Colors.HEADER}Vocabulary Learning Tool - Commands{Colors.END}
{Colors.BOLD}{'='*50}{Colors.END}

  {Colors.GREEN}add|a <word> <meaning> [tags]{Colors.END}
        Add a new word (tags separated by commas)
        Example: a hello 你好 greeting,common

  {Colors.GREEN}search|s <pattern> [-r]{Colors.END}
        Search for words (-r for regex)
        Example: s ^hello -r

  {Colors.GREEN}show|w <word> [-s]{Colors.END}
        Display a word (-s to play sound)

  {Colors.GREEN}test|t [number] [-s]{Colors.END}
        Start a test session

  {Colors.GREEN}list|l [tag]{Colors.END}
        List all words (optionally filter by tag)

  {Colors.GREEN}stats|st{Colors.END}
        Show vocabulary statistics

  {Colors.GREEN}save [filename]{Colors.END}
        Save vocabulary to file

  {Colors.GREEN}load [filename]{Colors.END}
        Load vocabulary from file

  {Colors.GREEN}export <filename.csv>{Colors.END}
        Export to CSV format

  {Colors.GREEN}delete|d <word>{Colors.END}
        Delete a word

  {Colors.GREEN}clear{Colors.END}
        Clear all words

  {Colors.GREEN}help|h{Colors.END}
        Show this help

  {Colors.GREEN}quit|q{Colors.END}
        Exit the program
"""
        
        print(f"{Colors.HEADER}Vocabulary Learning Tool{Colors.END}")
        print("Type 'help' for commands\n")
        
        while self.running:
            try:
                command = input(f"{Colors.BOLD}vocab> {Colors.END}").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd in ['quit', 'q', 'exit']:
                    print("Goodbye!")
                    break
                
                elif cmd in ['help', 'h']:
                    print(help_text)
                
                elif cmd in ['add', 'a']:
                    if len(parts) < 3:
                        print("Usage: add <word> <meaning> [tags]")
                        continue
                    
                    word = parts[1]
                    meaning = parts[2]
                    tags = parts[3].split(',') if len(parts) > 3 else None
                    self.add_word(word, meaning, tags)
                
                elif cmd in ['search', 's']:
                    if len(parts) < 2:
                        print("Usage: search <pattern> [-r]")
                        continue
                    
                    pattern = parts[1]
                    use_regex = '-r' in parts
                    matches = self.search_words(pattern, use_regex)
                    
                    if matches:
                        print(f"\nFound {len(matches)} matches:")
                        for word in matches:
                            print(f"  • {word}: {self.db.words[word].meaning}")
                    else:
                        print("No matches found.")
                
                elif cmd in ['show', 'w']:
                    if len(parts) < 2:
                        print("Usage: show <word> [-s]")
                        continue
                    
                    word = parts[1]
                    play_sound = '-s' in parts
                    self.display_word(word, play_sound)
                
                elif cmd in ['test', 't']:
                    num_words = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
                    play_sound = '-s' in parts
                    self.test_session(num_words, play_sound)
                
                elif cmd in ['list', 'l']:
                    tag_filter = parts[1] if len(parts) > 1 else None
                    
                    words = self.db.words.items()
                    if tag_filter:
                        words = [(w, e) for w, e in words if tag_filter in e.tags]
                    
                    if words:
                        print(f"\n{Colors.CYAN}Words:{Colors.END}")
                        for word, entry in sorted(words):
                            tag_str = f" [{', '.join(entry.tags)}]" if entry.tags else ""
                            print(f"  • {word}: {entry.meaning}{tag_str}")
                        print(f"\nTotal: {len(words)}")
                    else:
                        print("No words found.")
                
                elif cmd in ['stats', 'st']:
                    self.show_stats()
                
                elif cmd == 'save':
                    filename = parts[1] if len(parts) > 1 else None
                    self.db.save(Path(filename) if filename else None)
                
                elif cmd == 'load':
                    filename = parts[1] if len(parts) > 1 else None
                    self.db.load(Path(filename) if filename else None)
                
                elif cmd == 'export':
                    if len(parts) < 2:
                        print("Usage: export <filename.csv>")
                        continue
                    self.db.export_csv(Path(parts[1]))
                
                elif cmd in ['delete', 'd']:
                    if len(parts) < 2:
                        print("Usage: delete <word>")
                        continue
                    
                    word = parts[1]
                    if word in self.db.words:
                        del self.db.words[word]
                        print(f"{Colors.GREEN}✓ Deleted '{word}'{Colors.END}")
                    else:
                        print(f"{Colors.FAIL}✗ Word not found{Colors.END}")
                
                elif cmd == 'clear':
                    confirm = input("Are you sure? (y/n): ").lower()
                    if confirm == 'y':
                        self.db.words.clear()
                        print("Dictionary cleared.")
                
                else:
                    print(f"{Colors.WARNING}Unknown command. Type 'help' for available commands.{Colors.END}")
            
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"{Colors.FAIL}Error: {e}{Colors.END}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Vocabulary Learning Tool')
    parser.add_argument('-f', '--file', type=Path, help='Data file to use')
    parser.add_argument('-a', '--add', nargs=2, metavar=('WORD', 'MEANING'),
                       help='Add a word and exit')
    parser.add_argument('-s', '--search', help='Search for a word and exit')
    parser.add_argument('--stats', action='store_true', help='Show statistics and exit')
    
    args = parser.parse_args()
    
    app = VocabularyApp(args.file)
    
    if args.add:
        app.add_word(args.add[0], args.add[1])
        app.db.save()
    elif args.search:
        matches = app.search_words(args.search)
        for word in matches:
            print(f"{word}: {app.db.words[word].meaning}")
    elif args.stats:
        app.show_stats()
    else:
        app.run_interactive()

if __name__ == "__main__":
    main()