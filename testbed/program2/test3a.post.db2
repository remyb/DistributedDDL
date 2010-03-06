connect to mydb1;
--select * from t3aXXTNXX;
drop table t3aXXTNXX;
connect reset;

connect to mydb2;
--select * from t3aXXTNXX;
drop table t3aXXTNXX;
connect reset;

connect to mycatdb;

delete from dtables where tname='t3aXXTNXX';

connect reset;

