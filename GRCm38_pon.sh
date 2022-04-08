mkdir vcf
wget --recursive --no-parent --no-directories --accept vcf.gz ftp://ftp.ncbi.nih.gov/snp/organisms/archive/mouse_10090/VCF/
rm vcf_chr_AltOnly.vcf.gz vcf_chr_Multi.vcf.gz vcf_chr_NotOn.vcf.gz vcf_chr_Un.vcf.gz
ls ./vcf/*vcf.gz |xargs -i tabix -f -p vcf {}
ls ./vcf/*vcf.gz > files.txt
bcftools concat -a -f  files.txt -o concat.vcf 
cat concat.vcf|awk '! a[$0]++'> unique.vcf
bcftools sort unique.vcf -o binary.vcf

bgzip mouse_GRCm38_pon.vcf
tabix -f -p vcf mouse_GRCm38_pon.vcf.gz
rm vcf_chr_* concat.vcf files.txt 00-All.vcf.gz unique.vcf
