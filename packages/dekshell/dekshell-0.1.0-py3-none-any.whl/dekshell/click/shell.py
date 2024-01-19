import os
import shutil
import sys
import shlex
import tempfile
import codecs
from ..core import shell_command_batch, shell_command_file
from ..core.markers.base import MarkerBase
from ..core.contexts import get_all_context
from ..core.markers import generate_markers
from ..utils.print import pprint
from ..utils.str import str_escaped
from ..utils.shell import shell_wrapper
from ..core.redirect import redirect_shell_by_path_tree
from ..core.plugin import find_plugins
from ..core.encode import decode_run_str
from .base import app


def get_argv(index=None):
    argv = shlex.split(' '.join(sys.argv), posix=False)
    if index is not None:
        return argv[index]
    else:
        return argv


def get_kwargs(begin):
    return MarkerBase.cmd2ak(get_argv()[begin:])[1]


def try_redirect_shell(filepath=None):
    filepath = filepath or os.getcwd()
    path_shell = redirect_shell_by_path_tree(filepath)
    if path_shell:
        shell_wrapper(path_shell + ' ' + ' '.join(sys.argv[1:]))
        return True
    else:
        return False


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def rs():
    line = get_argv(2)
    if not try_redirect_shell():
        line = decode_run_str(line)
        shell_command_batch(str_escaped(line), context=get_kwargs(3))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def rf():
    filepath = get_argv(2)
    if not try_redirect_shell(filepath):
        filepath = os.path.normpath(os.path.abspath(filepath))
        cwd = os.getcwd()
        os.chdir(os.path.dirname(filepath))
        shell_command_file(filepath, context=get_kwargs(3))
        os.chdir(cwd)


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def rfc():
    filepath = get_argv(2)
    if not try_redirect_shell(filepath):
        shell_command_file(filepath, context=get_kwargs(3))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def r():
    s = get_argv(2)
    if os.path.isfile(s):
        rf()
    else:
        rs()


@app.command()
def self():
    if not try_redirect_shell():
        pprint(dict(
            context=get_all_context(),
            marker=generate_markers(),
            plugin=find_plugins()
        ))


@app.command()
def reg():
    assert os.name == 'nt'
    path_ext_reg = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'res', 'windows',
                                'ext.reg.tpl')
    with codecs.open(path_ext_reg, 'r', encoding='utf-8') as f:
        content = f.read()
    path_dekshell = shutil.which(os.path.basename(sys.argv[0]))
    content_reg = content.format(
        dekshell_exe=os.path.basename(path_dekshell),
        dekshell_exe_full_path=path_dekshell.replace('\\', '\\\\'),
    )
    path_reg = os.path.join(tempfile.mkdtemp(), 'ext.reg')
    with codecs.open(path_reg, 'w', encoding='utf-8') as f:
        f.write(content_reg)
    shell_wrapper(f'regedit {path_reg}')
