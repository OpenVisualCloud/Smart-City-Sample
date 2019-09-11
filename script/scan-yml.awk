#!/usr/bin/awk

BEGIN {
    im=im2="";
    if (constraints==1) {
        labels="node.labels."substr(labels,5,length(labels)-5);
        gsub(" "," node.labels.",labels);
        gsub(":","==",labels);
    }
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

/- node\..*==.*/ {
    if (constraints==1)
        if (index(labels" "role,$2)==0)
            im=im2="";
}

END {
    saveim();
    for (im in images)
        print(im);
}
