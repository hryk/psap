"""Main module."""
import os
import sys
import ntpath
import datetime
import pandas as pd
from Bio import SeqIO
from scipy import signal
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from tqdm.auto import tqdm
from multiprocessing import Pool
import time

RESIDUES = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
            'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

# Kyte & Doolittle {kd} index of hydrophobicity
HP = {'A': 1.8, 'R':-4.5, 'N':-3.5, 'D':-3.5, 'C': 2.5,
      'Q':-3.5, 'E':-3.5, 'G':-0.4, 'H':-3.2, 'I': 4.5,
      'L': 3.8, 'K':-3.9, 'M': 1.9, 'F': 2.8, 'P':-1.6,
      'S':-0.8, 'T':-0.7, 'W':-0.9, 'Y':-1.3, 'V': 4.2, 'U': 0.0}

class MakeMatrix:
    def __init__(self, dbfasta):  
        self.df = pd.DataFrame()
        executables = [
             'self.fasta2df(dbfasta)',
#             'self.amino_acid_analysis()',
#             'self.idr_iupred()',
#             'self.hydrophobic()',
#             'self.add_iupred_features()',
#             'self.add_hydrophobic_features()',
#             'self.add_biochemical_combinations()',
#             'self.add_lowcomplexity_features()' ,
#             #'self.add_plaac()'
        ]        
        for e in executables:
            start = time.time()     
            print(e)
            exec(e)
            end = time.time()        
            print(str(round(end - start, 2))+'s '+e)

    def fasta2df(self, dbfasta):
        rows = list()
        with open(dbfasta) as f:
            for record in SeqIO.parse(dbfasta, 'fasta'):
                seqdict = dict()
                seq = str(record.seq)
                id = record.description.split('|')                
                if id[0] == 'sp':
                    uniprot_id = id[1]
                    name = id[2].split(' ')[0]
                    rows.append([name, uniprot_id, seq])
                elif id[0] == 'tr':
                    uniprot_id = id[1]
                    name = id[2].split(' ')[0]
                    rows.append([name, uniprot_id, seq])
                else:
                    uniprot_id = id[0]
                    name = id[2].split(' ')[0]
                    rows.append([name, uniprot_id, seq])                    
        self.df = pd.DataFrame(rows, columns=['protein_name', 'uniprot_id', 'sequence'])
        
def fasta_to_df(name, fasta_path, out_path, operating_system='Windows'):
    # Change pathing
    """ Generates and saves a file which contains features of a protein sequence.
    Parameters:
        name: Name of the file.
        fasta_path: Path of the fasta file which needs to be featured.
        operating_system: String which indicates which operating system is used only 'Windows' available.
    """
    data = MakeMatrix(fasta_path)   
    now = datetime.datetime.now()
    date = (str(now.day) + '-' + str(now.month)  + '-' +  str(now.year))
    #if operating_system == 'Windows':
    pkl = os.path.join(out_path,name,'_llps_f2f_',date,'.pkl')
    data.df.to_pickle(pkl)
    print('Generated file: ' + name + '_llps_f2f_' + date + '.pkl')
    return data.df