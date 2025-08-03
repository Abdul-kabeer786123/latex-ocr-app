
from pix2tex.cli import LatexOCR
from PIL import Image

model = LatexOCR()

image = Image.open("math3.png")  

prediction = model(image)
print(" Predicted LaTeX:", prediction)
