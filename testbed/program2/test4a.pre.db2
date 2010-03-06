connect to mydb1;
drop table t4aXXTNXX;

create table t4aXXTNXX (info char(16), age int);

commit work;
connect reset;

connect to mydb2;
drop table t4aXXTNXX;
create table t4aXXTNXX (info char(16), age int);

commit work;
connect reset;

connect to mycatdb;
--drop table dtables;
--
--create table dtables(
--   tname char(32), 
--   nodedriver char(64),
--   nodeurl char(128), 
--   nodeuser char(16),
--   nodepasswd char(16), 
--   partmtd int, 
--   nodeid int, 
--   partcol char(32),
--   partparam1 char(32), 
--   partparam2 char(32))

delete from dtables where tname='t4aXXTNXX' or tname=UCASE('t4aXXTNXX');

insert into dtables(tname,nodedriver,nodeurl,nodeuser,nodepasswd,nodeid) 
VALUES
('t4aXXTNXX',
'com.ibm.db2.jcc.DB2Driver',
'jdbc:db2://localhost:50001/mydb1',
'db2inst1',
'XXPWXX',
1),
('t4aXXTNXX',
'com.ibm.db2.jcc.DB2Driver',
'jdbc:db2://localhost:50001/mydb2',
'db2inst1',
'XXPWXX',
2);

commit work;
connect reset;

