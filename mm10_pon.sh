#wget --recursive --no-parent --no-directories --accept vcf*vcf.gz ftp://ftp.ncbi.nih.gov/snp/organisms/archive/mouse_10090/VCF/
rm vcf_chr_AltOnly.vcf.gz vcf_chr_Multi.vcf.gz vcf_chr_NotOn.vcf.gz vcf_chr_Un.vcf.gz 00-All.vcf.gz

for vcf in $(ls -1 *.vcf.gz) ; do
  vcf_new=${vcf/.vcf.gz/.vcf}
  echo $vcf
  zcat $vcf | sed 's/^\([0-9XY]\)/chr\1/' > $vcf_new
  rm -fv $vcf
done

ls *vcf | xargs -i bgzip {}
ls *vcf.gz |xargs -i tabix -f -p vcf {}
ls *vcf.gz > files.txt
bcftools concat -a -f  files.txt -o concat.vcf 
bcftools sort concat.vcf -o mouse_mm10_pon.vcf
bgzip mouse_mm10_pon.vcf
tabix -f -p vcf mouse_mm10_pon.vcf.gz
rm vcf_chr_* concat.vcf files.txt
