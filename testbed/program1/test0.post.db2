connect to mydb1;
select * from XXTNXX;
connect reset;

connect to mydb2;
select * from XXTNXX;
connect reset;

connect to mycatdb;

select nodedriver, nodeurl, nodeuser 
from dtables
where tname='XXTNXX' or tname=UCASE('XXTNXX')
order by nodeurl;


