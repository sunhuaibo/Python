#!/usr/bin/env python
import sys
from gzip import open as gz_open
import argparse
parser = argparse.ArgumentParser(description="seqIO functions (fasta,fastq)")
parser.add_argument('-i','--input',help='input file path',required=True)
parser.add_argument('-o','--output',help='output file name',default='seq.fasta')
parser.add_argument('-t','--file_type',help='The input sequences file type (either "fastq" or "fasta")',choices=['fasta','fastq'],required=True)
#args=vars(parser.parse_args())         # not identify unknows arguments
args, remaining = parser.parse_known_args()     # unknows arguments loaded into remaining
#args, remaining = parser.parse_known_args(sys.argv)    # including python script name
#print remaining
#print args.out
args = vars(args)           # dict
#print args.keys()
def read_fasta(fa):
    ''' This function is read fasta format file.
        Argument is a filehandle of fasta. 
        Return value is (name,seq). 
    '''
    name , seq = '' , []
    name = fa.readline().rstrip()[1:]
    while True:
        line = fa.readline().rstrip()
        if not line:
            break
        elif line.startswith('>'):
            yield (name, ''.join(seq))
            name, seq = line[1:], []
        else:
            seq.append(line)
    if name: 
        yield (name, ''.join(seq))

def read_fastq(fq):
    ''' This function is read fastq format file.
        Argument is a filehandle of fastq.
        Return value is (name,seq,qual).
    '''
    while True:
        seq_name = fq.readline().rstrip()
        if not seq_name: break
        seq_base = fq.readline().rstrip()
        seq_name2 = fq.readline().rstrip()
        seq_qual = fq.readline().rstrip()
        yield (seq_name, seq_base, seq_qual)

def main():
#    fr_type = {}
#    fr_type['fasta'] = read_fasta
#    fr_type['fastq'] = read_fastq
#    sequence_read_fp = sys.argv[1]
    sequence_read_fp = args['input']
    fw = open(args["output"],'w')
    if sequence_read_fp.endswith('.gz'):
        sequence_read_f = gz_open(sequence_read_fp, 'rb')
    else:
        sequence_read_f = open(sequence_read_fp, 'U')
    if args['file_type'] == 'fastq':
        for seq_name, seq_base ,seq_qual in read_fastq(sequence_read_f):
#            print "%s\n%s\n%s" %(seq_name,seq_base,seq_qual)
            fw.write("%s\n%s\n%s" %(seq_name,seq_base,seq_qual)+"\n")
    if args['file_type'] == 'fasta':
        for seq_name, seq_base in read_fasta(sequence_read_f):
#            print ">%s\n%s" %(seq_name,seq_base)
            fw.write(">%s\n%s" %(seq_name,seq_base)+"\n")
    sequence_read_f.close()
    fw.close()

if __name__ == '__main__':
    main()
