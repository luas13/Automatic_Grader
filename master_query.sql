use ABC;
show tables;
select * from table_name;

-- 1.	Write an SQL query to retrieve the Department Name of the employee whose ID is 10.
select DepartmentName from employee where EmployeeID=10;

-- 2.	Display data for a given condition:
SELECT EMP_ID, LAST_NAME
FROM EMPLOYEE_TBL
WHERE EMP_ID = '333333333';


-- 3.	Retrieve column_name1 from table_name where corresonding values of 2 column_1 and column_2 are same.
SELECT column_name1 
FROM table_name 
WHERE column_1 = value_1 AND column_2 = value_2;


-- 4.	Retrive maximum value of column_name from table_name. (Check I just wrote ; as I don't know the answer.)
; 


-- 5.	Retrive all records from a table and displaying all columns:
SELECT * FROM table_name;