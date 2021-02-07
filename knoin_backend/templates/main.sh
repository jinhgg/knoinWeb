echo start at `date`
perl /mnt/sda/fanxm/bin/pipeline/pipeline.pl -sc mNGS_config_sam.ini -pc mNGS_config_sys_bgi.ini -runat pbs
echo finished at `date`