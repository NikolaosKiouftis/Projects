import argparse

parser = argparse.ArgumentParser()
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()
answer = args.x**args.y
if args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print(answer)