class Progression:

    def __init__(self, start=0, step=1, stop=None):
        self.current = start
        self.start = start
        self.stop = stop
        self._step = None
        self.step = step

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        if value <= 0:
            raise ValueError("The step cannot be negative")
        self._step = value

    def progress(self):
        raise NotImplementedError

    def __next__(self):
        self.progress()
        if self.stop is not None and self.current >= self.stop:
            self.current = self.start
            raise StopIteration
        return self.current

    def __iter__(self):
        return self


class ArithmeticProgression(Progression):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def progress(self):
        print(f"Received {self.current}")
        self.current += self.step


pg = ArithmeticProgression(start=2, stop=10, step=0)
for i in pg:
    print(i)

