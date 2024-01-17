import random
from pydantic import PositiveInt
from pydantic.dataclasses import dataclass


@dataclass
class Dice:
    max: PositiveInt = 100

    def roll(self, seed=False):
        if seed: random.seed(seed)
        return random.randint(1, self.max)

    def rolln(self, x: int, seed=False):
        if seed: random.seed(seed)
        results = []
        for i in range(x):
            results.append(random.randint(1, self.max))
        return sum(results)
    def __repr__(self) -> str:
        return f"d{self.max}"


d100 = Dice(100)
d6 = Dice(6)
d4 = Dice(4)

if __name__ == "__main__":
    res = d100.roll()
    print(res)
