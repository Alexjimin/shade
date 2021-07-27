def compress_text(text, compress_level):
    outfile = str()
    for x in text.splitlines()[::int(compress_level)]:
        outfile += x[::int(compress_level)] + "\n"
    return (outfile, (len(outfile.splitlines()[0]), len(outfile.splitlines())))
    # with open("compressed/"+args[1], "w") as f:
    #     [f.write(x) for x in outfile]
    #     f.write("end of file")
    #     f.close()
