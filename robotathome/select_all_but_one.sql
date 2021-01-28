SELECT "CREATE TEMP VIEW my_view_1 AS SELECT " ||  (
SELECT 
    group_concat(name, ', ') 
FROM 
    pragma_table_info('raw') 
WHERE 
    name != 'id') || 
" FROM raw";