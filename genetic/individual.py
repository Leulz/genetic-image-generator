class Individual:
  """Represents an image"""
  def __init__(self, **kwargs):
    self.genome = kwargs['genome'] # List of genes
    self.fitness = 0 # Fitness value for this individual