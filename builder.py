import sys, os, random
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
  r = random.randrange(1, int(min(width,height)/2))
  color = random.randrange(256)

  return Gene(x=x, y=y, z=z, r=r, color=color)

def print_gene(gene):
  print("x is %d, y is %d, z is %d, r is %d, color %d" % (gene.x, gene.y, gene.z, gene.r, gene.color))

def get_next_population(current_population, mutator, fitnessFunction):
  individual_list = current_population.individuals
  next_individual_list = []
  next_individual_list.append(individual_list[0])
  while len(next_individual_list) < len(individual_list):
    parent1, i = pick_individual(individual_list, -1)
    parent2, i = pick_individual(individual_list, i)
    next_individual = reproduce(parent1, parent2, mutator)
    next_individual_list.append(next_individual)
  next_individual_list = sorted(next_individual_list, key=lambda individual: fitnessFunction.calculate_fitness(individual), reverse=True)
  # print("first in list has %f" % ((lambda individual: fitnessFunction.calculate_fitness(individual))(next_individual_list[0])))
  # print("last in list has %f" % ((lambda individual: fitnessFunction.calculate_fitness(individual))(next_individual_list[len(next_individual_list)-1])))
  return Population(individuals=next_individual_list)

if __name__ == "__main__":
  os.system("find . -name \*.pyc -delete")
  target_image_path = input("Insert path to the image to be used as the target: ")
  try:
    target_image = Image.open(target_image_path)
    target_image.load()
    target_image = target_image.convert('L')
    fitnessFunction = FitnessFunction(target_image)

    width, height = target_image.size
    number_of_indidivuals = int(input("Insert the number of images you want in the population: "))
    number_of_genes = int(input("Insert the number of circles you want in the image: "))
    mutation_chance = float(input("Insert the mutation chance: "))
    current_population = create_population(number_of_indidivuals, number_of_genes)
    ind_list = current_population.individuals
    ind_list = sorted(ind_list, key=lambda individual: fitnessFunction.calculate_fitness(individual), reverse=True)
    current_population.individuals = ind_list
    count = 0
    saves = 0
    mutator = Mutator(width, height, mutation_chance)
    while True:
      print("Looping...")
      current_population = get_next_population(current_population, mutator, fitnessFunction)
      if count == 0:
        im = Image.new("L", (target_image.width, target_image.height))
        dr = ImageDraw.Draw(im)
        print("Best one has fitness: %f" % ((lambda individual: fitnessFunction.calculate_fitness(individual))(current_population.individuals[0])))
        genome = current_population.individuals[0].genome
        genome = sorted(genome, key=(lambda g : g.z))
        for gene in genome:
          pos = (gene.x-gene.r, gene.y-gene.r, gene.x+gene.r, gene.y+gene.r)
          dr.ellipse(pos,fill=gene.color)
        filename = "/home/leo/ind%d.jpeg" % saves
        im.save(filename, "JPEG")
        print("saved")
        im.close()
        saves += 1
      count = (count + 1) % 20
  except IOError:
    print("Error when opening image!")
    sys.exit(1)