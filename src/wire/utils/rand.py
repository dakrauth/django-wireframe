import random


class RandomSampler:
    def __init__(self):
        self.population = list("ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789-")
        self.counts = [2] * len(self.population)
        self.counts[-1] = 1

    def __call__(self, size=8):
        return "".join(random.sample(self.population, size, counts=self.counts))


sampler = RandomSampler()
