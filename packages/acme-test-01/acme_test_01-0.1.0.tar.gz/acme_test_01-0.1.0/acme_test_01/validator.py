import math
import random


class RandomValidator:
    def __init__(self):
        self.msg = "Random validator"

    def __str__(self):
        return f'This is a basic example of a {self.msg} package who generates a random number {random.uniform(0, 1000)}'


