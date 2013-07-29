# /bin/python

'''There are times when you want to transpose an abc file and are
far too lazy to transpose them yourself. This is a python script you
can use to transpose your files.

USAGE:
abc-transpose.py [transpose] /path/to/input/file /path/to/output/file

Where [transpose] is one of the following:
-u [number of semi-tones]
-d [number of semi-tones]
'''

import sys, getopt

global TRANPOSE
TRANSPOSE = [',C', ',D', ',E', ',F', ',G', ',A', ',B', "C", "D",
             "E", "F", "G", "A", "B", "c", "d", "e", "f", "g",
             "a", "b", "'c", "'d", "'e", "'f", "'g", "'a", "'b"]
TRANSPOSE_UP = []
for note in TRANSPOSE[TRANSPOSE.index("'c"):]:
    TRANSPOSE_UP.append("'" + note)
TRANSPOSE_DOWN = []
for note in TRANSPOSE[:TRANSPOSE.index("C")]:
    TRANSPOSE_DOWN.append("," + note)
    
def write_output(outfile, output):
    if outfile == -1:
        print(output.strip())
    else:
        with open(outfile, "a") as outfile:
            outfile.write(output)
            
def usage():
    print()
    print("USAGE:")
    print("abc-transpose.py [transpose] /path/to/input /path/to/output")
    print("")
    print("Where [transpose] is one of the following:")
    print("    -u [number of semi-tones]")
    print("    -d [number of semi-tones]")
    print("OPTIONS:")
    print("-u | --up      : Number of semi-tones to increase by")
    print("-d | --down    : Number of semi-tones to decrease by")
    print("-i | --input   : The input file")
    print("-o | --output  : The output file")
    print("-c | --console : Outputs to terminal. Default output file")
    print("-n | --number  : The number in the file to transpose")
    print()

def main(args):
    global transpose
    transpose = 0
    global infile
    infile = 0
    global outfile
    outfile = 0
    global number
    number = 0
    UP_OPTS = ["-u", "--up"]
    DOWN_OPTS = ["-d", "--down"]
    IN_OPTS = ["-i", "--input"]
    OUT_OPTS = ["-o", "--output"]
    CONSOLE_OPTS = ["-c", "--console"]
    NUMBER_OPTS = ["-n", "--number"]
    try:
        opts, args = getopt.getopt(args,
                                   "cu:d:i:o:n:",
                                   ["up=", "down=", "input=",
                                    "output=", "console", "number="])
        for opt, arg in opts:
            if opt in UP_OPTS:
                if transpose:
                    print("Already passed a value")
                    raise ValueError("Already passed a value")
                transpose = int(arg)
            elif opt in DOWN_OPTS:
                if transpose:
                    print("Already passed a value")
                    raise ValueError("Already passed a value")
                transpose = -int(arg)
            elif opt in IN_OPTS:
                infile = arg
            elif opt in OUT_OPTS:
                outfile = arg
            elif opt in CONSOLE_OPTS:
                outfile = -1
            elif opt in NUMBER_OPTS:
                number = int(arg)
            last_arg = arg
        return last_arg            
    except:
        usage()
        sys.exit(2)

if __name__ == "__main__":
    args = sys.argv[1:]
    last_arg = main(args)

if not(infile and outfile):
    if outfile == -1:
        infile = args[-1]
    elif last_arg == args[-1]:
        print("Need to specify the input and output files")
        sys.exit(2)
    elif last_arg == args[-2]:
        infile = args[-1]
        outfile = -1
    else:
        infile = sys.argv[-2]
        outfile = sys.argv[-1]

def description(line):
    MARKERS = "ABCDEFGHIJLMNOPQRSTUVWXYZabcdefghijlmnopqrstuvwxyz"
    for marker in MARKERS:
        if (marker + ":") in line:
            return True
    return False

def transpose_key(line):
    keys = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    scales = ["maj", "min", "dor", "phr", "lyd", "mix", "aol"]
    key = False
    for scale in scales:
        if scale in line:
            key = line[line.rfind(":")+1:line.rfind(scale)]
            used_scale = scale
    if not key:
        line = line + "maj"
        key = line[line.rfind(":")+1:line.rfind("maj")]
        used_scale = "maj"
    new_key = keys[(keys.index(key.strip()) + transpose) % len(keys)]
    return "K: " + new_key + line[line.rfind(used_scale):]

def transpose_note(note):    
    if note in TRANSPOSE:
        note = TRANSPOSE[(TRANSPOSE.index(note) + transpose)]
    return note
    
def transpose_line(line):
    buff = ""
    to_return = ""
    for character in line:
        if character in ["'", ","]:
            buff = character
        else:
            to_return += transpose_note(buff+character)
            buff = ""
    return to_return

def song_check(line, number):
    lines_number = line[line.rfind(":")+1:].strip()
    return int(lines_number) == number or number == 0

if transpose > 0:
    TRANSPOSE.append(TRANSPOSE_UP)
else:
    TRANSPOSE.append(TRANSPOSE_DOWN)
    
with open(infile) as infile:
    for line in infile:
        if "X:" in line or "x:" in line:
            do_song = song_check(line, number)
        if do_song and not description(line):
            if "K:" in line or "k:" in line:
                out = transpose_key(line)
            else:
                out = transpose_line(line)
            write_output(outfile, out)
        else:
            write_output(outfile, line)
