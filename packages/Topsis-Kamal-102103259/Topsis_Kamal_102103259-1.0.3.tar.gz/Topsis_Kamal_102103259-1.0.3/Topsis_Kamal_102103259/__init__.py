from .Topsis_102103259 import TOPSIS
import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("incorrect number of parameters")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]
    
    TOPSIS(input_file,weights,impacts,output_file)