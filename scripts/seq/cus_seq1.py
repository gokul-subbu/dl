class Fib:
    def __init__(self, n):
        self._n=n

    def __getitem__(self,s):
        if isinstance(s, int):
            print(f'requesting [{s}]')
        else:
            print(f'requesting [{s.start}:{s.stop}:{s.step}]')

