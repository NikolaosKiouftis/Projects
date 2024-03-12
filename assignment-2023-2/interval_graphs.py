import argparse
import sys
from collections import deque

# Set arguments of the program
parser = argparse.ArgumentParser()
parser.add_argument("task", type=str, help="name of task to be executed")
parser.add_argument("input_filename", type=argparse.FileType("r"), help="name of the file.txt describing the graph")

args = parser.parse_args()

# Check for the name of the task in arguments
if sys.argv[1] not in ["lexbfs", "chordal", "interval"]:
    print("Wrong name of task. Please try again")
    raise SystemExit(1)
    
# Function to open file and extract data in a dictionary that represent a graph
def read_file(graph_input):
    g = {}
    with args.input_filename as graph_input:
        for line in graph_input:
            # Split line and convert line parts to integers.
            nodes = [int(x) for x in line.split()]
            if len(nodes) != 2:
                continue
            # If a node is not already in the graph
            # we must create a new empty list.
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            # We need to append the "to" node
            # to the existing list for the "from" node.
            g[nodes[0]].append(nodes[1])
            # And also the other way round.
            g[nodes[1]].append(nodes[0])
    
    return g

# Function for given input a graph and returns lexicographic BFS order 
def interval_grafs_lexbfs(g):
    # Set with all the nodes of the graph
    nodes = set(g.keys())
    # List "s" containing the sorted list of no visited nodes
    # for the partition of lists, to neighbors and no neighbors
    s = []
    s.append(sorted(nodes))
    # list for the ordering of lexBFS
    lexbfs = []
    # Until no, no visited nodes left in list "s"
    while len(s) != 0:
        # If the first list of "s" is empty, remove it
        if not s[0]:
            s.remove(s[0])
        # If the first list of "s" is not empty
        else:
            # Remove the first node, of first list, in list "s", as visiting
            visit = s[0].pop(0)
            # Remove the visiting node from the set of nodes
            # We need to have a set with the non visited nodes
            nodes.remove(visit)
            # Add visiting node in ordering list of lexbfs
            lexbfs.append(visit)
            # Set of non visited neigbors of visiting node
            neighbors = set(g[visit]) & nodes
            # List to hold all non visited neighbors of visiting node
            # and the index of the list they belong in "s"
            neighbor_position = []
            for i in range(len(s)):
                # If the visiting node has non visited neighbors (to ignore empty set)
                # and if exists common elements between non visited neighbors and current list in "s"
                if neighbors & set(s[i]) and neighbors:
                    # list to hold non visited neighbors from the current list in "s"
                    # and the index of current list in "s"
                    in_same_list = []
                    # Sorted list of non visited neighbors which they belong in the current list in "s"
                    collected = sorted(neighbors & set(s[i]))
                    # Append the collected neighbors
                    in_same_list.append(collected)
                    # Append the index of current list
                    in_same_list.append(i)
                    # Removing the non visited neighbors from the current list in "s"
                    for j in range(len(collected)):
                        s[i].remove(collected[j])
                    # Append the list that holds the non visited neighbors found in the current list
                    # and the index of the current list in "s"
                    # to the list that holds the non visited neighbors of the visiting node
                    # and the index of the list they belong in "s"
                    neighbor_position.append(in_same_list)
            # If the visiting node has all non visited neighbors in one list in "s"
            if len(neighbor_position) == 1:
                # Insert the non visited neighbors list before the list they were found in "s"
                s.insert(neighbor_position[0][1], neighbor_position[0][0])
            # If the visiting node has non visited neighbors in different lists in "s"
            else:
                while len(neighbor_position) != 0:
                    # Insert the non visited neighbors lists before the lists they were found in "s"
                    # starting from the end of the list "s"
                    s.insert(neighbor_position[-1][1], neighbor_position[-1][0])
                    # Removing from list the non visited neighbors list after positioning in "s"
                    neighbor_position.pop(-1)
            # Removing lists got empty, in "s"
            for empty in s:
                if len(empty) == 0:
                    s.remove(empty)
    
    return lexbfs

# Function for given input a graph and returns if it's chordal
def interval_graphs_chordal(g):
    # Calling the function for graph "g" to return it's lexicographic BFS
    lexbfs = interval_grafs_lexbfs(g)
    # reverse it
    lexbfs.reverse()
    # Set with all the nodes of the graph
    nodes = set(g.keys())
    # For every node in reversed lexicographic BFS
    for i in range(len(lexbfs)):
        # Remove the first node in reversed order of LexBFS from the set with all nodes
        nodes.remove(lexbfs[i])
        # Finding the neighbors of the node, from the right side of the node in reversed LexBFS
        neighbors_of_u = set(g[lexbfs[i]]) & nodes
        # If the node has neighbors
        if neighbors_of_u:
            # Finding the index of closest neighbor of node in reversed LexBFS
            first_index = min(lexbfs.index(x) for x in neighbors_of_u)
            # The closest neighbor of node in reversed LexBFS
            first_neighbor_of_u = lexbfs[first_index]
            # Get the rest of the nodes, after the closest neighbor of node in reversed LexBFS
            slice = lexbfs[first_index+1:]
            # Finding the neighbors of closest neighbor of node
            neighbors_of_w = set(g[first_neighbor_of_u]) & set(slice)
            # Remove the closest neighbor of node, from set with the neighbors of the node
            neighbors_of_u.remove(first_neighbor_of_u)
        # Check if it is or not a subset
        if not neighbors_of_u.issubset(neighbors_of_w):
            chordal = neighbors_of_u.issubset(neighbors_of_w)
            break
        else:
            chordal = neighbors_of_u.issubset(neighbors_of_w)
    
    return chordal

# Function for given input a graph and a starting node, to return its Breadth-First Search
def interval_graphs_bfs(g, node):
    
    q = deque()
    bfs = []
    
    visited = [ False ] * len(g)
    inqueue = [ False ] * len(g)
    
    q.appendleft(node)
    inqueue[node] = True
    
    while not (len(q) == 0):
        c = q.pop()
        bfs.append(c)
        inqueue[c] = False
        visited[c] = True
        for v in g[c]:
            if not visited[v] and not inqueue[v]:
                q.appendleft(v)
                inqueue[v] = True
                
    return bfs, visited

# Read given file to form the graph "g"
g = read_file(args.input_filename)

if sys.argv[1] == "lexbfs":
    # Calling the function for graph "g" to return it's lexicographic BFS
    lexbfs = interval_grafs_lexbfs(g)
    print(lexbfs)

if sys.argv[1] == "chordal":
    # Calling the function for graph "g" to return if it's chordal
    chordal = interval_graphs_chordal(g)
    print(chordal)

if sys.argv[1] == "interval":
    # Get a sorted list with the nodes of the graph
    nodes = sorted(g.keys())
    # Get the first node in the list as a starting node
    node = nodes.pop(0)
    # Calling the function for graph g to return it's BFS
    bfs, visited = interval_graphs_bfs(g, node)

    for i in range(len(bfs)):
        new_dict = {}
        u_with_neighbors = set(g[bfs[i]])
        u_with_neighbors.add(bfs[i])
        components_of_u = set(bfs) - u_with_neighbors
        new_graph = sorted(components_of_u)

        for x in new_graph: 
            new_dict[x] = g[x]
        
    # Initialize a square matrix in the size of our graph
    table_c = [[1 for _ in range(len(g))] for _ in range(len(g))]
