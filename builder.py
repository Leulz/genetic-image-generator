import requests
import json
import signal
import pickle
import sys, os, random
from PIL import Image, ImageDraw
from genetic.gene import Gene
from genetic.individual import Individual
from genetic.population import Population
from genetic.operations.crossover import *
from genetic.selection.selector import pick_individual
from genetic.operations.mutator import Mutator
from genetic.record import Record
from multiprocessing import Pool
import json
from base64 import b64encode

LOAD_BALANCER_URL = 'http://127.0.0.1:5005/calculate-fitness'

# These need to be set when the target image has been received.
width = 0
height = 0
depth = 500
#max_rgb_value = 255

current_population = None
mutation_chance = 0.0

def calculate_fitness(individual):
  str_individual = pickle.dumps(individual, pickle.HIGHEST_PROTOCOL)
  r = requests.post(LOAD_BALANCER_URL, data=json.dumps({"individual": b64encode(str_individual)}))
  fitness = json.loads(r.text)['fitness']

  return float(fitness)

def calculate_fitnesses(individual_list):
  pool = Pool()
  fitnesses = pool.map(calculate_fitness, individual_list)
  return [x for _,x in sorted(zip(fitnesses,individual_list), key=lambda pair: pair[0], reverse=True)]

def print_menu():
  '''
  Shows to the user the menu of options.

  If the user chooses option 1, information to create a new population will have to be provided.
  If the user chooses option 2, a saved population can be loaded from a file.
  '''
  print("\nMENU:")
  print("1 - Create new population.")
  print("2 - Load a saved population.")

def signal_handler(signal, frame):
  '''
  Captures the signal generated after pressing CTRL + C. This function calls the function thats
  saves the current population into a file.
  '''
  save_population(current_population, mutation_chance)
  sys.exit(0)

def save_population(current_population, mutation_chance):
  '''
  Saves the current population into a file.
  '''
  record = Record(population=current_population, mutation_chance=mutation_chance)

  pickle.dump(record, open( "saved_population.p", "wb" ))

def load_population(path):
  '''
  Loads the population and the chance of mutation from a file.
  '''
  record = pickle.load( open( path, "rb" ) )

  current_population = record.population
  mutation_chance = record.mutation_chance

  return current_population, mutation_chance

def create_population(individual_num, genes_num):
  '''
  Creates a new population.

  individual_num:
    Number of individuals of the population.

  genes_num:
    Number of genes of each individual.
  '''
  individual_list = []
  for i in range(individual_num):
    individual = create_individual(genes_num)
    individual_list.append(individual)

  return Population(individuals=individual_list)

def create_individual(genes_num):
  '''
  Creates a new individual.

  genes_num:
    Number of genes of the individual.
  '''
  genes_list = []
  for i in range(genes_num):
    gene = create_gene()
    genes_list.append(gene)

  return Individual(genome=genes_list)

def create_gene():
  '''
    Creates a new gene.

    The gene contains the following attributes:  x, y, z, radius, and color.
    The attributes x,y and z represent the coordinates of the pixel.
  '''
  x = random.randrange(height)
  y = random.randrange(width)
  z = random.randrange(depth)
  r = random.randrange(1, int(min(width,height)/2))
  color = random.randrange(256)

  return Gene(x=x, y=y, z=z, r=r, color=color)

def print_gene(gene):
  '''
  Prints all the information about a specific gene.
  '''
  print("x is %d, y is %d, z is %d, r is %d, color %d" % (gene.x, gene.y, gene.z, gene.r, gene.color))

def get_next_population(current_population, mutator):
  '''
  Generates the next new population.

  The new population is composed by the fittest genes of the current population.
  '''
  individual_list = current_population.individuals
  next_individual_list = []
  next_individual_list.append(individual_list[0])

  while len(next_individual_list) < len(individual_list):
    parent1, i = pick_individual(individual_list, -1)
    parent2, i = pick_individual(individual_list, i)
    next_individual = reproduce(parent1, parent2, mutator)
    next_individual_list.append(next_individual)
  next_individual_list = calculate_fitnesses(next_individual_list)

  return Population(individuals=next_individual_list)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)

  target_image_path = "/home/ubuntu/genetic-image-generator/image.png"

  try:
    img = Image.open(target_image_path)
    img_as_jpg = img.convert("L")
    img_as_jpg.save('/home/ubuntu/image.jpg')

    width, height = img.size

    number_of_indidivuals = 50
    number_of_genes = 100
    mutation_chance = 0.1
    generated_images_path = "/home/ubuntu"

    current_population = create_population(number_of_indidivuals, number_of_genes)

    if(current_population is not None):
      with open("/home/ubuntu/app-progress.log", 'w'): pass
      ind_list = current_population.individuals
      ind_list = calculate_fitnesses(ind_list)
      current_population.individuals = ind_list

      count = 0
      saves = 0
      mutator = Mutator(width, height, mutation_chance)

      while True:
        current_population = get_next_population(current_population, mutator)

        if count == 0:
          im = Image.new("L", (img.width, img.height))
          im.load()
          dr = ImageDraw.Draw(im)
          with open('/home/ubuntu/app-progress.log', 'a') as prog_file:
            prog_file.write("%f\n" % ((lambda individual: calculate_fitness(individual))(current_population.individuals[0])))
          genome = current_population.individuals[0].genome
          genome = sorted(genome, key=(lambda g : g.z))

          for gene in genome:
            pos = (gene.x-gene.r, gene.y-gene.r, gene.x+gene.r, gene.y+gene.r)
            dr.ellipse(pos,fill=gene.color)

          filename = generated_images_path + "/image_%d.jpeg" % saves
          im.save(filename, "JPEG")
          print("saved")
          im.close()
          saves += 1

        count = (count + 1) % 1
    else:
      raise TypeError
  except IOError:
    print("Error when opening image!")
    sys.exit(1)
  except TypeError:
    print("Null object error!")
    sys.exit(1)
  except RuntimeError:
    print("You must provide a valid input!")
    sys.exit(1)
