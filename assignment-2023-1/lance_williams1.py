import argparse
import sys

# Set arguments of the program
parser = argparse.ArgumentParser()
parser.add_argument("method", type=str, help="name of method being used")
parser.add_argument("input_filename", type=argparse.FileType("r"), help="name of data file.txt")

args = parser.parse_args()

# Check for the name of the method in arguments
if sys.argv[1] not in ["single", "complete", "average", "ward"]:
    sys.exit("Wrong name of method used. Please try again")

# Function to open file and extract data in a list of lists with single element
def read_file(file):
    data = []
    with args.input_filename as file:
        for line in file:
            a = [int(x) for x in line.split()]
            for item in a:
                b = [item]
                data.append(b)

    return sorted(data)

# Read file with data and create a list with the length of each element of the data
data = read_file(args.input_filename)
data_len = [1]*len(data)

# Initialize a square matrix in the size of our data 
dist = [[0 for _ in range(len(data))] for _ in range(len(data))]

# Pass the distances between the elements of our data, in the square matrix
for i in range(len(data)):
    for j in range(len(data)):
        dist[i][j] = float(abs(data[i][0] - data[j][0]))

# Function to find minimum distance in a square matrix
# Finds the first pair of the square matrix with the minimum distance which is called similarity
# Returns: the indexes of the minimum distance in the square matrix, the minimum distance is called best
# and the cluster to be created from two parts
def similarity_pair(dist):
    best = float("inf")
    for i in range(len(dist)):
        for j in range(len(dist)):
            if dist[i][j] > 0 and dist[i][j] < best:
                best = dist[i][j]
                similarity_i = i
                similarity_j = j
    part1 = data[similarity_i]
    part2 = data[similarity_j]
    cluster = part1 + part2
    
    return similarity_i, similarity_j, best, part1, part2, cluster


# Function to find distance between created cluster and the other elements of the data, according to method being used
# Returns the updated square matrix with the distances
def new_distance(dist, similarity_i, similarity_j, best, part1, part2, data_len):
    if sys.argv[1] == "single":
        a1, a2, b1, c = 1/2, 1/2, 0, -1/2

    if sys.argv[1] == "complete":
        a1, a2, b1, c = 1/2, 1/2, 0, 1/2

    if sys.argv[1] == "average":
        a1, a2, b1, c = len(part1)/(len(part1) + len(part2)), len(part2)/(len(part1) + len(part2)), 0, 0
    
    if sys.argv[1] == "ward":

        for i in range(len(data_len)):
            if i != similarity_i:
                x = data_len[i]
                print(x)

        for i in range(len(dist)):
            if similarity_i != i:
                a1 = (len(part1)+x)/(len(part1)+x+len(part2))
                a2 = (len(part2)+x)/(len(part1)+x+len(part2))
                b1 = -x/(len(part1)+x+len(part2))
                dist[similarity_i][i] = a1 * dist[similarity_i][i] + a2 * dist[similarity_j][i] + b1 * best + abs(dist[similarity_i][i] - dist[similarity_j][i])
            else:
                dist[similarity_i][i] = 0

            dist[i][similarity_i] = dist[similarity_i][i]
        for i in range(len(dist)):
            del(dist[i][similarity_j])
        dist.remove(dist[similarity_j])
    else:
        for i in range(len(dist)):
            if similarity_i != i:
                dist[similarity_i][i] = a1 * dist[similarity_i][i] + a2 * dist[similarity_j][i] + b1 * best + c * abs(dist[similarity_i][i] - dist[similarity_j][i])   
            else:
                dist[similarity_i][i] = 0

            dist[i][similarity_i] = dist[similarity_i][i]

        for i in range(len(dist)):
            del(dist[i][similarity_j])
        dist.remove(dist[similarity_j])

    return dist

# Function to update data list with the new cluster created
# and to updata data_len, the list with the length of each element
def join_cluster(cluster, similarity_i, similarity_j, data_len):
    if len(data) > 1:
        data.remove(data[similarity_i])
        data.insert(similarity_i, cluster)
        data.remove(data[similarity_j])
        data_len.remove(data_len[similarity_i])
        data_len.insert(similarity_i, len(cluster))
        data_len.remove(data_len[similarity_j])

    return data, data_len

# Call functions to run program
while len(data) > 1:
    similarity_i, similarity_j, best, part1, part2, cluster = similarity_pair(dist)
    new_distance(dist, similarity_i, similarity_j, best, part1, part2, data_len)
    join_cluster(cluster, similarity_i, similarity_j, data_len)
    print("("+str(part1).strip("[]")+")" "("+str(part2).strip("[]")+")", format(best, ".2f"), len(cluster))
    