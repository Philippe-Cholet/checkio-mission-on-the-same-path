from checkio import api
from checkio.signals import ON_CONNECT
from checkio.referees.io import CheckiOReferee
from checkio.referees import cover_codes

from tests import TESTS


# To match the tree and pairs types,
# we must make tuples that JSON changed to lists.
# Tree = Tuple[Node, List['Tree']]
# Pairs = List[Tuple[Node, Node]]
make_tuples = '''
def parse_tree(tree):
    root, childs = tree
    if childs:
        childs = map(parse_tree, childs)
    return root, list(childs)


def cover(func, data):
    tree, pairs = data
    tree = parse_tree(tree)
    pairs = list(map(tuple, pairs))
    return func(tree, pairs)
'''


api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        function_name={
            'python': 'on_same_path',
            'js': 'onSamePath',
        },
        cover_code={
            'python-3': make_tuples,
            'js-node': cover_codes.js_unwrap_args,
        },
    ).on_ready,
)
