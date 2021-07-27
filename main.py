import shade
import compresstext
import sys

args = sys.argv
print(args)
if args == []:
	print("Usage: python3 shade.py -if <input> -of <output> --shadelist <texts | shades | barcode | braille> --font <font> --compress <level>")
	exit()

compress_level = 1
if "--compress" in args:
    compress_level = args[args.index("--compress")+1]
ret, infile = shade.compress(args)
outfile, size = compresstext.compress_text(ret, compress_level)
print(size)
shade.to_image(outfile, args, size, infile)
# shade.to_image(ret, args, grayscale_array, infile)
