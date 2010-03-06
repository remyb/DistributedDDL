src=3a
tgt=4a
cmd="cp"

$cmd test$src.cfg test$tgt.cfg
$cmd test$src.post.db2 test$tgt.post.db2
#$cmd test$src.post.db2.exp test$tgt.post.db2.exp
$cmd test$src.pre.db2 test$tgt.pre.db2
#$cmd test$src.sql test$tgt.sql
