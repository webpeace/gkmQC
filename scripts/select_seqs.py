#!/usr/bin/env python
"""
    select_seqs.py: select a subset of sequences from a given FASTA sequence file

    Copyright (C) 2013 Dongwon Lee
"""

import sys

def generate_kmers(kmerlen):
    """make a full list of k-mers 

    Arguments:
    kmerlen -- integer, length of k-mer

    Return:
    a list of the full set of k-mers
    """

    nts = ['A', 'C', 'G', 'T']
    kmers = [] 
    kmers.append('')
    l = 0
    while l < kmerlen: 
        imers = [] 
        for imer in kmers:
            for nt in nts: 
                imers.append(imer+nt)
        kmers = imers
        l += 1 
    
    return kmers


def revcomp(seq):
    """get reverse complement DNA sequence

    Arguments:
    seq -- string, DNA sequence

    Return:
    the reverse complement sequence of the given sequence
    """
    rc = {'A':'T', 'G':'C', 'C':'G', 'T':'A'}
    return ''.join([rc[seq[i]] for i in xrange(len(seq)-1, -1, -1)])


def generate_rcmap_table(kmerlen, kmers):
    """make a lookup table for reverse complement k-mer ids for speed 

    Arguments:
    kmerlen -- integer, length of k-mer
    kmers -- list, a full set of k-mers generated by generate_kmers

    Return:
    a dictionary containing the mapping table
    """
    revcomp_func = revcomp

    kmer_id_dict = {}
    for i in xrange(len(kmers)): 
        kmer_id_dict[kmers[i]] = i

    revcomp_mapping_table = []
    for kmerid in xrange(len(kmers)): 
        rc_id = kmer_id_dict[revcomp_func(kmers[kmerid])]
        if rc_id < kmerid:
            revcomp_mapping_table.append(rc_id)
        else:
            revcomp_mapping_table.append(kmerid)
    
    return revcomp_mapping_table


def read_fastafile(filename, subs=True):
    """Read sequences from a file in FASTA format

    Arguments:
    filename -- string, the name of the sequence file in FASTA format
    subs -- bool, substitute 'N' with 'A' if set true

    Return: 
    list of sequences, list of sequence ids
    """

    sids = []
    seqs = []

    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

    except IOError as err:
        print("I/O error: ", err)
        sys.exit(0)

    seq = [] 
    for line in lines:
        if line[0] == '>':
            sids.append(line[1:].rstrip('\n').split()[0])
            if seq != []: seqs.append("".join(seq))
            seq = []
        else:
            if subs:
                seq.append(line.rstrip('\n').replace('N', 'A').upper())
            else:
                seq.append(line.rstrip('\n').upper())

    if seq != []:
        seqs.append("".join(seq))

    return seqs, sids

def print_fasta_seq(seqid, seq):
    print(">" + seqid)
    print(seq)

def read_coordfile(filename):
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

    except IOError as err:
        print("I/O error: ", err)
        sys.exit(0)

    coords = []
    for line in lines:
        l = line.split()
        c = l[0]
        if (c.find('.') == -1) and (c.find(':') == -1) and (c[0:3] == "chr"):
            c = ':'.join([l[0], '-'.join([str(int(l[1])+1), l[2]])]) #convert bed to position

        coords.append(c)

    return coords

def main(argv=sys.argv):
    if len(argv) != 3:
        print(sys.argv[0] + " <sequence file> <coord file>")
        sys.exit()

    fastafile = argv[1]
    coordfile  = argv[2]

    seqs, ids = read_fastafile(fastafile, subs=False)
    coords = read_coordfile(coordfile)

    id_seq_dict = {}

    for i in range(len(ids)):
        id_seq_dict[ids[i]] = seqs[i]

    for pos in coords:
        if pos in id_seq_dict:
            print_fasta_seq(pos, id_seq_dict[pos])


if __name__=='__main__': main()
