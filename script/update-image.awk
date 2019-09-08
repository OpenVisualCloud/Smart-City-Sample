#!/usr/bin/awk

BEGIN {
    im="";
    labels="node.labels."substr(labels,5,length(labels)-5);
    gsub(" "," node.labels.",labels);
    gsub(":","==",labels);
}

/image:/ {
    if (im!="") images[im]=1;
    im=$2;
}

/docker run/ {
    im=$NF;
    gsub(/\"/,"",im);
}

/node\..*==.*/ {
    if (index(labels" "role,$2)==0) im="";
}

END {
    if (im!="") images[im]=1;
    for (im in images)
        print(im);
}
