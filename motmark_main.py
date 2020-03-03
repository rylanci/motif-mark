#!/usr/bin/env python

# Package Imports
import math
import cairo
import re



# Read in files

#seqs = open("Figure_1.fasta")



# Functions
'''
def mto2linefasta(file):
    with open(file, "r"):
        new_fasta = tuple()
        for line in file:
            #print(line[0])
            if line[0] == ">":
                #new_fasta.append(line)
                new_fasta += f"\n{line}"

            if line[0] != ">":
                #new_fasta.append(line.strip())
                new_fasta += line.strip()

        return new_fasta
'''

'''
def mto2linefasta(file):
    file = open(file)
    nfile =  open("m21.fa", "w")
    for i,line in enumerate(file):
        if line[0] == ">" and i == 0:
            nfile.write(line)
        if line[0] == ">" and i != 0:
            nfile.write(f"\n{line}")
        if line[0] != ">":
            nfile.write(line.strip())

mto2linefasta("../Figure_1.fasta")

'''


def draw_intron(y, seq):
    # identify introns
    intron = re.compile('[a-z]+')
    j = intron.findall(seq)

    # loop over introns and draw line
    ctx.set_line_width(5)
    for match in j:
        # identify intron coordinates
        i = re.compile(match)
        f = i.search(line2)
        start, end = f.span()

        # draw line
        ctx.move_to(start,y)
        ctx.line_to(end,y)
        ctx.stroke()



def draw_exon(y, seq):
    # identify exons
    intron = re.compile('[A-Z]+')
    j = intron.findall(seq)

    # loop over exons and draw line
    ctx.set_line_width(10)
    for match in j:
        # identify intron coordinates
        i = re.compile(match)
        f = i.search(line2)
        start, end = f.span()

        # draw line
        ctx.move_to(start,y)
        ctx.line_to(end,y)
        ctx.stroke()






m21fa = open("m21.fa")


# use seqe lengths to calculate width of surface
# use num_seqs to calculate height
seq_lens = ()
num_seqs = 0
for i, line in enumerate(m21fa):
    #print(len(line))
    if i == 1:
        line2 = line
    if line[0] == ">":
        num_seqs += 1

#print(line2)


WIDTH, HEIGHT = 750, num_seqs * 120


# Pycairo experiments
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

'''
ctx.set_line_width(5)
ctx.move_to(0,10)
ctx.line_to(500,10)
ctx.stroke()

ctx.move_to(0,100)
ctx.line_to(300,100)
#ctx.rectangle(0, 0, 20, 20)
ctx.stroke()
'''

#ctx.rectangle(x,y,width,height)


'''
#print(type(line2))
intron = re.compile('[a-z]+')
j = intron.findall(line2)
for match in j:
    i = re.compile(match)
    f = i.search(line2)
    start, end = f.span()
    print(start, end)

'''




draw_intron(30, line2)
draw_exon(30, line2)

# Save to file
surface.write_to_png("example.png")  # Output to PNG
