import os
import sys
import subprocess
from .file import write_file


def shell_wrapper(command):
    err = os.system(command)
    if err:
        raise ChildProcessError(command)


def shell_output(command):
    return subprocess.getoutput(command)


def shell_stdout(command, write=sys.stdout.write, env=None):
    proc = subprocess.Popen(command,
                            env=env,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True
                            )
    while proc.poll() is None:
        stdout = proc.stdout.readline()
        if write:
            write(stdout)


def shell_command(command, sync=True, headless=False, quiet=False, ignore=False, env=None):
    result = None
    if os.name == 'nt' and headless:
        result = shell_command_nt_headless(command, sync)
    else:
        if not sync:
            command = _cmd_to_async(command)
        if quiet:
            shell_output(command)
        else:
            try:
                subprocess.run(command, check=True, shell=True, env=env)
            except subprocess.CalledProcessError as e:
                result = ChildProcessError((command, e))
    return None if ignore else result


def _cmd_to_async(command):
    if os.name == 'nt':
        command = 'start ' + command
    else:
        command = 'nohup ' + command + ' &'
    return command


def shell_command_nt_headless(command, sync=True, env=None):
    executor = 'wscript'
    if not env:
        env = os.environ.copy()
    if env.get('DEKSHELL_VBS_ENV') == 'true':  # As vbs call deep bug
        if sync:
            return shell_command(command, sync, headless=False, env=env)
        else:
            executor = 'start ' + executor
    env['DEKSHELL_VBS_ENV'] = "true"

    command = command.replace('"', '""')
    vbs = f"""
Dim Wsh
Set Wsh = WScript.CreateObject("WScript.Shell")
Wsh.Run "{command}",0,{'true' if sync else 'false'}
Set Wsh=NoThing
WScript.quit
    """
    fp = write_file('run.vbs', t=vbs)
    try:
        subprocess.run(f'{executor} {fp}', check=True, shell=True, env=env)
    except subprocess.CalledProcessError as e:
        return e
    return None


def show_win_msg(msg=None, title=None):
    if os.name == 'nt':
        import ctypes
        mb = ctypes.windll.user32.MessageBoxW
        mb(None, msg or 'Message', title or 'Title', 0)
