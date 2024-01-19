import os
import tempfile
from beepy import beep
from ...utils.common import get_module_attr
from ...utils.file import sure_dir, write_file, read_text, remove_path
from ...utils.print import pprint
from ...utils.shell import shell_output
from ..encode import encode_run_str
from ..redirect import search_bin_by_path_tree


def _is_true(x):
    if isinstance(x, str):
        x = x.lower()
    return x not in {'false', '0', 'none', 'null', '', ' ', False, 0, None}


def _path_dir(path, num=1):
    cursor = path
    for i in range(int(num)):
        cursor = os.path.dirname(cursor)
    return cursor


default_methods = {
    'venvbin': lambda x: search_bin_by_path_tree(os.getcwd(), x),
    'rs': encode_run_str,
    'so': lambda *xx: shell_output(' '.join(xx)),
    'print': print,
    'pp': pprint,
    'gma': get_module_attr,
    'chdir': os.chdir,
    'ch': os.chdir,
    'cwd': lambda : os.getcwd().replace('\\', '/'),
    'lsa': lambda x: [os.path.normpath(os.path.abspath(os.path.join(x, y))) for y in os.listdir(x)],
    'ls': lambda x: os.listdir(x),
    'tmpd': lambda: tempfile.mkdtemp(),
    'exist': lambda x: os.path.exists(x),
    'noexist': lambda x: not os.path.exists(x),

    'pd': _path_dir,
    'sdir': sure_dir,
    'sd': sure_dir,
    'wf': write_file,
    'rt': read_text,
    'rp': remove_path,

    'value': lambda x: x,
    'true': lambda *x: True,
    'false': lambda *x: False,

    'istrue': _is_true,
    'isfalse': lambda x: not _is_true(x),
    'isequal': lambda x, y: x == y,
    'beep': lambda x=True: beep('coin' if x else 'robot_error')
}
