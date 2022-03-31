#wget ftp-mouse.sanger.ac.uk/REL-1505-SNPs_Indels/mgp.v5.merged.indels.dbSNP142.normed.vcf.gz -O mgp.v5.indels.vcf.gz
python3 - << EOF
import gzip
import re
f=open("mgp.v5.indels.pass.chr.vcf","w")
with gzip.open('mgp.v5.indels.vcf.gz','r') as fin:
    for line in fin:
        line=line.decode('utf-8')
        if "##contig" in line:
            chr=re.findall("ID=(\d{1,2}|X|Y|MT)",line)
            newID="ID=chr"+chr[0]
            line=re.sub("ID=(\d{1,2}|X|Y)",newID,line)
        if not "#" in line and "PASS" in line:
            line="chr"+line
        elif not "#" in line and not "PASS" in line:
            continue
        f.write(line)
f.close
EOF
# keep only passing and adjust chromosome name
bcftools sort mgp.v5.indels.pass.chr.vcf -o mouse_mm10_germline_resource.vcf
bgzip mouse_mm10_germline_resource.vcf
tabix -f -p vcf mouse_mm10_germline_resource.vcf.gz
rm mgp.v5.indels.pass.chr.vcf
rm mgp.v5.indels.vcf.gz
