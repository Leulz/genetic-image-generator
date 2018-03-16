from random import uniform


def pick_individual(individual_list, partner_index):
  '''
  Picks an individual

  Picks an individual from a list of individuals.
  Assumes the list is sorted, with the most fit individuals
  being at the beginning of the list.
  '''
  list_length = len(individual_list)
  bias = 0.6 * list_length
  for i in range(1, list_length):
    if i != partner_index and uniform(0,1) < ((list_length - i) / (list_length + bias)):
      return individual_list[i], i # more likely to pick a fit individual
  return individual_list[0], 0 # on the off chance that no individual is returned in the loop, we return the most fit individual
