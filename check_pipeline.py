#!/usr/bin/python
import sys,os
if len(sys.argv) < 2:
	print "Usage: python %s <current_dir> <sample.list>" % sys.argv[0]
	exit()

cdir = sys.argv[1]
sample = sys.argv[2]
#cdir_tmp =cdir + "/check"

#if not os.path.isdir(cdir_tmp):
#	os.mkdir(cdir_tmp)

fr = open(sample,'r')
i = 1
for line in fr:
	line =line.strip().split("\t")
	if i < 3:
		pass
	else:
		outshell = cdir + "/check_%s.sh" %(line[0])
		fw = open(outshell,'w')
		code = "cd %s\n" %cdir
		code += "/mnt/NL200/sunshuai/pipeline/checkVariation/snv_post.sh -hs37 -step 1 -sample %s -indir variation/ -outdir check/\n" %(line[0])
		code += "/mnt/NL200/sunhb/script/perl/health_flt.pl -in check/check_snv/%s/snv.filter.info.bed -out check/check_snv/%s/snv.health_flt.bed\n" %(line[0],line[0])
		code += "/mnt/NL200/sunshuai/pipeline/check_peizhh/autocheckcnv_bp.v4.sh -I variation/%s -v %s -o check/check_cnv -p %s\n" %(line[0],"v11",line[0])
		code += "/mnt/NL200/sunshuai/softwares/bin/check_sv.pl -bam variation/%s/cancer/5_recal_bam/*realign_recal.bam -sv variation/%s/report/somatic_var/*.sv.csv -prefix check/check_sv/%s\n" %(line[0],line[0],line[0])
		fw.write(code)
		fw.close()
		os.system("qsub -cwd -V -l vf=500m -q large.q %s" %outshell)
	i += 1
fr.close()

