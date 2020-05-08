define(`loop',`ifelse(eval($2<=$3),1,`pushdef(`$1',$2)$4`'loop(`$1',incr($2),$3,`$4')popdef(`$1')')')dnl
