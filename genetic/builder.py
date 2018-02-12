import random
from gene import Gene
from individual import Individual
from population import Population

# These need to be set when the target image has been received.
width = 0
height = 0

depth = 500
max_rgb_value = 255

def create_population(individual_num, genes_num):
  individual_list = []
  for i in range(individual_num):
    individual = create_individual(genes_num)
    individual_list.append(individual)

  return Population(individuals=individual_list)

def create_individual(genes_num):
  genes_list = []
  for i in range(genes_num):
    gene = create_gene()
    genes_list.append(gene)

  return Individual(genome=genes_list)

def create_gene():
  x = random.randrange(height)
  y = random.randrange(width)
  z = random.randrange(depth)
  # The circle's radius will have at least 3 pixels of length, at most one fifth of the width or height 
  # depending on which is smaller. These values were arbitrarily chosen and are subject to change.
  r = random.randrange(3, min(width,height)/5)
  rgb = (random.randrange(max_rgb_value),) * 3

  return Gene(x=x, y=y, z=z, r=r, rgb=rgb)