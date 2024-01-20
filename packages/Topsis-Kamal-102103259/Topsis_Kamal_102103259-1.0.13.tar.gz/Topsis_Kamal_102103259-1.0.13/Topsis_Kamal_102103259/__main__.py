import sys
import numpy as np
import pandas as pd

def TOPSIS(input_file,weights,impacts,output_file):
    
    if input_file.lower().endswith('.xlsx'):
        data = pd.read_excel(input_file)
    elif input_file.lower().endswith('.csv'):
        data = pd.read_csv(input_file)
    else:
        print("unsupported file format")
        sys.exit(1)
    normalized_data = data.iloc[:,1:]
    weights = [float(w) for w in weights.split(',')]
    impacts = [str(s) for s in impacts.split(',')]
    
    if len(weights) != len(normalized_data.columns) or len(impacts) != len(normalized_data.columns):
        print("Error: Number of weights or impacts does not match the number of columns in the input data.")
        sys.exit(1)
    
    normalized_data = normalized_data/np.sqrt((normalized_data**2).sum())
    weighted_normalized_data = normalized_data*weights
    
    ideal_best = np.max(weighted_normalized_data,axis = 0)
    ideal_worst = np.min(weighted_normalized_data,axis = 0)
    
    separation_best = np.sqrt(((weighted_normalized_data-ideal_best)**2).sum(axis =1))
    separation_worst = np.sqrt(((weighted_normalized_data-ideal_worst)**2).sum(axis = 1))
    
    topsis_scores =separation_worst/(separation_worst+separation_best)
    
    ranks = topsis_scores.rank(ascending = False)
    data['Topsis Score'] = topsis_scores
    data['Rank'] = ranks
    
    data.to_csv(output_file,index = False)
        

    
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("incorrect number of parameters")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]
    
    TOPSIS(input_file,weights,impacts,output_file)