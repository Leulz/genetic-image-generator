from PIL import Image, ImageDraw
from skimage.measure import compare_ssim as ssim
from numpy import array
from pickle import load
from flask import Flask, request
from os import path

image_path = '/home/ubuntu/image.jpg'
individual_path = '/home/ubuntu/individual'

def compare(img1, img2):
    cv_img1 = array(img1)
    cv_img2 = array(img2)
    
    return ssim(cv_img1, cv_img2)

def get_fitness():
  image = Image.open(image_path)
  image.load()
  image = image.convert('L')
  
  im = Image.new("L", (image.width, image.height))
  dr = ImageDraw.Draw(im)
  
  with open(individual_path, 'rb') as individual_file:
    individual = load(individual_path)
  genome = sorted(individual.genome, key=(lambda g : g.z))
  
  for gene in genome:
    pos = (gene.x-gene.r, gene.y-gene.r, gene.x+gene.r, gene.y+gene.r)
    dr.ellipse(pos,fill=gene.color)

  return compare(image, im)

app = Flask(__name__)

@app.route('/calculate-fitness', methods=['POST'])
def calculate_fitness():
  uploaded_files = request.files.getlist('file')
  
  #We assume that the image file is called 'image.jpg' and the individual file is called 'individual'
  for f in uploaded_files:
    f.save(path.join('/home/ubuntu', f.filename))
  
  return {'fitness': get_fitness()}

if __name__ == '__main__':
  import sys
  app.run(host='0.0.0.0', port=sys.argv[1])
