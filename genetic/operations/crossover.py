import sys, random

sys.path.insert(0, '../')
from genetic.individual import Individual

def reproduce(ind1, ind2):
  genes1 = ind1.genome
  genes2 = ind2.genome

  child_genome = []

  #add chance of mutation here
  for i in range(len(genes1)):
    chance = random.randrange(10)
    if chance<5:
      child_genome.append(genes1[i])
    else:
      child_genome.append(genes2[i])

  return Individual(genome=child_genome)