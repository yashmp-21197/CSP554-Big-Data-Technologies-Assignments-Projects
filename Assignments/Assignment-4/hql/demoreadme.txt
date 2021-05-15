Use scp to move the hql.zip demo file to your EMR master node (/home/hadoop).

Once the demo file is on your master node decomporess it using 'unzip hql.zip'.

To use this demo make sure your current directory is /home/hadoop/hql
by entering:

cd /home/hadoop/hql

Then start up the Hive Beeline by entering:

beeline -u jdbc:hive2://localhost:10000/ -n hadoop -d org.apache.hive.jdbc.HiveDriver --showDbInPrompt 

Now enter the following into Beeline:
1) source ./basicsetup.hql;
2) source ./partsetup.hql;
3) source ./salaries.hql;
4) source ./loadsalaries.hql;
5) source ./salaries2.hql;
6) source ./salaries3.hql;        <- this takes a while



