# ABC Transposer

A simple python script to solve your transposition needs when working
with abc notation

## Requirements

Python >= 2.7

## Usage

abc-transpose.py [transpose] /path/to/input /path/to/output

Where [transpose] is one of the following:
    -u [number of semi-tones]
    -d [number of semi-tones]

Omitting the output file (or passing -c) will output it to your
terminal window.
    
OPTIONS:
-u | --up      : Number of semi-tones to increase by
-d | --down    : Number of semi-tones to decrease by
-i | --input   : The input file
-o | --output  : The output file
-c | --console : Outputs to terminal. Default output file
-n | --number  : The number in the file to transpose

## Licence

