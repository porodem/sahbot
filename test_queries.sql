create table ls_adr_split(id int8 generated always as identity,
ls text, district text,
adr text, city text, str text, house text, kv text, adr_len int);

copy ls_address from 'C:\Python\Python310\Scripts\sahbot\lss\full.csv' delimiter ';' csv encoding 'WIN-1251'

drop table ls_adr_split

truncate ls_adr_split 

with tt as (
select 
sah_ls , district ,
adr,
string_to_array(adr,',') a
from ls_address where --sah_ls = '13103111309'
district <> 'Железнодорожный'
)
insert into ls_adr_split(ls, district , adr, city, str, house, kv, adr_len) 
select 
sah_ls ,
district,
adr,
a[1] city,
a[2] str,
trim(a[3]) house,
trim(a[4]) kv,
--array_length(a,1),
cardinality(a) a_len
from tt


with tt as (
select 
adr,
string_to_array(adr,',') a
from ls_address 
where sah_ls = '13103111309'
--adr ~* 'шамшурина'
)
select 
adr,
a[1], a[2], trim(a[3]), a[4],
array_length(a,1),
cardinality(a)
from tt

select * from ls_adr_split a
where a.str ~* 'владимировская'
and house ~* '^3$'
and kv = '7'