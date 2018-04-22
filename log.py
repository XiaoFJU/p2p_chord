import sys


class Log():
    def __init__(self, enable=True, level='ERROR'):
        self._enable = enable

    def get_enable(self):
        return bool(self._enable)

    def switcher(self, enable):
        self._enable = enable

    def log(self, *objects, mark='', sep=' ', end='\n', file=sys.stdout, flush=False):
        if self.get_enable():
            print(mark, *objects, sep=sep, end=end, file=file, flush=flush)

    def info(self, *objects, sep=' ', end='\n', file=sys.stdout, flush=False):
        self.log('[INFO]', *objects, sep=sep, end=end, file=file, flush=flush)

    def debug(self, *objects, sep=' ', end='\n', file=sys.stdout, flush=False):
        self.log('[DEBUG]', *objects, sep=sep, end=end, file=file, flush=flush)
