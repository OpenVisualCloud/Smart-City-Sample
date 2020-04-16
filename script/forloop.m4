# Copyright (C) 2006, 2010-2012 Free Software Foundation, Inc.
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.
divert(`-1')
# forloop(var, from, to, stmt) - improved version:
#   works even if VAR is not a strict macro name
#   performs sanity check that FROM is larger than TO
#   allows complex numerical expressions in TO and FROM
define(`forloop', `ifelse(eval(`($2) <= ($3)'), `1',
  `pushdef(`$1')_$0(`$1', eval(`$2'),
    eval(`$3'), `$4')popdef(`$1')')')
define(`_forloop',
  `define(`$1', `$2')$4`'ifelse(`$2', `$3', `',
    `$0(`$1', incr(`$2'), `$3', `$4')')')
divert`'dnl
