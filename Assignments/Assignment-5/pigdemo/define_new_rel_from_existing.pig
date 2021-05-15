truck_events = LOAD '/user/hadoop/truck_event_text_partition.csv' USING PigStorage(',')
AS (driverId:int, truckId:int, eventTime:chararray,
eventType:chararray, longitude:double, latitude:double,
eventKey:chararray, correlationId:long, driverName:chararray,
routeId:long,routeName:chararray,eventDate:chararray);
DESCRIBE truck_events;
truck_events_subset = LIMIT truck_events 100;
DESCRIBE truck_events_subset;

