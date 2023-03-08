import os


def read_block(f):
    buf = ""
    while(f.read(1) != "{"):
        pass
    stack = 1
    while stack > 0:
        c = f.read(1)
        if c == '}':
            stack = stack - 1
        elif c == '{':
            stack = stack + 1

        if stack != 0:
            buf = buf + c;
    return buf

sections = ["dfn", "thm", "nt", "ex"]
indices = {}
for s in sections:
    indices[s] = 0
    os.system("mkdir cards_"+s);
texfile = open("main.tex", "r")
os.system("rm -rf cards")
os.system("mkdir cards")
chrbuf = ""
cardidx = 0
header = "\n".join(open("header.tex", "r").readlines())
while True:
    char = (texfile.read(1))
    if not char:
        break
    chrbuf = chrbuf + char
    read_section = ""
    for a in sections:
        if chrbuf.endswith("\\" + a):
            read_section = a
    
    if(read_section != ""):
        indices[read_section] = indices[read_section] + 1
        print(read_section)
        frontside = read_block(texfile)
        backside = read_block(texfile)
        print(frontside)
        print(backside)
        cardidx = cardidx + 1
        
        with open("front_" + str(cardidx) + ".tex", "w") as f:
            f.write(header)
            f.write("\n\\" + read_section)
            f.write("{")
            f.write(frontside)
            f.write("}{}\n\\end{document}")
        with open("back_" + str(cardidx) + ".tex", "w") as f:
            f.write(header)
            f.write("\n\\" + read_section)
            f.write("{")
            f.write(frontside)

            f.write("}\n{")
            f.write(backside)
            f.write("}\n\\end{document}")
        os.system("pdflatex -interaction=nonstopmode front_{}.tex".format(str(cardidx)));
        os.system("pdflatex -interaction=nonstopmode back_{}.tex".format(str(cardidx)));
        os.system("convert -density 300 front_{}.pdf -quality 90 front_{}.png".format(str(cardidx), str(cardidx)));
        os.system("convert -density 300 back_{}.pdf -quality 90 back_{}.png".format(str(cardidx),str(cardidx)));
        os.system("cp front_{}.png cards_{}/front_{}.png".format(str(cardidx), read_section, indices[read_section]))
        os.system("cp back_{}.png cards_{}/back_{}.png".format(str(cardidx), read_section, indices[read_section])) 
        chrbuf = ""
os.system("mv front_*.png front_*.pdf cards")
os.system("mv back_*.png back_*.pdf cards")
os.system("rm front_* back_*")
os.system("latexmk -c")
