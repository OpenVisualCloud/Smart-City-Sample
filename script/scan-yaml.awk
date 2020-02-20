#!/usr/bin/awk

BEGIN {
    im=im2="";
    ns_space=0;
    matched=1;
}

function saveim() {
    if (im!="" && (matched || labels=="*")) {
        images[im]=1;
        im="";
    }
    if (im2!="" && (matched || labels=="*")) {
        images[im2]=1;
        im2="";
    }
    matched=1;
}

/image:/ {
    saveim();
    im=$2;
}

/VCAC_IMAGE:/ {
    im2=im;
    im=$2;
}

/- node\..*==.*/ && labels!="*" {
    gsub(/[\" ]/,"",$2);
    if (index(labels,$2)==0) {
        im=im2=""; 
        matched=0;
    }
}

/- node\..*!=.*/ && labels!="*" {
    gsub(/[\" ]/,"",$2);
    gsub(/!=/,"==",$2);
    if (index(labels,$2)!=0) {
        im=im2=""; 
        matched=0;
    }
}

/^\s*---\s*$/ {
    ns_space=0;
    saveim();
}

/- key:/ && ns_space>0 {
    match($0, /^ */);
    if (RLENGTH > ns_space) {
       key=$3
    } else {
       ns_space=0
    }
}

/operator:/ && ns_space>0 {
    match($0, /^ */);
    if (RLENGTH > ns_space) {
       operator=$2
    } else {
       ns_space=0
    }
}

/- ".*"/ && ns_space>0 {
    match($0, /^ */);
    if (RLENGTH > ns_space) {
       label_eqn=key":"$2
       gsub(/[\" ]/,"",label_eqn);
       i=index(labels,label_eqn);
       if ((operator=="In" && i==0) || (operator=="NotIn" && i!=0)) {
           im=im2=""; 
           matched=0;
       }
    } else {
       ns_space=0
    }
}

/nodeAffinity:/ {
    ns_space=index($0,"nodeAffinity:");
}

END {
    saveim();
    for (im in images)
        print(im);
}
