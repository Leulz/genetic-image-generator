class Gene:
  """Represents a circle"""
  def __init__(self, **kwargs):
    self.x = kwargs['x'] # x coordinate
    self.y = kwargs['y'] # y coordinate
    self.z = kwargs['z'] # z coordinate
    self.r = kwargs['r'] # Radius
    self.color = kwargs['color'] # Color