#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
digest_dir="$(pwd)/.digest"
ssh_dir="$(pwd)/.ssh"

digest () {
    docker inspect $1 2>/dev/null | grep Id | cut -f4 -d'"'
}

is_containerd () {
    major=($(kubectl version -o yaml 2>/dev/null | grep major: | cut -f2 -d'"'))
    minor=($(kubectl version -o yaml 2>/dev/null | grep minor: | cut -f2 -d'"'))
    if [ "${major[0]}" -gt 1 ] || [ "${minor[0]}" -ge 24 ]; then
        echo "1"
    fi
}

is_new () {
    [ "$(cat "$digest_dir"/${1/*\//} 2>/dev/null)" != "$2" ] && return 0 || return 1
}

save_digest () {
    echo "$1" > "$digest_dir"/${2/*\//}
}

remote_exec () {
    options=()
    while [[ "$1" = "-"* ]]; do
        options+=("$1")
        shift
    done

    ip=$1
    shift

    if [[ " $(hostname -I) " = *" $ip "* ]]; then
        "$@"
    else
        ssh "${options[@]}" -o ControlMaster=auto -o ControlPath="$ssh_dir"/'%r@%h-%p' -o ControlPersist=5m -o TCPKeepAlive=yes $ip "$@"
    fi
}

mkdir -p "$digest_dir" "$ssh_dir"
docker node ls > /dev/null 2> /dev/null && (
    echo "Updating docker-swarm nodes..."
    for id in $(docker node ls -q 2> /dev/null); do
        ready="$(docker node inspect -f {{.Status.State}} $id)"
        active="$(docker node inspect -f {{.Spec.Availability}} $id)"
        nodeip="$(docker node inspect -f {{.Status.Addr}} $id)"
        labels="$(docker node inspect -f {{.Spec.Labels}} $id | sed 's/map\[/node.labels./' | sed 's/\]$//' | sed 's/ / node.labels./g' | sed 's/:/==/g')"
        role="$(docker node inspect -f {{.Spec.Role}} $id)"

        if test "$ready" = "ready"; then
            if test "$active" = "active"; then
                # skip unavailable or manager node
                if [[ " $(hostname -I) " != *" $nodeip "* ]]; then
                    for image in $(awk -v labels="$labels node.role=${role}" -f "$DIR/scan-yaml.awk" "${DIR}/../deployment/docker-swarm/docker-compose.yml"); do
                        image_digest=$(digest $image)
                        if [ -n "$image_digest" ]; then
                            if is_new $image $image_digest; then
                                echo "$image..."
                                docker save $image | remote_exec $nodeip docker load
                            fi
                            save_digest $image_digest $image
                        fi
                    done
                fi
            fi
        fi
    done
) || echo -n ""

kubectl get node >/dev/null 2>/dev/null && (
    echo "Updating Kubernetes nodes..."
    containerd="$(is_containerd)"
    for id in $(kubectl get nodes $([ -n "$containerd" ] || echo "--selector='!node-role.kubernetes.io/master'") 2> /dev/null | grep ' Ready ' | cut -f1 -d' '); do
        nodeip="$(kubectl describe node $id | grep InternalIP | sed -E 's/[^0-9]+([0-9.]+)$/\1/')"
        labels="$(kubectl describe node $id | awk '/Annotations:/{lf=0}/Labels:/{sub("Labels:","",$0);lf=1}lf==1{sub("=",":",$1);print$1}')"

        for image in $(helm >/dev/null 2>/dev/null && (helm template smtc "$DIR/../deployment/kubernetes/smtc" | awk -v labels="$labels" -f "$DIR/scan-yaml.awk")); do
            image_digest=$(digest $image)
            if [ -n "$image_digest" ]; then
                if is_new $image $image_digest; then
                    echo "$image..."
                    docker save $image | (
                        if [ -n "$containerd" ]; then
                            remote_exec -t $nodeip sudo ctr -n k8s.io i import -
                        else
                            remote_exec $nodeip docker load
                        fi
                    )
                    save_digest $image_digest $image
                fi
            fi
        done
    done
) || echo -n ""
