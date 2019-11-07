#!/bin/bash

scheme="$1"
case "$scheme" in
traffic)
    x0=-122.97570389153029
    x1=-122.95002310846972
    y0=45.55110181605918
    y1=45.5331153839408
    ;;
stadium)
    x0=-121.98610951561652
    x1=-121.94083448438347
    y0=37.406071432118374
    y1=37.37009856788163
    ;;
*)
    echo "Usage: <scheme [x0 x1 y0 y1]> <IMAGE> [DIR]"
    exit 3
    ;;
esac

if test -n "$6"; then
    x0="$2"; shift
    x1="$2"; shift
    y0="$2"; shift
    y1="$2"; shift
fi

image="$2"
if test "$image" != "${image/ /_}"; then
    echo "image name cannot contain whitespace"
    exit 3
fi

echo "Image: $image"
image_dir=$(dirname $(readlink -f "$image"))
image=$(basename $(readlink -f "$image"))

GDAL2="geographica/gdal2"
cwd=$(readlink -f "$3")
if test -z "$cwd"; then
    cwd="$(pwd)"
fi
echo "working dir: $cwd"

user="$(id -u):$(id -g)"
info=$(docker run -v "$image_dir:/home:ro" -v "$cwd:/mnt" --rm -u $user -it $GDAL2 sh -c "gdalinfo /home/${image}" | grep "Size is")
width=$(echo "$info" | sed -E 's/^[^0-9]*([0-9]+).*$/\1/')
height=$(echo "$info" | sed -E 's/^.*, ([0-9]+).*$/\1/')
echo "Image size: :${width}x${height}:"
if test "$width" -ne "$height"; then
    echo "Not a square image."
    exit 3
fi

docker run --rm -u $user -v "$image_dir:/home:ro" -v "$cwd:/mnt" --rm -it $GDAL2 gdal_translate -of GTiff -gcp 0 0 $x0 $y0 -gcp 0 $height $x0 $y1 -gcp $width $height $x1 $y1 -gcp $width 0 $x1 $y0 "/home/${image}" "/mnt/${image}.tmp.tif"
rm -f "$cwd/${image}.modified.tif"
docker run --rm -u $user -v "$cwd:/home" --rm -it $GDAL2 gdalwarp -r cubic -tps -co COMPRESS=LZW  "/home/${image}.tmp.tif" "/home/${image}.modified.tif"
rm -f "$cwd/${image}.tmp.tif"
rm -rf "$cwd/${scheme}"
mkdir -p "$cwd/${scheme}"
docker run --rm -u $user -v "$cwd:/home" --rm -it $GDAL2 gdal2tiles.py -p mercator -z 13-18 -s EPSG:4326 -d -n -w none -r cubic /home/${image}.modified.tif /home/${scheme}
find "$cwd/${scheme}" -name "*.xml" -exec rm -f {} \;
