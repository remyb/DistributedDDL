connect to mydb1;
select * from t4aXXTNXX
order by info;
drop table t4aXXTNXX;
connect reset;

connect to mydb2;
select * from t4aXXTNXX
order by info;
drop table t4aXXTNXX;
connect reset;

connect to mycatdb;

SELECT nodeid, partmtd, partcol, partparam1, partparam2 
FROM dtables 
WHERE tname='t4aXXTNXX' or tname=UCASE('t4aXXTNXX')
order by nodeid;

connect reset;

