import string
import codecs
from collections.abc import Mapping


class FormatDict(Mapping):
    empty = object()

    def __init__(self, kwargs, missing=None):
        self.kwargs = kwargs
        self.missing = missing

    @staticmethod
    def __missing(key):
        return f'{{{key}}}'

    def __getitem__(self, item):
        value = self.kwargs.get(item, self.empty)
        if value is self.empty:
            return (self.missing or self.__missing)(item)
        else:
            return value

    def __iter__(self):
        return iter(self.kwargs)

    def __len__(self):
        return len(self.kwargs)


formatter = string.Formatter()


def str_format_partial(s, kwargs, missing=None):
    return formatter.vformat(s, (), FormatDict(kwargs, missing))


def str_escaped(s):
    return codecs.getdecoder("unicode_escape")(s.encode('utf-8'))[0]


def str_format_var(s, begin='{', end='}', escape='\\'):
    fmt = ['']
    args = []
    arg = None
    escaping = False
    for x in s:
        if not escaping and x == escape:
            escaping = True
        else:
            if escaping:
                if arg is None:
                    fmt[-1] += x
                else:
                    arg += x
            else:
                if x == begin:
                    if arg is None:
                        arg = ""
                    else:
                        arg += x
                else:
                    if x == end:
                        if arg is None:
                            fmt[-1] += x
                        else:
                            args.append(arg)
                            arg = None
                            fmt.append('')
                    else:
                        if arg is None:
                            fmt[-1] += x
                        else:
                            arg += x
            escaping = False
    return lambda xx, ma=None, mi=None: _str_format_var_final(fmt, xx, ma, mi), args


def _str_format_var_final(fmt, args, mapping=None, missing=None):
    s = ""
    cursor = 0
    while True:
        s += fmt[cursor]
        if cursor == len(fmt) - 1:
            break
        arg = args[cursor]
        if mapping and arg in mapping:
            arg = mapping[arg]
        elif missing:
            arg = missing(arg)
        s += str(arg)
        cursor += 1
    return s
