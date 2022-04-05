import vcf
import sys
import re
import os

if not  os.path.exists("mgp.v5.merged.snps_all.dbSNP142.vcf.gz"):
    wget = "wget http://crispor.tefor.net/genomes/mm10/mgp.v5.merged.snps_all.dbSNP142.vcf.gz -O mgp.v5.merged.snps_all.dbSNP142.vcf.gz"
    os.system(wget)

os.system("gunzip mgp.v5.merged.snps_all.dbSNP142.vcf.gz")
r_sys="cut  -f 1-8 mgp.v5.merged.snps_all.dbSNP142.vcf > mgp.v5.merged.snps_all.dbSNP142_fourcol.vcf"
os.system(r_sys)
os.remove("mgp.v5.merged.snps_all.dbSNP142.vcf")
vcf_reader = vcf.VCFReader(open("mgp.v5.merged.snps_all.dbSNP142_fourcol.vcf"))
out1="mgp.v5.merged.snps_all.dbSNP142_AF.vcf"
out2="mm10_germline_resource.vcf"
vcf_writer = vcf.Writer(open(out1, 'w'), vcf_reader)

for rec in vcf_reader:
    DP4 = rec.INFO['DP4']
    ref_total = float(DP4[0] + DP4[1])
    alt_total = float(DP4[2] + DP4[3])
    try:
        AF = alt_total/(ref_total + alt_total)
    except:
        AF=0
    rec.INFO['AF'] = AF
    vcf_writer.write_record(rec)
vcf_writer.close()
vcf_writer.close()
os.remove("mgp.v5.merged.snps_all.dbSNP142_fourcol.vcf")
infile=open(out1,"r")
outfile=open(out2,"w")
for line in infile:
    if "##source" in line or "##FORMAT" in line:
        continue
    outfile.write(line)
    if "##INFO=<ID=DP" in line:
        TPRINT="##INFO=<ID=AF,Number=A,Type=Float,Description=\"Allele Frequency\">\n"
        outfile.write(TPRINT)

infile.close()
os.remove(out1)
outfile.close()
bgzip="bgzip "+out2
os.system(bgzip)
tbi="tabix -f -p vcf "+out2+".gz"
os.system(tbi)
