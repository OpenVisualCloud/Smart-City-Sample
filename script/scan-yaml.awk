#!/usr/bin/awk

BEGIN {
    im="";
    n_space=c_space=0;
    matched=1;
}

function saveim() {
    split(im,ims,",");
    for (i in ims) {
        if (ims[i]!="" && (matched || labels=="*")) {
            images[ims[i]]=1;
        }
    }
    im="";
    matched=1;
}

/containers:/ {
    c_space=index($0,"containers:");
}

/initContainers:/ {
    c_space=index($0,"initContainers:");
}
    
/image:/ && c_space==0 {
    saveim();
    im=$2;
}

/image:/ && c_space>0 {
    im=im","$2
}

/VCAC_IMAGE:/ {
    im=im","$2
}

/- node\..*==.*/ && labels!="*" {
    gsub(/[\" ]/,"",$2);
    if (index(labels,$2)==0) {
        im=""; 
        matched=0;
    }
}

/- node\..*!=.*/ && labels!="*" {
    gsub(/[\" ]/,"",$2);
    gsub(/!=/,"==",$2);
    if (index(labels,$2)!=0) {
        im=""; 
        matched=0;
    }
}

/^\s*---\s*$/ || /^\s*$/ {
    n_space=c_space=0;
    saveim();
}

/- key:/ && n_space>0 {
    match($0, /^ */);
    if (RLENGTH > n_space) key=$3
}

/operator:/ && n_space>0 {
    match($0, /^ */);
    if (RLENGTH > n_space) operator=$2
}

/- ".*"/ && n_space>0 {
    match($0, /^ */);
    if (RLENGTH > n_space) {
       label_eqn=key":"$2
       gsub(/[\" ]/,"",label_eqn);
       i=index(labels,label_eqn);
       if ((operator=="In" && i==0) || (operator=="NotIn" && i!=0)) {
           im=im2=""; 
           matched=0;
       }
    }
}

/nodeAffinity:/ {
    n_space=index($0,"nodeAffinity:");
}

END {
    saveim();
    for (im in images)
        print(im);
}
