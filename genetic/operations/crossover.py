import sys, random

sys.path.insert(0, '../')
from genetic.individual import Individual

def reproduce(ind1, ind2, mutator):
  genes1 = ind1.genome
  genes2 = ind2.genome

  child_genome = []

  for i in range(len(genes1)):
    chance = random.randrange(10)
    child_gene = mutator.mutate(genes1[i] if chance < 5 else genes2[i])
    child_genome.append(child_gene)

  return Individual(genome=child_genome)