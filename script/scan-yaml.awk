#!/usr/bin/awk

BEGIN {
    im=im2="";
    ns_space=0;
}

function saveim() {
    if (im!="") {
        images[im]=1;
        im="";
    }
    if (im2!="") {
        images[im2]=1;
        im2="";
    }
}

/image:/ {
    saveim();
    im=$2;
}

/command:\s+\["-/ {
    im2=im;
    n=split($NF,args,",");
    im=args[n];
    gsub(/[\"\]]/,"",im);
}

/- node\..*==.*/ && labels!="*" {
    gsub(/[\" ]/,"",$2);
    if (index(labels,$2)==0) im=im2="";
}

/^\s*---\s*$/ {
    ns_space=0;
    saveim();
}

/:/ && ns_space>0 {
    match($0, /^ */);
    if (RLENGTH > ns_space) {
        gsub(/[\": ]/,"",$1);
        gsub(/[\": ]/,"",$2);
        if (index(labels,$1":"$2)==0) im=im2="";
    } else {
       ns_space=0
    }
}

/nodeSelector:/ {
    ns_space=index($0,"nodeSelector:");
}

END {
    saveim();
    for (im in images)
        print(im);
}
