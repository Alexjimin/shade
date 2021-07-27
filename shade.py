import PIL.Image
from PIL import ImageDraw, ImageFont
import numpy as np
import io

def compress(args):
	infile = ""
	if "-if" in args:
		infile = args[args.index("-if") + 1]
	else:
		infile = "test.jpeg"

	image = PIL.Image.open(infile)
	image_sequence = image.getdata()

	dimensions = image.size
	max_shade = 255

	image_array = np.array(image_sequence)
	grayscale_array = list()
	tmp = list()
	i = 0
	short_array = image_array
	compress_level = 0
	if "--compress" in args:
		compress_level = int(args[args.index("--compress") + 1])
		print(compress_level)
	for shade in short_array:
		if i < dimensions[0]:
			brightness = (shade[0]+shade[1]+shade[2])/len(shade)
			if brightness <= 0:
				tmp.append(1)
			else:
				tmp.append(brightness)
		else:
			grayscale_array.append(tmp)
			tmp = list()
			i = 0
		i += 1
	shade = grayscale_array
	shadelist = list()

	if "--shadelist" in args:
		listargs = args[args.index("--shadelist") + 1]
		if listargs == "shades":
			shadelist = ["\u2591", "\u2592", "\u2593", "\u2588"]
		elif listargs == "barcode":
			shadelist = ["\u2588", "\u2589", "\u258A", "\u258B", "\u258C", "\u258D", "\u258E", "\u258F"][::-1]
		elif listargs == "braille":
			shadelist = ["\u2800", "\u2840", "\u28C0", "\u2854", "\u2855", "\u2877", "\u28FE", "\u28FF"]
		else:
			shadelist = list(r" .',:-=+*/LOZ#&8%B@$")
	else:
		shadelist = list(r"  .',:-=+*/LOZ#&8%B@$")

	outfile = ""
	if "-of" in args:
		outfile = args[args.index("-of") + 1]
	else:
		outfile = f"output/{infile.split('.')[0][4:]}_processed"
		
	ret = ""
	with io.open(outfile+".txt", "w", encoding="utf-8") as f:
		for y, row in enumerate(shade):
			for x, item in enumerate(row):
				shade[y][x] = shadelist[int(item/max_shade * len(shadelist))]
				# print(shade)
				f.write(shade[y][x])
				ret += shade[y][x]
				# print(str(len(shade) / ((x*y)+1) * 100) +" %")
			f.write("\n"+shade[y][x])
			ret += "\n"
	# print(f"Finished text file.\nText file length is {len(shade)*len(shade[0])}\nOriginal file pixel length is {dimensions[0]*dimensions[1]}")
	return (ret, infile)

def to_image(outfile, args, size, infile):
	font = ""
	destination = ""
	if "--font" in args:
		font = args[args.index("--font") + 1].replace("\"", "")
	if "-of" in args:
		destination = args[args.index("-of")+1]

	# with open(outfile+".txt", "r") as f: # w: 25*(5/3) h: 25
		# img = PIL.Image.new("RGB", (int(25*(5/3))*len(grayscale_array[0]), 25*len(grayscale_array)))
	img = PIL.Image.new("RGB", (11*size[0], 18*size[1]))
	d = ImageDraw.Draw(img)
	d.text((0, 0), outfile, fill=(255, 255, 255), font=ImageFont.truetype(font, 18))
	img = img.resize((int(img.width*(300/3300)*20), int(img.height*(300/5382)*20)), PIL.Image.NEAREST)
	print(destination+".jpeg")
	img.save(destination+".jpeg")
	PIL.Image.open(infile).show()	# 300x300 -> 3300x5382
	img.show()

