from random import uniform

#picks an individual from a list of individuals.
#assumes the list is sorted, with the most fit individuals
#being at the beginning of the list.
def pick_individual(individual_list):
  list_length = len(individual_list)
  for i in range(list_length):
    if uniform(0,1) < (list_length - i / list_length): # more likely to pick a fit individual
      return individual_list[i]
  return individual_list[0] # on the off chance that no individual is returned in the loop, we return the most fit individual