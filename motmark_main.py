#!/usr/bin/env python

# Package Imports
import math
import cairo
import re
import random
import numpy as np
import imshow
from matplotlib import cm




# to notes
# remove upper case in motifs & convert u's to c's.
# remove upper case in exons after identified and drawn
# ensure regex list length == number of motifs
# Find out why regex arent fitting
#

# Read in files
m21fa = open("m21.fa")

# use seqe lengths to calculate width of surface
# use num_seqs to calculate height
seq_lens = ()
num_seqs = 0
for i, line in enumerate(m21fa):
    #print(len(line))
    if i == 1:
        line2 = line
    if i == 3:
        line3 = line
    if i == 5:
        line4 = line
    if line[0] == ">":
        num_seqs += 1


m21fa.close()
#seqs = open("Figure_1.fasta")

# read in motifs, standardize them
mots = set()
col_palate = []
with open("../Fig_1_motifs.txt", "r") as fh:
    for i,mot in enumerate(fh):
        mot = mot.replace("G","g")
        mot = mot.replace("C","c")
        mot = mot.replace("T","t")
        mot = mot.replace("A","a")
        mot = mot.replace("U","u")
        mot = mot.replace("Y","y")
        mot = mot.replace("u","c")
        mots.add(mot.strip())

        # create colors for each motif
        #col_palate.append()
        col = [random.random(),random.random(),random.random()]
        col_palate.append(col)

print(col_palate)
#print(mots)


# Functions

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
    ctx.set_source_rgb(0,0,0)
    for match in j:
        # identify intron coordinates
        i = re.compile(match)
        f = i.search(seq)
        start, end = f.span()

        # draw line
        ctx.move_to(start +30,y)
        ctx.line_to(end +30,y)
        ctx.stroke()



def draw_exon(y, seq):
    # identify exons
    intron = re.compile('[A-Z]+')
    j = intron.findall(seq)

    # loop over exons and draw line
    ctx.set_line_width(10)
    ctx.set_source_rgb(0,0,0)
    for match in j:
        # identify intron coordinates
        i = re.compile(match)
        f = i.search(seq)
        start, end = f.span()

        # draw line
        ctx.move_to(start +30,y)
        ctx.line_to(end +30,y)
        ctx.stroke()






def draw_mots(y, seq):

    # Create regex for the input motifs
    for i,m in enumerate(mots):
        mot_len = len(m)
        if "y" in m:
            m = m.replace("y", "[ct]{1}")
        if "u" in m:
            m.replace("u", "c")

#        print(mots)
        # identify motifs in the sequences
        j = re.finditer(f"(?={m})", seq)

        # Color the motifs. Set Width
        ctx.set_line_width(20)
#        cols = cm.jet(random.randint(1,100))[0:3]
#        ctx.set_source_rgb(cols[0],cols[1],cols[2])
        cols = col_palate[i]
        print(cols[0])
        print(cols[1])
        print(cols[2])
        ctx.set_source_rgb(cols[0],cols[1],cols[2])
        for match in j:
            # calculate end manually. len motif -1
            start = match.start()
            end = start + mot_len -1
#            print(start,end)
            # draw line
            ctx.move_to(start +30,y)
            ctx.line_to(end+30,y)
            ctx.stroke()
#        print(cols)
#
    #for i in range(100):
        #fprint(cm.jet(i))


def draw_text(y,text):
    ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0,0,0)
    ctx.set_font_size(13)

    ctx.move_to(30, y)
    ctx.show_text(text)


# Pycairo surface setup

WIDTH, HEIGHT = 900, num_seqs * 120

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
#ctx.rectangle(x,y,width,height)
'''


# To scale intron Y coords

scale_list = list()
for i in range(num_seqs):
    scale_list.append(HEIGHT/num_seqs * i + 50)



# Main Loop
m21fa = open("m21.fa")
cntr = 0
while True:
    label = m21fa.readline()
    if label == "":
        break
    seq = m21fa.readline()


    print(cntr)
    y_coord = scale_list[cntr]


    draw_intron(y_coord, seq)
    draw_text(y_coord - 30, label)
    draw_exon(y_coord, seq)
    seq = seq.replace("G","g")
    seq = seq.replace("C","c")
    seq = seq.replace("T","t")
    seq = seq.replace("A","a")
    draw_mots(y_coord, seq)
    cntr +=1





'''
draw_intron(30, line2)
draw_intron(130, line3)
draw_intron(260, line4)

draw_exon(30, line2)
line2 = line2.replace("G","g")
line2 = line2.replace("C","c")
line2 = line2.replace("T","t")
line2 = line2.replace("A","a")
draw_mots()
#print(line2)

'''


# Save to file
surface.write_to_png("example.png")  # Output to PNG
