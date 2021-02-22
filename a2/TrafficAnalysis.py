#!/usr/bin/python3

import struct
import argparse
import sys

def OPEN_FILE():
    # open the cap file from argumnet
    parser = argparse.ArgumentParser()                                               
    parser.add_argument("cap_file", help="Specify the cap file you wish to open") 
    args = parser.parse_args()   
    cap_file = args.cap_file   # Website name parsed from the command line
    #Add checks for error handling before returning to main (if file ends in .cap, if file specified etc.)
    return cap_file


def main():
    cap_file = OPEN_FILE()
    print(cap_file)



if __name__ == "__main__":
    main()