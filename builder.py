import sys, random
from PIL import Image, ImageDraw
from genetic.gene import Gene
from genetic.individual import Individual
from genetic.population import Population
from genetic.operations.crossover import * 
from genetic.operations.fitness import FitnessFunction
from genetic.selection.selector import pick_individual
from genetic.operations.mutator import Mutator

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

def get_next_population(current_population, mutator, fitnessFunction):
  individual_list = sorted(current_population.individuals, key=lambda individual: fitnessFunction.calculate_fitness(individual), reverse=True)
  next_individual_list = []
  print("first in list has %f" % ((lambda individual: fitnessFunction.calculate_fitness(individual))(individual_list[0])))
  print("last in list has %f" % ((lambda individual: fitnessFunction.calculate_fitness(individual))(individual_list[-1])))
  next_individual_list.append(individual_list[0])
  while len(next_individual_list) < len(individual_list):
    parent1 = pick_individual(individual_list)
    parent2 = pick_individual(individual_list)
    next_individual = reproduce(parent1, parent2, mutator)
    print((lambda individual: fitnessFunction.calculate_fitness(individual))(next_individual))
    next_individual_list.append(next_individual)
  next_individual_list = sorted(next_individual_list, key=lambda individual: fitnessFunction.calculate_fitness(individual), reverse=True)
  return Population(individuals=next_individual_list)

if __name__ == "__main__":
  target_image_path = input("Insert path to the image to be used as the target: ")
  try:
    target_image = Image.open(target_image_path)
    f = FitnessFunction(target_image)

    width, height = target_image.size
    number_of_indidivuals = int(input("Insert the number of images you want in the population: "))
    number_of_genes = int(input("Insert the number of circles you want in the image: "))
    mutation_chance = float(input("Insert the mutation chance: "))
    current_population = create_population(number_of_indidivuals, number_of_genes)
    count = 0
    saves = 0
    mutator = Mutator(width, height, mutation_chance)
    while True:
      print("Looping...")
      current_population = get_next_population(current_population, mutator, f)
      if count == 0:
        im = Image.new("L", (target_image.width, target_image.height))
        dr = ImageDraw.Draw(im)
        for gene in current_population.individuals[0].genome:
          pos = (gene.x-gene.r, gene.y-gene.r, gene.x+gene.r, gene.y+gene.r)
          dr.ellipse(pos,fill=gene.color)
        filename = "/home/leo/ind%d.jpeg" % saves
        im.save(filename, "JPEG")
        print("saved")
        im.close()
        saves += 1
      count = (count + 1) % 100
    #use f.calculate_fitness(individual) to get the fitness of an individual
    #start iterating over generations
  except IOError:
    print("Error when opening image!")
    sys.exit(1)