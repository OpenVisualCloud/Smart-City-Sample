#!/bin/bash

if test -z "$1"; then
    x0=-122.899823
    x1=-123.028397
    y0=45.521266
    y1=45.578520
else
    x0="$1"
    x1="$2"
    y0="$3"
    y1="$4"
fi

echo "$x0 $x1 $y0 $y1" | awk '
function min(x,y) { return x>y?y:x; }
function max(x,y) { return x>y?x:y; }
function pi() { return 3.14159265437; }
function R() { return 6378137; }
function ss() { return 0.5/(pi()*R()); }
function tiled(x) { return int(x/256); }
function project_x(lng,z) {
    d=pi()/180;
    px=R()*lng*d;
    s=256*(2**z);
    return tiled(s*(ss()*px+0.5));
}
function project_y(lat,z) {
    d=pi()/180;
    m=1 - 1.0e-15;
    ls=max(min(sin(lat*d),m),-m);
    s=256*(2**z);
    py=R()*log((1+ls)/(1-ls))/2;
    return tiled(s*(-ss()*py+0.5));
}
function xyz(lat0, lat1, lng0, lng1, zmin, zmax) {
    for (z=zmin;z<=zmax;z++) {
        x0=project_x(lng0,z);
        x1=project_x(lng1,z);
        y0=project_y(lat0,z);
        y1=project_y(lat1,z);
        for (x=min(x0,x1);x<=max(x0,x1);x++) {
            for (y=min(y0,y1);y<=max(y0,y1);y++) {
                system("mkdir -p "z"/"x);
                system("wget -O "z"/"x"/"y".png http://localhost:8080/tile/"z"/"x"/"y".png");
            }
        }
    }
}
{ xyz($3,$4,$1,$2,13,18); }
'
