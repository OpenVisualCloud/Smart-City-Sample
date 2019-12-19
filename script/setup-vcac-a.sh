#!/bin/bash -e

# setup host docker swarm if not already
docker swarm leave --force 2> /dev/null
docker swarm init --advertise-addr=172.32.1.254 2> /dev/null || echo
JOINCMD=$(docker swarm join-token worker | grep token)

# setup VCAC-A passwordless access
echo "Login to VACA-A once to establish passwordless access"
if test ! -f ~/.ssh/id_rsa; then
    cat /dev/zero | ssh-keygen -q -N ""
    echo
fi
NODEUSER="root"
NODEPREFIX="172.32"
echo
# setup node to join the host docker swarm
sudo vcactl blockio list 2> /dev/null
for nodeip in $(sudo vcactl network ip |grep $NODEPREFIX 2>/dev/null); do
    ssh-copy-id $NODEUSER@${nodeip} 2> /dev/null || echo
    echo "Node: $nodeip"
    ssh $NODEUSER@${nodeip} "docker swarm leave --force 2> /dev/null;$JOINCMD"
done

# setup node labels for office1
for id in $(docker node ls -q 2> /dev/null); do
    nodeip="$(docker node inspect -f {{.Status.Addr}} $id)"
    if test -z "$(hostname -I | grep --fixed-strings $nodeip)"; then
        echo "label $id: vcac_zone=yes"
        docker node update --label-add vcac_zone=yes $id
    fi
done
