import random

class Mutator:

    def __init__(self, width, height, prob):
        self.width = width
        self.height = height
        self.prob = prob

    def mutate(self, gene):
        r_value = random.random()

        if r_value > self.prob:
            return gene

        mutationType = random.randint(0, 4)
        if mutationType == 0:
            gene.x = random.randint(0,self.width)#self._bound(gene.x + random.randint(0,maxDelta) - halfDelta, 0, self.width)
        elif mutationType == 1:
            gene.y = random.randint(0,self.height)#self._bound(gene.y + random.randint(0,maxDelta) - halfDelta, 0, self.height)
        elif mutationType == 2:
            gene.z = random.randint(0, 500)
        elif mutationType == 3:
            gene.r = random.randint(1,int(min(self.width,self.height)/2))#self._bound(gene.r + random.randint(0, maxDelta) - halfDelta, 5, int(min(self.width,self.height)/5))
        else:
            gene.color = random.randint(0, 255)

        return gene