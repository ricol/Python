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
from typing import Dict, Optional, List, Tuple, Generator, Union
from dataclasses import dataclass, field
from pathlib import Path
import argparse
import urllib.request
import urllib.error
import time
import socket

# Constants
DEFAULT_LINE_LENGTH = 80
DEFAULT_DATA_FILE = Path.home() / ".words.dat"
SUPPORTED_LANGUAGES = ['en', 'zh', 'ja', 'ko']
RANDOM_WORD_CACHE_FILE = Path.home() / ".word_cache.json"
RANDOM_WORD_CACHE_EXPIRY = 86400  # 24 hours in seconds

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

class RandomWordFetcher:
    """
    Fetches random English words from various online sources
    with local caching for offline use.
    """
    
    # API endpoints for random word generation
    API_ENDPOINTS = [
        {
            'name': 'WordDrip',
            'url': 'https://worddrip.onrender.com/',
            'response_type': 'json',
            'word_field': 'word',
            'definition_field': 'definition',
            'enabled': True
        },
        {
            'name': 'Random-Words-API',
            'url': 'https://random-words-api-9itish.vercel.app/',
            'response_type': 'json',
            'word_field': 'word',
            'definition_field': 'definition',
            'enabled': True
        }
    ]
    
    # Built-in word list as fallback (common English words)
    FALLBACK_WORDS = [
        "serendipity", "ephemeral", "quintessential", "mellifluous", 
        "petrichor", "sonorous", "effervescent", "luminescence",
        "ethereal", "opulent", "resplendent", "cherish",
        "solitude", "serenity", "tranquility", "harmony",
        "curiosity", "adventure", "discovery", "imagination",
        "resilience", "perseverance", "dedication", "ambition"
    ]
    
    def __init__(self):
        self.cache = self._load_cache()
        self.session = None  # Will initialize if needed
    
    def _load_cache(self) -> Dict:
        """Load cached words from disk"""
        if RANDOM_WORD_CACHE_FILE.exists():
            try:
                with open(RANDOM_WORD_CACHE_FILE, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    # Check if cache is still valid
                    if time.time() - cache.get('timestamp', 0) < RANDOM_WORD_CACHE_EXPIRY:
                        return cache
            except (json.JSONDecodeError, IOError):
                pass
        return {'timestamp': time.time(), 'words': []}
    
    def _save_cache(self):
        """Save cached words to disk"""
        try:
            self.cache['timestamp'] = time.time()
            with open(RANDOM_WORD_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2)
        except IOError:
            pass  # Silently fail if can't write cache
    
    def _fetch_from_api(self, api_config: Dict) -> Optional[Dict]:
        """
        Fetch a random word from a specific API
        
        Args:
            api_config: API configuration dictionary
            
        Returns:
            Dictionary with word and definition, or None if failed
        """
        if not api_config.get('enabled', True):
            return None
        
        try:
            # Set timeout to avoid hanging
            req = urllib.request.Request(
                api_config['url'],
                headers={'User-Agent': 'Vocabulary-Learning-Tool/1.0'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                # Handle different response structures
                if api_config['response_type'] == 'json':
                    word = data.get(api_config['word_field'])
                    
                    # Try to get definition if available
                    definition = None
                    if api_config.get('definition_field'):
                        definition = data.get(api_config['definition_field'])
                    
                    if word:
                        return {
                            'word': word,
                            'definition': definition,
                            'source': api_config['name']
                        }
                        
        except (urllib.error.URLError, socket.timeout, json.JSONDecodeError, KeyError) as e:
            # Silently fail and try next API
            pass
        
        return None
    
    def fetch_random_word(self, force_refresh: bool = False) -> Dict:
        """
        Fetch a random word from online sources or cache
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh
            
        Returns:
            Dictionary with word information
        """
        # Check cache first if not forcing refresh
        if not force_refresh and self.cache.get('words'):
            # Return a random word from cache
            cached_word = random.choice(self.cache['words'])
            return {
                'word': cached_word['word'],
                'definition': cached_word.get('definition'),
                'source': 'cache'
            }
        
        # Try each API in random order
        api_order = self.API_ENDPOINTS.copy()
        random.shuffle(api_order)
        
        for api in api_order:
            result = self._fetch_from_api(api)
            if result:
                # Add to cache
                self.cache.setdefault('words', []).append({
                    'word': result['word'],
                    'definition': result.get('definition')
                })
                # Keep cache size reasonable (last 100 words)
                if len(self.cache['words']) > 100:
                    self.cache['words'] = self.cache['words'][-100:]
                self._save_cache()
                return result
        
        # Fallback to built-in word list
        word = random.choice(self.FALLBACK_WORDS)
        return {
            'word': word,
            'definition': None,
            'source': 'fallback'
        }
    
    def fetch_multiple_words(self, count: int = 5) -> List[Dict]:
        """
        Fetch multiple random words
        
        Args:
            count: Number of words to fetch
            
        Returns:
            List of word dictionaries
        """
        words = []
        for _ in range(count):
            words.append(self.fetch_random_word())
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        return words

@dataclass
class WordEntry:
    """Data class for word entries"""
    word: str
    meaning: str
    tags: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    
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
        self.word_fetcher = RandomWordFetcher()
        
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
    
    def add_random_word(self, meaning: Optional[str] = None) -> None:
        """
        Fetch and add a random word from the internet
        
        Args:
            meaning: Optional meaning (if not provided, will try to fetch from API)
        """
        print(f"{Colors.CYAN}Fetching random word...{Colors.END}")
        
        try:
            word_info = self.word_fetcher.fetch_random_word()
            word = word_info['word']
            
            # Use provided meaning or try to get from API
            if meaning:
                word_meaning = meaning
            else:
                word_meaning = word_info.get('definition')
                if not word_meaning:
                    # If no definition available, prompt user
                    print(f"\nWord: {Colors.BOLD}{word}{Colors.END}")
                    word_meaning = input(f"Enter meaning for '{word}': ").strip()
                    if not word_meaning:
                        print(f"{Colors.WARNING}No meaning provided, skipping.{Colors.END}")
                        return
            
            # Add the word
            self.add_word(
                word=word,
                meaning=word_meaning,
                tags=['random', word_info['source']]
            )
            
            print(f"{Colors.GREEN}✓ Added random word from {word_info['source']}{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.FAIL}Failed to fetch random word: {e}{Colors.END}")
    
    def discover_words(self, count: int = 3) -> None:
        """
        Discover multiple random words and let user choose which to add
        
        Args:
            count: Number of random words to fetch
        """
        print(f"{Colors.CYAN}Discovering {count} random words...{Colors.END}")
        
        try:
            words = self.word_fetcher.fetch_multiple_words(count)
            
            for i, word_info in enumerate(words, 1):
                print(f"\n{Colors.HEADER}Word #{i}{Colors.END}")
                print(f"{Colors.BOLD}{word_info['word']}{Colors.END}")
                
                if word_info.get('definition'):
                    print(f"Definition: {word_info['definition']}")
                
                print(f"Source: {word_info['source']}")
                
                response = input("Add this word? (y/n): ").lower()
                if response == 'y':
                    meaning = word_info.get('definition')
                    if not meaning:
                        meaning = input(f"Enter meaning for '{word_info['word']}': ").strip()
                    
                    if meaning:
                        self.add_word(
                            word=word_info['word'],
                            meaning=meaning,
                            tags=['discovered', word_info['source']]
                        )
                    else:
                        print(f"{Colors.WARNING}Skipped - no meaning provided{Colors.END}")
                else:
                    print("Skipped.")
            
        except Exception as e:
            print(f"{Colors.FAIL}Failed to discover words: {e}{Colors.END}")
    
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
                    play_sound: bool = False,
                    include_random: bool = False) -> None:
        """
        Run an interactive test session
        
        Args:
            num_words: Number of words to test (None for all)
            play_sound: Whether to play sounds
            include_random: Whether to include random words from internet
        """
        test_words = []
        
        # Add existing words
        if self.db.words:
            words = list(self.db.words.keys())
            random.shuffle(words)
            test_words.extend(words)
        
        # Add random words if requested
        if include_random:
            print(f"{Colors.CYAN}Fetching random words for testing...{Colors.END}")
            try:
                random_count = min(5, num_words or 5)
                random_words = self.word_fetcher.fetch_multiple_words(random_count)
                for word_info in random_words:
                    test_words.append(word_info['word'])
            except Exception as e:
                print(f"{Colors.WARNING}Failed to fetch random words: {e}{Colors.END}")
        
        if not test_words:
            print(f"{Colors.WARNING}No words to test!{Colors.END}")
            return
        
        # Limit number of words if specified
        if num_words:
            test_words = test_words[:min(num_words, len(test_words))]
        
        total = len(test_words)
        correct = 0
        
        print(f"\n{Colors.HEADER}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}Starting test session with {total} words{Colors.END}")
        print(f"{Colors.HEADER}{'='*50}{Colors.END}\n")
        
        for i, word in enumerate(test_words, 1):
            # Get meaning from database or prompt
            if word in self.db.words:
                entry = self.db.words[word]
                meaning = entry.meaning
                is_random = False
            else:
                meaning = "(random word - no definition in dictionary)"
                is_random = True
            
            print(f"\n{Colors.CYAN}Word {i}/{total}{Colors.END}")
            if is_random:
                print(f"{Colors.WARNING}[Random Word]{Colors.END}")
            print(f"Meaning: {meaning}")
            
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
        
        # Source statistics (from tags)
        source_tags = [tag for tag in all_tags if tag in ['random', 'discovered', 'fallback']]
        source_counts = {source: source_tags.count(source) for source in set(source_tags)}
        
        print(f"\n{Colors.HEADER}📊 Vocabulary Statistics{Colors.END}")
        print(f"{'='*40}")
        print(f"Total words: {total}")
        print(f"Words with CJK characters: {cjk_count}")
        print(f"Average word length: {avg_length:.1f} characters")
        
        if source_counts:
            print(f"\n{Colors.CYAN}Sources:{Colors.END}")
            for source, count in source_counts.items():
                print(f"  {source}: {count}")
        
        if tag_counts:
            print(f"\n{Colors.CYAN}Tags:{Colors.END}")
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
                if tag not in ['random', 'discovered', 'fallback']:
                    print(f"  {tag}: {count}")
        
        # Show sample of words
        print(f"\n{Colors.CYAN}Sample words:{Colors.END}")
        sample = random.sample(list(self.db.words.keys()), min(5, total))
        for word in sample:
            entry = self.db.words[word]
            tag_str = f" [{', '.join(entry.tags)}]" if entry.tags else ""
            print(f"  • {word}: {entry.meaning}{tag_str}")
    
    def run_interactive(self) -> None:
        """Run interactive command-line interface"""
        help_text = f"""
{Colors.HEADER}Vocabulary Learning Tool - Commands{Colors.END}
{Colors.BOLD}{'='*50}{Colors.END}

  {Colors.GREEN}add|a <word> <meaning> [tags]{Colors.END}
        Add a new word (tags separated by commas)
        Example: a hello 你好 greeting,common

  {Colors.GREEN}random|rand [meaning]{Colors.END}
        Fetch and add a random word from the internet
        Example: rand - adds random word (prompts for meaning if needed)

  {Colors.GREEN}discover|d [count]{Colors.END}
        Discover multiple random words and choose which to add
        Example: discover 5

  {Colors.GREEN}search|s <pattern> [-r]{Colors.END}
        Search for words (-r for regex)
        Example: s ^hello -r

  {Colors.GREEN}show|w <word> [-s]{Colors.END}
        Display a word (-s to play sound)

  {Colors.GREEN}test|t [number] [-s] [--random]{Colors.END}
        Start a test session (--random to include random words)

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

  {Colors.GREEN}delete|del <word>{Colors.END}
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
                
                elif cmd in ['random', 'rand']:
                    meaning = parts[1] if len(parts) > 1 else None
                    self.add_random_word(meaning)
                
                elif cmd in ['discover', 'd']:
                    count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 3
                    self.discover_words(count)
                
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
                            entry = self.db.words[word]
                            tag_str = f" [{', '.join(entry.tags)}]" if entry.tags else ""
                            print(f"  • {word}: {entry.meaning}{tag_str}")
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
                    include_random = '--random' in parts
                    self.test_session(num_words, play_sound, include_random)
                
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
                
                elif cmd in ['delete', 'del']:
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
    parser.add_argument('--random', action='store_true', 
                       help='Fetch and display a random word')
    parser.add_argument('--discover', type=int, metavar='COUNT',
                       help='Discover multiple random words')
    parser.add_argument('-s', '--search', help='Search for a word and exit')
    parser.add_argument('--stats', action='store_true', help='Show statistics and exit')
    
    args = parser.parse_args()
    
    app = VocabularyApp(args.file)
    
    if args.random:
        word_info = app.word_fetcher.fetch_random_word()
        print(f"Random word: {word_info['word']}")
        if word_info.get('definition'):
            print(f"Definition: {word_info['definition']}")
        print(f"Source: {word_info['source']}")
    elif args.discover:
        words = app.word_fetcher.fetch_multiple_words(args.discover)
        for i, word_info in enumerate(words, 1):
            print(f"{i}. {word_info['word']} [{word_info['source']}]")
            if word_info.get('definition'):
                print(f"   {word_info['definition']}")
    elif args.add:
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