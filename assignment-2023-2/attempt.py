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
    # print(g)
    return g

def interval_grafs_lexbfs(g):
    nodes = set(g.keys())
    s = []
    s.append(sorted(nodes))
    lexbfs = []
    # print(lexbfs, s, type(nodes))

    while len(s) != 0:
        if not s[0]:
            s.remove(s[0])
            #print("empty")
        else:

            visit = s[0].pop(0)
            nodes.remove(visit)
            lexbfs.append(visit)
            #print(lexbfs, s, nodes)
            # if not s[0]:
            #     s.remove(s[0])

            neighbors = set(g[visit]) & nodes
            
            same_set = []
            for i in range(len(s)):
                #print(len(s))
                if neighbors & set(s[i]) and neighbors:
                    bucket = []
                    collect = sorted(neighbors & set(s[i]))
                    #not_neighbors = sorted(set(s[i]) - neighbors)
                    bucket.append(collect)
                    bucket.append(i)
                    # print(collect, neighbors)
                    # same_set.append(collect)
                    # same_set.append(i)
                    for j in range(len(collect)):
                        s[i].remove(collect[j])
                    same_set.append(bucket)
            # print(same_set)       
            if len(same_set) == 1:
                s.insert(same_set[0][1], same_set[0][0])
            else:
                while len(same_set) != 0:
                    s.insert(same_set[-1][1], same_set[-1][0])
                    same_set.pop(-1)

            for empty in s:
                if len(empty) == 0:
                    s.remove(empty)
        # print(lexbfs, s)
    return lexbfs


def interval_graphs_chordal(g): 
    lexbfs = interval_grafs_lexbfs(g)
    lexbfs.reverse()
    # print(lexbfs)
    nodes = set(g.keys())
    for i in range(len(lexbfs)):
        nodes.remove(lexbfs[i])
        neighbors_of_u = set(g[lexbfs[i]]) & nodes
        # print(neighbors_of_u)
    
        if neighbors_of_u:
            first_index = min(lexbfs.index(x) for x in neighbors_of_u)
            first_neighbor_of_u = lexbfs[first_index]
            slice = lexbfs[first_index+1:]
            neighbors_of_w = set(g[first_neighbor_of_u]) & set(slice)
            neighbors_of_u.remove(first_neighbor_of_u)

        if not neighbors_of_u.issubset(neighbors_of_w):
            chordal = neighbors_of_u.issubset(neighbors_of_w)
            break
        else:
            chordal = neighbors_of_u.issubset(neighbors_of_w)

    return chordal
#print(neighbors_of_u.issubset(neighbors_of_w))

def interval_graphs_bfs(g, node):
    
    q = deque()
    bfs = []
    
    visited = [ False ] * len(g)
    inqueue = [ False ] * len(g)
    
    q.appendleft(node)
    inqueue[node] = True
    
    while not (len(q) == 0):
        # print("Queue", q)
        c = q.pop()
        bfs.append(c)
        # print("Visiting", c)
        inqueue[c] = False
        visited[c] = True
        for v in g[c]:
            if not visited[v] and not inqueue[v]:
                q.appendleft(v)
                inqueue[v] = True
                
    return bfs, visited

# Read given file to form the graph g
g = read_file(args.input_filename)

if sys.argv[1] == "lexbfs":
    # print(g)
    # Calling the function for graph g to return it's lexicographic BFS
    lexbfs = interval_grafs_lexbfs(g)
    print(lexbfs)

if sys.argv[1] == "chordal":
    # print(g)
    # Calling the function for graph g to return if it's chordal
    chordal = interval_graphs_chordal(g)
    print(chordal)

if sys.argv[1] == "interval":    
    print(g)
    nodes = sorted(g.keys())
    node = nodes.pop(0)
    # print(type(node))
    # Calling the function for graph g to return it's BFS
    bfs, visited = interval_graphs_bfs(g, node)
    print(bfs)
    
    for i in range(len(bfs)):
        new_dict = {}
        u_with_neighbors = set(g[bfs[i]])
        u_with_neighbors.add(bfs[i])
        components_of_u = set(bfs) - u_with_neighbors
        new_graph = sorted(components_of_u)
        # print(new_graph)
        for x in new_graph:
            new_dict[x] = [y for y in g[x] if y not in sorted(u_with_neighbors)]
        nodes_ = sorted(new_dict.keys())
        node_ = nodes_.pop(0)
        new_bfs, new_visited = interval_graphs_bfs(new_dict, node_)
        print(new_visited)
        
        # for y in sorted(u_with_neighbors):
        #         if y not in g[x]:
            # if y in new_dict.values():
            #     new_dict.values(y)
        print(new_dict)
        # print(neighbors_of_u)
        # print(u_with_neighbors)
        # print(set(g[bfs[i]]))
        # print(components_of_u)
        # print(bfs)
        # removing = g.pop(bfs[i])
        # new_dict = {}
        # for key, value in g.items():
        #     if key != bfs[i]:
        #         new_dict[key] = [value]
        # for value in new_dict.values():
        #     if value != bfs[i]:
        #         new_dict[key] = value
        #             # new_dict[key] = value
        # print(new_dict)
        # new_dict = {for x, y in g.items() if x, y != bfs[i]}
        # del g[bfs[i]]
        # nodes_ = sorted(g.keys())
        # node_ = nodes_.pop(0)
        # bfs_, visited_ = interval_graphs_bfs(g, node_)
        # print(bfs_, visited_)
        

