import argparse
import sys
from collections import deque

# Set arguments of the program
parser = argparse.ArgumentParser(description='Commentz-Walter algorithm for string matching')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
parser.add_argument('kw', type=str, help='keyword', nargs='+')
parser.add_argument('input_filename', type=argparse.FileType("r"), help='name of data file.txt')

args = parser.parse_args()

# Function to open file with the text
def read_file(file):
    with args.input_filename as file:
        return file.read()

# Read the given text
data = read_file(args.input_filename)

# A node in the trie structure
class TrieNode:
    index = 0
    # Function to assign values when the object is being created
    def __init__(self):
        self.children = {}
        self.end_of_word = False
        self.index = TrieNode.index
        self.depth = 0
        self.parent = None
        TrieNode.index += 1

# The trie object
class Trie:
    nodes = []

    # Function to assign values when the object is being created
    def __init__(self):
        self.root = TrieNode()
        Trie.nodes.append(self.root)

    # Insert a word into the trie
    def insert(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node.children:
                current_node.children[letter] = TrieNode()
                current_node.children[letter].depth = current_node.depth + 1
                current_node.children[letter].parent = current_node
                Trie.nodes.append(current_node.children[letter])
            current_node = current_node.children[letter]
        current_node.end_of_word = True


    def __str__(self):
        def print_node(node):
            for key in node.children:
                print(
                    key, node.children[key].index, node.children[key].depth, node.children[key].end_of_word)
                print_node(node.children[key])
        print_node(self.root)
        return ''

# The keywords given as input of the program
keywords = args.kw
reversed_keywords = [word[::-1] for word in keywords]

# Function to create the trie
def create_trie(reversed_keywords):
    trie = Trie()
    for word in reversed_keywords:
        trie.insert(word)
    return trie

# Create the trie
trie = create_trie(reversed_keywords)
# The length of the shortest keyword
pmin = len(min(args.kw, key=len))

print(trie)

# Function to find the chars from the keywords
def find_chars(keywords):
    chars = []
    for v in keywords:
        for u in v:
            if u not in chars:
                chars.append(u)
    return chars

# Function to create rightmost occurences table
def create_rt_table(trie, pmin, keywords):
    chars = find_chars(keywords)
    rt_table = {'*': pmin + 1}

    # Iterate throught the trie and find the depth 
    # of the first node that contains a character
    q = deque()
    q.append(trie.root)
    
    while not (len(q) == 0):
        u = q.pop()
        for c in u.children:
            q.appendleft(u.children[c])
            if c in chars and c not in rt_table: rt_table[c] = min(pmin +1  , u.children[c].depth)
    return rt_table

# Create the rt table
rt_table = create_rt_table(trie, pmin, keywords)

print(rt_table)

def create_failure(trie):
    pass

