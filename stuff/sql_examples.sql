sqlite3 robotathome.db

.databases
.tables
.indices
.exit
.schema <table_name>

select count(*) from raw;
87690
create index idx_raw_timestamp on raw(time_stamp);
drop index if exist idx_raw_timestamp;

explain query plan select * from raw where time_stamp > 0;
QUERY PLAN
`--SEARCH TABLE raw USING INDEX idx_raw_timestamp (time_stamp>?)

pragma index_list('raw');
pragma index_info('idx_raw_timestamp');



