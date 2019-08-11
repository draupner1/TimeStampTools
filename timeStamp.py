#!/usr/bin/env python2
import argparse
import csv
from datetime import datetime

# DraupnerData Python TimeStamp postProcessing

# example execution:
# ./timeStamp.py --hide Play CurrentFile20190731.cvs

# ============================================================

def print_it(args, pa, pd, pt):
    if args.hide != pa:
      print pa,';',pd,';',pt

# ============================================================

def calc_delta_time(args, sadt_tl):
    cd = None
    for row in sadt_tl:
      if cd != None:    # Init detection
        if cd == row[1].date(): # Same date > compare times
          dt = row[1] - ct
        else:                   # Different date > compare to 23.59.59
          dt = ct.replace(hour=23, minute=59, second=59) - ct
        print_it(args, ca, cd, dt)
        # Prepare for next row
      cd = row[1].date()
      ct = row[1]
      ca = row[0]
    dt = ct.replace(hour=23, minute=59, second=59) - ct # last to 23.59
    print_it(args, ca, cd, dt)

# ============================================================

def cmd_do(args):
    infile = args.infile
    adt_tuple_list = []

    print infile
    with open(infile, 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=';')
      for row in spamreader:
        if len(row) > 1:
          datetime_object = datetime.strptime(row[1], '%Y.%m.%d %H:%M')
          #print 'dto', row[0],datetime_object  # print unsorted data
          adt_tuple = (row[0], datetime_object)
          adt_tuple_list.append(adt_tuple)
# sort list by datetime
    s_adt_t_l = sorted(adt_tuple_list, key=lambda dto: dto[1])
    #for act in s_adt_t_l:  # print sorted tuple list
    #  print 'sto', act[0], ';', act[1]

# calc and print the time-diffs per date
    calc_delta_time(args, s_adt_t_l)

# ============================================================

def main():
    parser = argparse.ArgumentParser(
             description=("TimeStamp CurrentFile postProcessing tool"))
    parser.add_argument("infile", 
            help="The currentFile.csv from TimeStamp to process")
    parser.add_argument("--hide",
            help="Hide one Action when printing")
    parser.set_defaults(func=cmd_do)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
