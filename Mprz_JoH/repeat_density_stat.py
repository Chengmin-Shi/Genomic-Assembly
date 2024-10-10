#!/usr/bin/env python
# author: suyankai@ioz.ac.cn
# date: 2024-05-30

import sys
repeat_file = open(sys.argv[1],"r")
chrLen_file = open("scaffolds.review.fasta.chrLen.txt","r")
out_file = open(sys.argv[2],"w")

chr_list = []
chrLen_dict = {}
for line in chrLen_file.readlines():
    line = line.strip()
    if line.startswith("C"):
        arr = line.split()
        chrLen_dict[arr[0]] = int(arr[1])
        chr_list.append(arr[0])

repeat_dict = {}
for line in repeat_file.readlines():
    line = line.strip()
    if line.startswith("C"):
        arr = line.split("\t")
        if arr[0] in repeat_dict:
            repeat_dict[arr[0]].append(line)
        else:
            repeat_dict[arr[0]] = [line]


for chrom in chr_list:
    num = chrLen_dict[chrom] // 1000000 + 1
    for i in range(num):
        total_base = 0
        if i == num - 1:
            start = i*1000000 + 1 
            end = chrLen_dict[chrom]
        else:
            start = i*1000000 + 1 
            end = start + 1000000 - 1 
        for repeat in repeat_dict[chrom]:
            arr = repeat.split("\t")
            rep_start = int(arr[3])
            rep_end = int(arr[4]) 
            if rep_start >= start and end >= rep_end:
                total_base += (rep_end - rep_start + 1)
            elif  start >= rep_start and end >= rep_end and rep_end >= start:
                total_base += (rep_end - start + 1)
            elif end >= rep_start and rep_end >= end and rep_start >= start:
                total_base += (end - rep_start + 1)
            else:
                continue
        out_file.write(chrom+"\t"+str(start)+"\t"+str(end)+"\t"+'{:.4f}'.format(total_base / (end-start + 1))+"\n")


repeat_file.close()
chrLen_file.close()
out_file.close()
