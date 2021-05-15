Use scp to move the pigdemo.zip demo file to your EMR master 
node (/home/hadoop).

Once the demo file is on your master node decompress it using 
'unzip pigdemo.zip'.

To use this demo make sure your current directory is 
/home/hadoop/pigdemo by doing 'cd /home/hadoop/pigdemo'.

Copy some â€œ.csvâ€ data files from the pigdemo directory into 
HDFS as follows: hadoop fs -copyFromLocal *.csv /user/hadoop

Then start up the Pig CLI by entering 'pig'.

Now enter the following into the Pig CLI:

1) exec define_relation.pig
2) exec define_relation_w_schema.pig
3) exec define_new_rel_from_existing.pig
4) exec select_cols.pig
5) exec group_by_driverid.pig
6) exec order_by_name.pig
7) exec perform_join.pig

