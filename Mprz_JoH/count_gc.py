#!/usr/bin/env python
# author: suyankai@ioz.ac.cn
# date: 2024-05-30
fa_file = open("scaffolds.review_v2.fasta","r")
out_file = open("scaffolds.review_v2.gc.stat.txt","w")
seqid = ""
seq_dict = {}
for line in fa_file.readlines():
	line = line.strip()
	if line.startswith(">"):
		seqid = line.replace(">","").replace("Chromosome","Chr")
		seq_dict[seqid] = ""
	else:
		#gc = line.count("G")+line.count("C")+line.count("g")+line.count("c")
		seq_dict[seqid] += line

for seq in seq_dict.keys():
	num = len(seq_dict[seq]) // 1000000 + 1 
	for i in range(num):
		if i == num - 1 :
			start = 1000000 * i
			end = len(seq_dict[seq])
		else:
			start = 1000000 * i
			end = start + 1000000
		fragseq = seq_dict[seq][start:end]
		length = end - start
		gc = fragseq.count("G")+fragseq.count("C")+fragseq.count("g")+fragseq.count("c")
		out_file.write(seq+"\t"+str(start+1)+"\t"+str(end)+"\t"+str(format(gc/length,".4f"))+"\n")

fa_file.close()
out_file.close()
