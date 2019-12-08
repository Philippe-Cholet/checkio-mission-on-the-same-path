"""
Mission and solution inspired by
https://www.geeksforgeeks.org/check-if-two-nodes-are-on-same-path-in-a-tree/

Title: [typed] Timing a single DFS
"""

from typing import Dict, List, Tuple, Union
Node = Union[int, str]
Tree = Tuple[Node, List['Tree']]
Timings = Dict[Node, int]


def on_same_path(tree: Tree, pairs: List[Tuple[Node, Node]]) -> List[bool]:
    """For each given pair of tree's nodes, say if there are on a same path."""
    def timestamp(node: Node, times: Timings) -> None:
        # Note the time in `times` for the `node`.
        nonlocal timer
        timer += 1
        times[node] = timer

    def timed_dfs(root: Node, childs: List[Tree]) -> None:
        # DFS on the tree, with timestamps at each step.
        timestamp(root, intime)
        for child_tree in childs:
            timed_dfs(*child_tree)
        timestamp(root, outtime)

    def is_descendant_of(desc: Node, parent: Node) -> bool:
        # Is the node `desc` a descendant of the node `parent`? It is if we
        # find & quit `desc` after we find `parent` and before we quit `parent`.
        return intime[parent] < intime[desc] and outtime[desc] < outtime[parent]

    # We note arrival/departure times of all nodes during a DFS.
    timer: int = 0
    intime: Timings = {}
    outtime: Timings = {}
    timed_dfs(*tree)
    return [is_descendant_of(u, v) or is_descendant_of(v, u) for u, v in pairs]


if __name__ == '__main__':  # from python_3
    example = on_same_path(
        ('Me', [('Daddy', [('Grandpa', []),
                           ('Grandma', [])]),
                ('Mom', [('Granny', []),
                         ('?', [])])]),
        [('Grandpa', 'Me'), ('Daddy', 'Granny')],
    )
    print('Example: it should be [True, False].')
    print(list(example))

    TESTS = (
        (
            ('Me', [('Daddy', [('Grandpa', []),
                               ('Grandma', [])]),
                    ('Mom', [('Granny', []),
                             ('?', [])])]),
            [('Grandpa', 'Me'), ('Daddy', 'Granny')],
            [True, False],
        ),
        (
            (1, [(2, [(4, []),
                      (5, [(7, []),
                           (8, []),
                           (9, [])])]),
                 (3, [(6, [])])]),
            [(1, 5), (2, 9), (2, 6)],
            [True, True, False],
        ),
        (
            (0, [(1, [(2, []),
                      (3, [])]),
                 (4, [(5, []),
                      (6, [])]),
                 (7, [(8, []),
                      (9, [])])]),
            [(4, 2), (0, 5), (2, 3), (9, 2), (6, 4), (7, 8), (8, 1)],
            [False, True, False, False, True, True, False],
        ),
    )

    for test_nb, (tree, pairs, answers) in enumerate(TESTS, 1):
        user_result = list(on_same_path(tree, pairs))
        if user_result != answers:
            print(f'You failed the test #{test_nb}.')
            print(f'Your result: {user_result}')
            print(f'Right result: {answers}')
            break
    else:
        print('Well done! Click on "Check" for real tests.')


if __name__ == '__main__':  # from tests.py
    from tests import TESTS
    categories_to_test = (
        'Basic',
        'Extra',
        # 'Random',
    )

    TESTS = [
        (*test['input'], test['answer'])
        for category in categories_to_test
        for test in TESTS[category]
    ]

    for test_nb, (tree, pairs, answers) in enumerate(TESTS, 1):
        user_result = list(on_same_path(tree, pairs))
        if user_result != answers:
            print(f'You failed the test #{test_nb}.', tree, pairs, sep='\n')
            print(f'Your result: {user_result}')
            print(f'Right result: {answers}')
            break
    else:
        print('Well done! My solution pass all tests.')
