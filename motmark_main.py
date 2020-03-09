#!/usr/bin/env python

# Package Imports
import math
import cairo
import re
import random
import numpy as np
import imshow
from matplotlib import cm
import argparse

# Argparse implementation
def get_args():
    parser = argparse.ArgumentParser(description="A program to find and illustrate motifs")
    parser.add_argument("-i", help="Input fasta file", required = True)
    parser.add_argument("-o", help="Output image file", required = True)
    parser.add_argument("-m", help="file with input motifs", required = True)
    return parser.parse_args()

args = get_args()



##################
# Functions
##################

def mto2linefasta(file):
    file = open(file)
    nfile =  open(f"{args.i}.2lf", "x")
    for i,line in enumerate(file):
        if line[0] == ">" and i == 0:
            nfile.write(line)
        if line[0] == ">" and i != 0:
            nfile.write(f"\n{line}")
        if line[0] != ">":
            nfile.write(line.strip())




def draw_intron(y, seq):
    # identify introns
    seq_len = len(seq)

    # draw line
    ctx.set_source_rgb(0,0,0)
    ctx.set_line_width(5)
    ctx.move_to(30,y)
    ctx.line_to(seq_len +30,y)
    ctx.stroke()


def draw_exon(y, seq):
    # identify exons
    intron = re.compile('[A-Z]+')
    j = intron.findall(seq)

    # loop over exons and draw rectangles
    ctx.set_line_width(3)
    ctx.set_source_rgb(0,0,0)
    for match in j:
        # identify intron coordinates
        i = re.compile(match)
        f = i.search(seq)
        start, end = f.span()
        #print(start,end)

        ctx.rectangle(start+30, y-15,end-start, 30)
        ctx.stroke()




########
#return a dict with motif color pairs
#########

mot_col = dict()
def draw_mots(y, seq):

    # Create regex for the input motifs
    for i,m in enumerate(mots):
        mot_len = len(m)
        cols = col_palate[i]
        mot_col.update({m : cols})
        if "y" in m:
            m = m.replace("y", "[ct]{1}")
        if "u" in m:
            m.replace("u", "c")

#        print(mots)
        # identify motifs in the sequences
        j = re.finditer(f"(?={m})", seq)

        # Color the motifs. Set Width
        ctx.set_line_width(20)

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

        #print(m, cols)


def draw_text(x,y,text):
    ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0,0,0)
    ctx.set_font_size(13)

    ctx.move_to(x, y)
    ctx.show_text(text)


###################
#File and Variable setup
###################


# Create 2 line 2 line fasta
mto2linefasta(args.i)


# Read in seqs
# use seqe lengths to calculate width of surface
# use num_seqs to calculate height
with open(f"{args.i}.2lf") as fh:
    seq_lens = ()
    num_seqs = 0
    for i, line in enumerate(fh):
        if line[0] == ">":
            num_seqs += 1



# read in motifs, standardize them to lower case
mots = set()
col_palate = []
with open(args.m, "r") as fh:
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
        col = [random.random(),random.random(),random.random()]
        col_palate.append(col)



# Pycairo surface setup

WIDTH, HEIGHT = 900, num_seqs * 120 + 25

#surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
surface =cairo.PDFSurface(f"{args.o}", WIDTH, HEIGHT)
ctx = cairo.Context(surface)


# Text Header
ctx.select_font_face("Tango", cairo.FONT_SLANT_NORMAL,
    cairo.FONT_WEIGHT_NORMAL)
ctx.set_source_rgb(0,0,0)
ctx.set_font_size(25)

ctx.move_to(400, 20)
ctx.show_text("Motif-Mark")


# To scale intron Y coords
scale_list = list()
for i in range(num_seqs):
    scale_list.append(HEIGHT/num_seqs * i + 75)



# Main Loop
m21fa = open(f"{args.i}.2lf")
cntr = 0
while True:
    label = m21fa.readline()
    if label == "":
        break
    seq = m21fa.readline()


    #print(cntr)
    y_coord = scale_list[cntr]


    draw_intron(y_coord, seq)
    draw_text(30, y_coord - 30, label)
    draw_exon(y_coord, seq)
    seq = seq.replace("G","g")
    seq = seq.replace("C","c")
    seq = seq.replace("T","t")
    seq = seq.replace("A","a")
    draw_mots(y_coord, seq)
    cntr +=1

m21fa.close()






# Create Legend
#ctx.rectangle(x, y, width, height)
ctx.set_line_width(2)
ctx.set_source_rgb(0,0,0)
ctx.rectangle(740, 50, 130, len(mots)*25 +25)
ctx.stroke()


# scale for y
lgnd_scale = list()
for i in range(len(mots)):
    lgnd_scale.append(20 * i + 65)


#draw color blocks and print text
for i,mot in enumerate(mots):
    draw_text(800,lgnd_scale[i]+8, mot)
    ctx.set_line_width(2)
    col = mot_col.get(mot)
    ctx.set_source_rgb(col[0],col[1],col[2])
    ctx.rectangle(759, lgnd_scale[i],10 , 10)
    ctx.fill()
    ctx.stroke()

# add exon to legend
draw_text(800, lgnd_scale[len(lgnd_scale)-1]+28, "exon")
ctx.set_line_width(2)
ctx.set_source_rgb(0,0,0)
ctx.rectangle(759, lgnd_scale[len(lgnd_scale)-1]+20,10 , 10)
ctx.stroke()




# Save to file
#surface.write_to_png(f"{args.o}.png")  # Output to PNG
#ctx.show_page()
surface.finish()
