echo start at `date`
perl /mnt/sda/fanxm/bin/pipeline/pipeline.pl -sc {{ sam_ini_path }} -pc {{ sys_ini_path }} -runat pbs
echo finished at `date`