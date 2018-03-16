from PIL import Image, ImageDraw
from skimage.measure import compare_ssim as ssim
from numpy import array

def compare(img1, img2):
    cv_img1 = array(img1)
    cv_img2 = array(img2)
    return ssim(cv_img1, cv_img2)


class FitnessFunction:

  def __init__(self, target_image):
    self.target_image = target_image

  def calculate_fitness(self, individual):
    im = Image.new("L", (self.target_image.width, self.target_image.height))
    dr = ImageDraw.Draw(im)
    genome = sorted(individual.genome, key=(lambda g : g.z))
    for gene in genome:
      pos = (gene.x-gene.r, gene.y-gene.r, gene.x+gene.r, gene.y+gene.r)
      dr.ellipse(pos,fill=gene.color)

    return compare(self.target_image, im)
