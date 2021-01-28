-- USEFUL EXAMPLES

-- copy a table to another table
INSERT INTO Destination SELECT * FROM Source;

-- correlated subquery
SELECT *
FROM Table1
WHERE EXISTS (SELECT 1
              FROM Table2
              WHERE Table1.Value BETWEEN Table2.StartValue AND Table2.EndValue);
			  
-- get the first time_stamp			  
select min(time_stamp) from raw

-- add column
alter table aux_raw add column labelled integer not null default 0;