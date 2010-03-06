connect to mydb1;
drop table XXTNXX;
commit work;
connect reset;

connect to mydb2;
drop table XXTNXX;
commit work;
connect reset;

connect to mycatdb;
drop table dtables;
commit work;
connect reset;

