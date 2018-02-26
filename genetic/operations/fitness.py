from PIL import Image, ImageDraw

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

#TODO Move these functions to another file.
def compare(img1, img2):
    pix1 = numpy.array(img1)
    pix2 = numpy.array(img2)
    img1 = to_grayscale(pix1.astype(float))
    img2 = to_grayscale(pix2.astype(float))
    n_0 = compare_images(img1, img2)
    
    return n_0*1.0/img1.size

def compare_images(img1, img2):
    img1 = normalize(img1)
    img2 = normalize(img2)
    diff = img1 - img2  # elementwise for scipy arrays
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    
    return z_norm

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

class FitnessFunction:
  def __init__(self, target_image):
    self.target_image = target_image
  def calculate_fitness(self, individual):
    genome = individual.genome
    im = Image.new("L", (self.target_image.width, self.target_image.height))
    dr = ImageDraw.Draw(im)
    
    for gene in individual.genome:
      pos = (gene.x-gene.r, gene.y-gene.r, gene.x+gene.r, gene.y+gene.r)
      dr.ellipse(pos,fill=gene.color)
    
    return 1 - compare(self.target_image, im)