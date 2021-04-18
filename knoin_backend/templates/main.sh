echo start at `date`
perl /mnt/sda/fanxm/bin/pipeline/pipeline.pl -sc mNGS_config_sam.ini -pc mNGS_config_sys_bgi.ini -runat pbs
echo finished at `date`
python3 /mnt/sda/antairan/bin/result_statistics.py -i /mnt/sda/platform/result_data/{{ collection_name }}/result/classify/*.classify_abundance_result.anno.xls -o result_stat.csv
python3 /mnt/sda/antairan/bin/qc_statistics.py -i /mnt/sda/platform/result_data/{{ collection_name }}/result/filter/*/*.qc.xls -o qc_stat.csv
