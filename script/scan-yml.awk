#!/usr/bin/awk

BEGIN {
    im="";
    if (constraints==1) {
        labels="node.labels."substr(labels,5,length(labels)-5);
        gsub(" "," node.labels.",labels);
        gsub(":","==",labels);
    }
}

/image:/ {
    if (im!="") images[im]=1;
    im=$2;
}

/\/usr\/local\/bin\/docker/ {
    if (im!="") images[im]=1;
    n=split($NF,args,",");
    im=args[n];
    gsub(/[\"\]]/,"",im);
}

/- node\..*==.*/ {
    if (constraints==1) {
        if (index(labels" "role,$2)==0) im="";
    }
}

END {
    if (im!="") images[im]=1;
    for (im in images)
        print(im);
}
