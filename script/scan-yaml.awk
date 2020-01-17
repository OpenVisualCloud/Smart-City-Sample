#!/usr/bin/awk

BEGIN {
    im=im2="";
    ns_space=0;
    matched=0;
    vcac=index(labels,"vcac-zone:yes")>0 || index(labels,"vcac_zone==yes")>0;
}

function saveim() {
    if (im!="" && (matched || !vcac)) {
        images[im]=1;
        im="";
    }
    if (im2!="" && (matched || !vcac)) {
        images[im2]=1;
        im2="";
    }
    matched=0;
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
    if (index(labels,$2)==0) im=im2=""; else matched=1;
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
        if (index(labels,$1":"$2)==0) im=im2=""; else matched=1;
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
