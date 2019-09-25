#!/usr/bin/awk

BEGIN {
    im=im2="";
    ns_space=0;
    if (constraints==1 && dockercompose==1) {
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

/command:\s+\["-/ && dockercompose==1 {
    im2=im;
    n=split($NF,args,",");
    im=args[n];
    gsub(/[\"\]]/,"",im);
}

/- node\..*==.*/ && dockercompose==1 {
    if (constraints==1) {
        gsub(/[\" ]/,"",$2);
        if (index(labels" "role,$2)==0)
            im=im2="";
    }
}

/^\s*---\s*$/ {
    ns_space=0;
    saveim();
}

/:/ && ns_space>0 && kubernetes==1 {
    match($0, /^ */);
    if (RLENGTH > ns_space) {
        if (constraints==1) {
            gsub(/[\": ]/,"",$1);
            gsub(/[\": ]/,"",$2);
            print("checking "$1":"$2);
            if (index(labels,$1":"$2)==0)
                im=im2="";
        }
    } else {
       ns_space=0
    }
}

/nodeSelector:/ && kubernetes==1 {
    ns_space=index($0,"nodeSelector:");
}

END {
    saveim();
    for (im in images)
        print(im);
}
