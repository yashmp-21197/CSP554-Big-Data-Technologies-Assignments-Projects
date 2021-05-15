truck_events = LOAD '/user/hadoop/truck_event_text_partition.csv' USING PigStorage(',');
DESCRIBE truck_events;

