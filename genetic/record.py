class Record:
	def __init__(self, **kwargs):
		self.population = kwargs['population'] #Population that is being saved.
		self.mutation_chance = kwargs['mutation_chance'] #Mutation chance of the population that is being saved.