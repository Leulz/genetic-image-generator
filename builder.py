import sys, random
from PIL import Image
from genetic.gene import Gene
from genetic.individual import Individual
from genetic.population import Population
from genetic.operations.crossover import * 
from genetic.operations.fitness import FitnessFunction

# These need to be set when the target image has been received.
width = 0
height = 0

depth = 500
#max_rgb_value = 255

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
  r = random.randrange(3, int(min(width,height)/5))
  color = random.randrange(255)
  #rgb = (random.randrange(max_rgb_value),) * 3

  return Gene(x=x, y=y, z=z, r=r, color=color)

if __name__ == "__main__":
  target_image_path = input("Insert path to the image to be used as the target: ")
  try:
    target_image = Image.open(target_image_path)
    f = FitnessFunction(target_image)

    width, height = target_image.size
    number_of_indidivuals = int(input("Insert the number of images you want in the population: "))
    number_of_genes = int(input("Insert the number of circles you want in the image: "))
    initial_population = create_population(number_of_indidivuals, number_of_genes)
    
    #use f.calculate_fitness(individual) to get the fitness of an individual
    #start iterating over generations


  except IOError:
    print("Error when opening image!")
    sys.exit(1)