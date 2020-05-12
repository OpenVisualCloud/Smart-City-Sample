define(`loop',`ifelse(eval($2<=$3),1,`pushdef(`$1',$2)$4`'loop(`$1',incr($2),$3,`$4')popdef(`$1')')')dnl
define(`loopifdef',`pushdef(`$1',$2)ifdef($3,`$4loopifdef(`$1',incr($2),`$3',`$4')')popdef(`$1')')dnl
define(`looplist',`pushdef(`$1',regexp($2,`\(\w+\)',`\1'))ifelse(regexp($2,`\w+'),-1,,`$3looplist(`$1',regexp($2,`\w+[/ ]*\(.*\)',`\1'),`$3')')popdef(`$1')')dnl
