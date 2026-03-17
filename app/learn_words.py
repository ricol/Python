#!/usr/bin/env python3
import os
import re
import random
import threading
import subprocess
import sys

LENGTH_LINE = 80

def is_chinese(char):
    """Check if a character is Chinese (CJK Unified Ideographs)"""
    return '\u4e00' <= char <= '\u9fff'

class MyLibrary:
    DEFAULT_FILE_NAME = "./words.dat"

    def __init__(self, filename=None):
        self.data = {}
        if filename is None:
            filename = self.DEFAULT_FILE_NAME
        self.load(filename)

    def save(self, filename=None):
        if filename is None:
            filename = self.DEFAULT_FILE_NAME
        with open(filename, "w", encoding='utf-8') as file:
            for key, value in self.data.items():
                if value:
                    file.write(f"{key}|{value}\n")
            print(f"#dictionary saved to {filename}")

    def load(self, filename=None):
        if filename is None:
            filename = self.DEFAULT_FILE_NAME
        if os.path.exists(filename):
            with open(filename, "r", encoding='utf-8') as file:
                content = file.readlines()
                for line in content:
                    line = line.rstrip('\n')
                    parts = line.split("|")
                    if len(parts) >= 2:
                        self.add(parts[0], parts[1])
            print(f"#dictionary loaded from {filename}")
            print(f"#total: {len(self.data)}")
        else:
            print(f"##{filename} doesn't exist.")

    def add(self, word, meaning):
        if word and meaning:
            self.data[word] = meaning
            print(f"##{word}: {meaning} added.")

    def remove(self, word):
        if not word:
            return
        if word in self.data:
            del self.data[word]
            print(f"##{word} removed.")
        else:
            print(f"##{word} not found!")

    def clear(self):
        self.data = {}
        print("#dictionary cleared.")

    def search_word(self, pattern):
        if not pattern:
            return None
        try:
            r = re.compile(pattern)
            for word in self.data.keys():
                if r.search(word):
                    return word
        except Exception as e:
            print(f"exception: {e}")
            return None
        return None

    def get_word(self, total=None):
        if total is None:
            total = len(self.data)
        data = list(self.data.keys())
        random.shuffle(data)
        index = 0
        for word in data:
            index += 1
            yield word, index
            if index >= total:
                break

    def format_text(self, character, word, length, character_type=1):
        s = ""
        index = 0
        length_of_word = 0
        for c in word:
            length_of_word += 1
            if is_chinese(c):
                length_of_word += 1
        
        left = (length - length_of_word) // 2 - 1
        s += character
        index += 1
        
        new_character = character
        if character_type != 1:
            new_character = " "
        
        for _ in range(left - 1):
            s += new_character
            index += 1
        
        s += word
        index += length_of_word
        
        while index < length - 1:
            s += new_character
            index += 1
        
        s += character
        return s

    def show_word(self, word, play=False):
        length = LENGTH_LINE
        print(self.format_text("=", "WORD", length))
        print(self.format_text("=", word, length, 2))
        print(self.format_text("=", self.data[word], length, 2))
        print(self.format_text("=", "", length))
        if play:
            self.say(word)

    def say(self, word):
        cmd = f"say {word}"
        thread = threading.Thread(target=lambda: subprocess.run(cmd, shell=True))
        thread.start()

    def test(self, total, sound=0):
        if total:
            try:
                total = int(total)
            except ValueError:
                total = len(self.data)
        else:
            total = len(self.data)
        
        print("begin.")
        for aWord, index in self.get_word(total):
            self.show_word(aWord, sound == 1)
            print(f"{index}/{total}")
            print("#? <quit to exit>")
            response = input().strip().lower()
            
            while response != aWord and response != "quit":
                print("#wrong!")
                if sound == 1:
                    self.say("you are wrong!")
                self.show_word(aWord)
                print("#again? <quit to exit>")
                response = input().strip().lower()
            
            if response == "quit":
                return
            print("#greate! next.")
        print("complete.")

    def __str__(self):
        s = ""
        for key, value in self.data.items():
            if value:
                s += f"{key}: {value}\n"
        return s

    def run(self):
        doc = """Menu:
==============================================
  i [word] [meaning] - insert a new word
  r [word]           - remove a word
  s [filename]       - save to a local file
  l [filename]       - load from a local file
  d [pattern] [-s]   - display a word
  a                  - display all words
  c                  - clear all words in the memory
  t [total]          - run words test
  q                  - quit
==============================================
Your command?
"""
        while True:
            print(doc)
            response = input()
            response = response.rstrip('\n')
            commands = response.split()
            
            if not commands:
                continue
                
            if commands[0] == "s":
                filename = commands[1] if len(commands) > 1 else None
                self.save(filename)
            
            elif commands[0] == "l":
                filename = commands[1] if len(commands) > 1 else None
                self.load(filename)
            
            elif commands[0] == "c":
                self.clear()
            
            elif commands[0] == "d":
                if len(commands) > 1:
                    word = self.search_word(commands[1])
                    bSay = len(commands) > 2 and commands[2] == "-s"
                    if word:
                        self.show_word(word, bSay)
                    else:
                        print("#word not found!")
                else:
                    print("#command not complete!")
            
            elif commands[0] == "a":
                print(f"#dictionary: \n{self}")
                print(f"#total: {len(self.data)}")
            
            elif commands[0] == "t":
                total = commands[1] if len(commands) > 1 else None
                sound = commands[2] if len(commands) > 2 else 0
                try:
                    sound = int(sound)
                except ValueError:
                    sound = 0
                self.test(total, sound)
            
            elif commands[0] == "q":
                return
            
            elif commands[0] == "i":
                if len(commands) >= 3:
                    word = commands[1]
                    meaning = commands[2]
                    self.add(word, meaning)
                else:
                    print("#command not complete!")
            
            elif commands[0] == "r":
                if len(commands) > 1:
                    self.remove(commands[1])
                else:
                    print("#command not complete!")
            
            else:
                print("#invalid command!")


if __name__ == "__main__":
    library = MyLibrary()
    library.run()