drivers =  LOAD '/user/hadoop/drivers.csv' USING PigStorage(',')
AS (driverId:int, name:chararray, ssn:chararray,
location:chararray, certified:chararray, wage_plan:chararray);
ordered_data = ORDER drivers BY name asc;
DUMP ordered_data;

