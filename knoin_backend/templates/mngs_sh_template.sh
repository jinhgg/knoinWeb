[config]
runposition=pbs
sections=fastp,kraken2,kracal,rgi

[dir]
outDir=/home/lijh/mNGS/result
filter=$outDir/filter
kraken=$outDir/kraken
card_rgi=$outDir/card_rgi

[sample]
{% for sample in sample_list %}
LX2004622={{ sample }}
{% endfor %}
# LX2004622=/mnt/sda/project/rawdata/20201203/S200012080_L01_64.fq.gz
ctrl={{ ctrl }}

[pbs]
queue=batch