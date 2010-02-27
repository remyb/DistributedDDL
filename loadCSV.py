#!/usr/bin/env python

filename = "csvfile"
contents = []
for line in open(filename):
  fields = line.split(',');
  number = fields[0]
  title = fields[1]
  author = fields[2]
  book = (number,title,author)
  contents.append(book)
  
print contents[0][1] +" is title of first csv" # test