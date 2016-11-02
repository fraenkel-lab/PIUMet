1) Input File Format

Input file contains parameter lambda, list of edges, and list of terminal nodes.

Lambda is a parameter used in clustering algorithm within MAT, and controls the size of clusters.
It can take continuous values in the range of [0, 1]. Closer to 0 is bigger the size of clusters,
possibly higher the execution time of algorithm, and better the solution quality in terms of objective value for PCST.

List of edges are provided in the following format:
E i j cij : Edge between i and j with cost of cij

List of terminal nodes are provided in the following format:
W i pi : Node i with prize pi

Example File: test2.txt
lambda 0.1
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

./mat_32core < test2.txt


3) Output txt file
Network 1
a c
c d
d f



