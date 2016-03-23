#!/bin/bash
resource=$1
operation=$2

# Unmanage the resource
pcs resource unmanage $resource

# Setting variables for the parameters
#eval $(pcs resource show $resource|
#	grep Attributes:|
#	awk '{$1=""; print}'|
#	tr " " "\n"|
#	grep .|
#	xargs -0I X echo export OCF_RESKEY_X|
#	sed 's/=\(.*\)/="\1"/')

params=$(./params.py $resource)

IFS=$'\n'
for v in $params; do 
    #echo $v
    export "${v}"
done 

export OCF_RESOURCE_INSTANCE=${resource}
# OCF_ROOT is needed and might be OS dependent
export OCF_ROOT=/usr/lib/ocf

#set 
# Run the RA now that we have the right environment
bash -x /usr/lib/ocf/resource.d/$(pcs resource show $resource|
    sed -n 1p|
    sed 's@.*provider=\(.*\) type=\(.*\))@\1/\2@') $operation
