import argparse
import os
from PIL import Image


# Parse input file
parser = argparse.ArgumentParser()
parser.add_argument("-directory", help = "Path to folder containing the photos", default = os.getcwd())
parser.add_argument("-extension", help = "Extension of photos files", default = '.JPG')
parser.add_argument("-background", help = "Minimum R, G or B value for Background", default = 120)
parser.add_argument("-black", help = "Maximum R, G or B value for Black", default = 120)
parser.add_argument("-output", help = "Name of result table, tab delimited", default = 'Salamander_color_results.csv')
args = parser.parse_args()


def measure_color(picture, min_background, max_black):
# Create counts
  background=0
  black=0
  yellow=0
  other=0

# Import image
  infile = Image.open(picture)
  image = infile.load()
  [xs, ys] = infile.size

# Obtain R,G,B values for each pixel
  for x in xrange(0, xs):
    for y in xrange(0, ys):
      [r, g, b] = image[x, y]

# Take off "white" pixels, i.e. background and shiny spots
      if all(j > float(min_background) for j in [r,g,b]) and all(n < 20 for n in [abs(r-g), abs(r-b), abs(g-b)]):
        background += 1

# Count black, yellow and other pixels
      elif all(m < max_black for m in [r,g,b]) and all(n < 20 for n in [abs(r-g), abs(r-b), abs(g-b)]):
        black += 1
      else:
        if all(y > 25 for y in [r-b, g-b]) and g in range(b,r):
          yellow += 1
        else:
          other += 1

# Calculate percents and proportions 
  total = black + yellow
  black_percent = round(float(black)*100/float(total), 2)
  yellow_percent = round(float(yellow)*100/float(total), 2)
  ratio = round(float(black)/float(yellow),2)
  result_line = [str(r) for r in [background,total,black,black_percent,yellow,yellow_percent,ratio,other]]
  return result_line


# Directory
path = str(args.directory)


# Header of results table
results = 'Sample\tBackground_pixels\tTotal_pixels\tBlack_pixels\tBlack_percent\tYellow_pixels\tYellow_percent\tRatio\tOther_pixels\n'


# Process all pictures in folder
for root, dirs_list, files_list in os.walk(path):
    for file_name in files_list:
        if os.path.splitext(file_name)[-1] == str(args.extension):
            file_path = os.path.join(root, file_name)
            results += file_name[:file_name.index('.')] + '\t'
            results += '\t'.join(measure_color(file_path, float(args.background), float(args.black)))
            results += '\n'


# Write results table
out_file = open(str(args.output), 'w')
out_file.write(results)


print 'Done!'
