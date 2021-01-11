[config]
runposition=pbs
sections=fastp,kraken2,kracal,rgi

[dir]
outDir=/home/lijh/mNGS/result
filter=$outDir/filter
kraken=$outDir/kraken
card_rgi=$outDir/card_rgi

[sample]

LX2004622=123

LX2004622=456

LX2004622=888

# LX2004622=/mnt/sda/project/rawdata/20201203/S200012080_L01_64.fq.gz
ctrl=sdfsdfddddddd

[pbs]
queue=batch