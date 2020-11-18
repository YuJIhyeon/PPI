import pandas as pd
import numpy as np
import math

# gene_id : 버텍스들의 집합
def initial_data(filename):
    input_file = open(filename, 'r')
    adjacent_vertex = dict()
    gene_id = set()
    for line in input_file:
        for value in line.split():
            gene_id.add(value)

    gene_id = list(gene_id)
    gene_id.sort()

    zero_graph = np.zeros((len(gene_id), len(gene_id)), dtype=int)
    original_graph = pd.DataFrame(zero_graph, index=gene_id, columns=gene_id)

    # 원본 그래프 만들기.
    # 그래프는 알파벳 순으로 만들어졌다.
    input_file = open(filename, 'r')
    for line in input_file:
        con = line.split()
        original_graph._set_value(con[0], con[1], 1)
        original_graph._set_value(con[1], con[0], 1)

        if adjacent_vertex.get(con[0]) == None: adjacent_vertex[con[0]] = con[1]
        else: adjacent_vertex[con[0]] = adjacent_vertex[con[0]] + "," + con[1]

        if adjacent_vertex.get(con[1]) == None: adjacent_vertex[con[1]] = con[0]
        else: adjacent_vertex[con[1]] = adjacent_vertex[con[1]] + "," + con[0]

    return original_graph, adjacent_vertex, gene_id


def output_to_file(filename):
    file = open(filename, 'w')

    file.close()

def make_weight_graph(original_graph, adjacent_vertex, gene_id):
    initial_graph = np.array([-1] * len(gene_id)*len(gene_id)).reshape(len(gene_id), len(gene_id))
    weight_graph = pd.DataFrame(initial_graph, index=gene_id, columns=gene_id)

    for base_ver in gene_id:
        adj = adjacent_vertex[base_ver].split(',')
        base_degree = original_graph.__getitem__(base_ver).sum()
        for adj_ver in adj:
            adj_degree = original_graph.__getitem__(adj_ver).sum()
            if weight_graph._get_value(base_ver, adj_ver) == -1:
                if base_degree == 1 or adj_degree == 1:
                    weight_graph._set_value(base_ver, adj_ver, 0)
                    weight_graph._set_value(adj_ver, base_ver, 0)
                else:
                    weight_graph._set_value(base_ver, adj_ver, abs(base_degree - adj_degree))
                    weight_graph._set_value(adj_ver, base_ver, abs(base_degree - adj_degree))

    return weight_graph


# The main function
def main():
    input_filename = 'test.txt'
    original_graph, adjacent_vertex, gene_id = initial_data(input_filename)
    weight_graph = make_weight_graph(original_graph, adjacent_vertex, gene_id)
    print(original_graph)
    print()
    print(weight_graph)
    pass
    # 결과 값 출력 ------------
    #output_filename = 'result.txt'
    #output_to_file(output_filename)



if __name__ == '__main__':
    main()