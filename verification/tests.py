import itertools as it
import math
import random
from string import ascii_letters as alphabet

from my_solution import on_same_path


def random_tree(nodes: list, nb_nodes: int):
    root = nodes.pop()
    childs = []
    if nb_nodes > 1:
        # Max 5 sub-trees.
        nb_childs = (random.choice(range(2, min(5, nb_nodes - 1) + 1))
                     if nb_nodes > 2 else 1)
        # Then childs are well distributed into the sub-trees.
        q, r = divmod(nb_nodes - 1, nb_childs)
        nbs = [q + (x < r) for x in range(nb_childs)]
        # assert sum(nbs) == nb_nodes - 1
        random.shuffle(nbs)
        for nb in nbs:
            if nb:
                childs.append(random_tree(nodes, nb))
    return root, childs


def random_input(nb_nodes):
    # Generate all nodes and all pairs.
    all_nodes = range(nb_nodes) if nb_nodes > 52 else alphabet[:nb_nodes]
    if nb_nodes > 52 and not random.randint(0, 2):
        all_nodes = map(str, all_nodes)
    all_nodes = list(all_nodes)
    if random.randint(0, 1):
        all_nodes.reverse()
    else:
        random.shuffle(all_nodes)
    all_pairs = list(it.combinations(all_nodes, 2))

    # Tree
    tree = random_tree(all_nodes, nb_nodes)

    # Pairs
    x = math.ceil(math.sqrt(nb_nodes))  # enough but not too much.
    x = min(len(all_pairs), x)  # just to be sure it's <= len(all_pairs)
    mini = min(len(all_pairs), 3)  # min 3 pairs (or the max)
    nb_pairs = random.randint(mini, max(mini, x))
    pairs = random.sample(all_pairs, nb_pairs)

    return tree, pairs


nb_nodes_for_random_tests = 10, 25, 33, 50, 100, 125, 250, 333, 500, 750, 1000

TESTS = {
    'Basic': [
        {'input': (
            ('Me', [('Daddy', [('Grandpa', []),
                               ('Grandma', [])]),
                    ('Mom', [('Granny', []),
                             ('?', [])])]),
            [('Grandpa', 'Me'), ('Daddy', 'Granny')],
         ),
         'answer': [True, False]},
        {'input': (
            (1, [(2, [(4, []),
                      (5, [(7, []),
                           (8, []),
                           (9, [])])]),
                 (3, [(6, [])])]),
            [(1, 5), (2, 9), (2, 6)],
         ),
         'answer': [True, True, False]},
        {'input': (
            (0, [(1, [(2, []),
                      (3, [])]),
                 (4, [(5, []),
                      (6, [])]),
                 (7, [(8, []),
                      (9, [])])]),
            [(4, 2), (0, 5), (2, 3), (9, 2), (6, 4), (7, 8), (8, 1)],
         ),
         'answer': [False, True, False, False, True, True, False]},
    ],
    'Extra': [
    ],
    'Random': [{'input': data, 'answer': on_same_path(*data)}
               for data in map(random_input, nb_nodes_for_random_tests)],
}


if __name__ == '__main__':
    from graphviz import Graph

    def render_tree(tree, filename):
        def graphviz_dfs(root, childs):
            G.node(repr(root))
            for node, sub_trees in childs:
                graphviz_dfs(node, sub_trees)
                G.edge(repr(root), repr(node))

        G = Graph(
            filename=filename,
            format='png',
            node_attr={
                'fontname': 'bold',
                'style': 'filled',
                'color': '#8FC7ED',
                'fontcolor': '#294270',
            },
            edge_attr={
                'color': '#294270',
                'penwidth': '3',
            },
        )
        graphviz_dfs(*tree)
        G.render()

    # category, index, filename = (
    #     'Random', -1, 'big'
    #     # 'Basic', 0, 'example'
    #     )
    # tree = TESTS[category][index]['input'][0]
    # render_tree(tree, filename)
    for cat, tests in TESTS.items():
        for n, test in enumerate(tests, 1):
            render_tree(test['input'][0], f'{cat.lower()}-{n}')
