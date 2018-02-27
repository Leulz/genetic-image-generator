import random

class Mutator:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def mutate(self, gene, prob):
        #for moving/size
        maxDelta = ((self.width + self.height) / 2) / 2
        halfDelta = maxDelta / 2 + 2
        r_value = random.random()

        if r_value > prob:
            return gene

        mutationType = random.randint(0, 4)
        if mutationType == 0:
            gene.x = self._bound(gene.x + random.randint(0,maxDelta) - halfDelta, 0, self.width - gene.r)
        elif mutationType == 1:
            gene.y = self._bound(gene.y + random.randint(0,maxDelta) - halfDelta, 0, self.height - gene.r)
        elif mutationType == 2:
            gene.z = random.randint(0, 1000)
        elif mutationType == 3:
            gene.r = self._bound(gene.r + random.randint(0, maxDelta) - halfDelta, 5, self.width)
        else:
            gene.color = random.randint(0, 255)

        return gene

    def _bound(self, value, min, max):
        if (value < min):
            return min
        if (value > max):
            return max
        return value
