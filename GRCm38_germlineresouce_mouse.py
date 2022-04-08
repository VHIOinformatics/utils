import vcf
import sys
import re
import os
import gzip
mgp_url="ftp-mouse.sanger.ac.uk/REL-1807-SNPs_Indels/mgp.v6.merged.norm.snp.indels.sfiltered.vcf.gz"
mgp=mgp_url.split("/")[-1]
if not  os.path.exists(mgp):
    wget = "wget "+mgp_url
    os.system(wget)

if not os.path.exists("GRCm38_germline_resource.vcf"):

    o=open("GRCm38_germline_resource.vcf","w")
    l="##fileformat=VCFv4.2\n##FILTER=<ID=PASS,Description=\"All filters passed\">\n##reference=file:///nfs/production/mousegenomes/projects/REL-17/reference/GRCm38_68.fa\n"
    o.write(l)
    with gzip.open(mgp,'r') as fin:
        for line in fin:
            line=line.decode("utf-8")
            if ("##contig" in line) or ("CHROM" in line) or ("ID=AC" in line):
                if "##INFO" in line and "ID=AC" in line:
                    line+="##INFO=<ID=AF,Number=A,Type=Float,Description=\"Allele Frequency\">\n"
                if "CHROM" in line:
                    tmp=line.split("\t")
                    line="\t".join(tmp[0:8])+"\n"
                o.write(line)
            elif not "#" in line:
                tmp=line.split("\t")
                l="\t".join(tmp[0:6])+"\tPASS\t"
                DP4= list(filter(lambda a: 'DP4' in a, tmp[7].split(";")))[0].split("=")[1].split(",")
                AC= list(filter(lambda a: 'AC' in a, tmp[7].split(";")))[0]
                
                ref_total = float(DP4[0] + DP4[1])
                alt_total = float(DP4[2] + DP4[3])
                try:
                    AF = str(alt_total/(ref_total + alt_total))
                except:
                    AF=str(0)
                l+="AF="+AF[0:6]+";"+AC+"\n"
                o.write(l)

    o.close()
bgzip="bgzip GRCm38_germline_resource.vcf "
os.system(bgzip)
tbi="tabix -f -p vcf GRCm38_germline_resource.vcf.gz"
os.system(tbi)
