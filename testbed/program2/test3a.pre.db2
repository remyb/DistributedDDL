connect to mydb1;
drop table t3aXXTNXX;

create table t3aXXTNXX (info char(16));

insert into t3aXXTNXX VALUES('db1d1'), ('db1d2'), ('db1d3');

commit work;
connect reset;

connect to mydb2;
drop table t3aXXTNXX;
create table t3aXXTNXX (info char(16));

insert into t3aXXTNXX VALUES('db2d1'), ('db2d2'), ('db2d3');

commit work;
connect reset;

connect to mycatdb;
drop table dtables;

create table dtables(
   tname char(32), 
   nodedriver char(64),
   nodeurl char(128), 
   nodeuser char(16),
   nodepasswd char(16), 
   partmtd int, 
   nodeid int, 
   partcol char(32),
   partparam1 char(32), 
   partparam2 char(32));

insert into dtables(tname,nodedriver,nodeurl,nodeuser,nodepasswd,nodeid) 
VALUES
('t3aXXTNXX',
'com.ibm.db2.jcc.DB2Driver',
'jdbc:db2://localhost:50001/mydb1',
'db2inst1',
'XXPWXX',
1),
('t3aXXTNXX',
'com.ibm.db2.jcc.DB2Driver',
'jdbc:db2://localhost:50001/mydb2',
'db2inst1',
'XXPWXX',
2);

commit work;
connect reset;

