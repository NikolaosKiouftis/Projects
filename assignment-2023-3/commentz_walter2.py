import argparse
import sys
from collections import deque


parser = argparse.ArgumentParser(description='Commentz-Walter algorithm')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='verbose mode')
parser.add_argument('kw', metavar='keyword', type=str,
                    help='keyword', nargs='+')
parser.add_argument('input_filename', metavar='input_filename',
                    type=str, help='input filename')

args = parser.parse_args()


def read_file(file):
    with open(file, 'r') as f:
        return f.read()


class TrieNode:
    index = 0

    def __init__(self):
        self.children = {}
        self.end_of_word = False
        self.index = TrieNode.index
        self.depth = 0
        self.parent = None
        TrieNode.index += 1

    # def __str__(self):
    #     return str(self.children) + str(self.end_of_word) + str(self.index)


class Trie:
    nodes = []

    def __init__(self):
        self.root = TrieNode()
        Trie.nodes.append(self.root)

    # def __str__(self):
    #     def print_node(node):
    #         for key in node.children:
    #             print(
    #                 key, node.children[key].index, node.children[key].depth, node.children[key].end_of_word)
    #             print_node(node.children[key])
    #     print_node(self.root)
    #     return ''

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

    def get_node_by_index(self, index):
        return Trie.nodes[index]


def trie_creation(reversed_kw):
    trie = Trie()
    for word in reversed_kw:
        trie.insert(word)
    return trie


data = read_file(args.input_filename).strip()
pmin = len(min(args.kw, key=len))
kw = [word.strip() for word in args.kw]

reversed_kw = [word[::-1] for word in kw]

trie = trie_creation(reversed_kw)


def rt_table_creation(patterns):
    rts = []
    alphabet = set('*')
    for pattern in patterns:
        rt_table = {}
        alphabet = alphabet.union(set(pattern))
        for i in range(len(pattern) - 1):
            rt_table[pattern[i]] = len(pattern) - i - 1
        if pattern[-1] not in rt_table:
            rt_table[pattern[-1]] = len(pattern) - 1
        rt_table['*'] = len(pattern)
        rts.append(rt_table)

    median = {}
    for rt in rts:
        for key in alphabet:
            if key not in median:
                if key in rt:
                    median[key] = [rt[key]]
                else:
                    median[key] = [rt['*']]
            else:
                if key in rt:
                    median[key].append(rt[key])
                else:
                    median[key].append(rt['*'])

    for key in median:
        median[key] = sum(median[key]) // len(median[key])

    return median


rt_table = rt_table_creation(kw)


def failure_creation(trie):
    failure = [i for i in range(TrieNode.index)]
    # Set the failure of the root and his children to the root
    for c in trie.root.children:
        failure[trie.root.children[c].index] = trie.root.index

    queue = deque()
    queue.append(trie.root)
    # Do a BFS on the trie
    while queue:
        # current node is u
        u = queue.popleft()
        for c in u.children:
            v = u.children[c]
            queue.append(v)
            w = trie.get_node_by_index(failure[u.index])
            while w != trie.root and c not in w.children:
                w = trie.get_node_by_index(failure[w.index])
            if c in w.children and u != trie.root:
                failure[v.index] = w.children[c].index
            else:
                failure[v.index] = trie.root.index

    return failure


failure = failure_creation(trie)


def create_set1(failure):
    set1 = [None] * len(failure)

    for u in range(len(failure)):
        set1[u] = set()
        for i, v in enumerate(failure):
            if v == u:
                set1[u].add(i)
    return set1


set1 = create_set1(failure)


def create_set2(set1):
    set2 = [None] * len(set1)
    for u in range(len(set1)):
        set2[u] = set()
        for v in set1[u]:
            node = trie.get_node_by_index(v)
            if node.end_of_word:
                set2[u].add(v)
    return set2


set2 = create_set2(set1)


def k_depth_diff(current_set, u, trie):
    diffs = []
    parent = trie.get_node_by_index(u)
    for v in current_set[u]:
        child = trie.get_node_by_index(v)
        diffs.append(child.depth - parent.depth)
    return diffs


def create_s1(set1, pmin, trie):
    s1 = [None] * len(set1)
    for u in range(len(set1)):
        if u == 0:
            s1[u] = 1
        else:
            diffs = k_depth_diff(set1, u, trie)
            diffs.append(pmin)
            s1[u] = min(diffs)
    return s1


s1 = create_s1(set1, pmin, trie)


def create_s2(set2, pmin, trie):
    s2 = [None] * len(set2)
    for u in range(len(set2)):
        if u == 0:
            s2[u] = pmin
        else:
            diffs = k_depth_diff(set2, u, trie)
            node = trie.get_node_by_index(u)
            diffs.append(s2[node.parent.index])
            s2[u] = min(diffs)
    return s2


s2 = create_s2(set2, pmin, trie)

if args.verbose:
    for i in range(len(set1)):
        print(f"{i}: {s1[i]},{s2[i]}")


def commentz_walter(data, trie, pmin, rt, s1, s2):
    q = deque()
    i = pmin - 1
    j = 0
    u = trie.root
    m = ''
    while i < len(data):
        while data[i-j] in u.children:
            u = u.children[data[i-j]]
            m = m + data[i-j]
            j += 1
            if u.end_of_word:
                q.append((m[::-1], i-j+1))
        if j > i:
            j = i
        s = min(s2[u.index], max(s1[u.index], rt[data[i-j]] - j - 1))
        i += s
        j = 0
        u = trie.root
        m = ''
    return q


q = commentz_walter(data, trie, pmin, rt_table, s1, s2)

for i in q:
    print(f'{i[0]}: {i[1]}')
