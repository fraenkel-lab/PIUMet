1) Input File Format

Input file contains list of edges and list of terminal nodes.

List of edges are provided in the following format:
E i j cij : Edge between i and j with cost of cij

List of terminal nodes are provided in the following format:
W i pi : Node i with prize pi

Example File: test1.txt
E a b 0.45
E a c 0.34
E b c 0.54
E c d 0.31
E d f 0.28
W a 0.6
W c 0.5
W d 0.7
W f 0.4

2) Usage

./mst_32core < test1.txt


3) Output
Tree
c d
a c
f d


