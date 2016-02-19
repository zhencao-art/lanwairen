#!/bin/bash

DEVICES="/sys/devices"
LOCAL_CPU="local_cpus"
LOCAL_CPULIST="local_cpulist"
MSI_IRQS="msi_irqs"
AFFINITY_OP="set"
RQ_AFFINITY=2
VERBOSE=1

function echo_n()
{
    case $1 in
        info|INFO)
            if [ $VERBOSE != 0 ]; then
                echo "[INFO] $2"
            fi
        ;;
        warn|WARN)
            echo "[WARN] $2"
        ;;
        error|ERROR)
            echo "[ERROR] $2"
            exit 1
        ;;
        *)
            echo "[$1] $2"
        ;;
    esac
}

function add_comma_every_eight()
{
    echo " $1 " | sed -r ':L;s=\b([0-9]+)([0-9]{8})\b=\1,\2=g;t L'
}

function int2hex()
{
    CHUNKS=$(( $1/64 ))
    COREID=$1
    HEX=""
    for (( CHUNK=0; CHUNK<${CHUNKS} ; CHUNK++ ))
    do
        HEX=$HEX"0000000000000000"
        COREID=$((COREID-64))
    done
    printf "%x$HEX" $(echo $((2**$COREID)) )
}


function core_to_affinity()
{
    echo $( add_comma_every_eight $( int2hex $1) )
}

function get_block_device_list()
{
    local pci_addr=$1
    local link=""
    local block_list=""
    for item in /sys/block/*
    do
        link=`readlink $item`
        if [ "${link#*$pci_addr/host*}" != "$link" ]; then
            if [ "$block_list"x == ""x ]; then
                block_list=$item
            else
                block_list="$block_list $item"
            fi
        fi
    done
    echo $block_list
} 

function rq_affinity_set()
{
    local pci=$1
    local rq_affinity=$2
    local block_list=`get_block_device_list $pci`
    local block=""

    for block in $block_list
    do
        echo $rq_affinity > $block/queue/rq_affinity
    done

}

function affinity_set()
{
    local I=1
    local core_id=0
    local affinity=0
    local cores=$3
    for IRQ in $1
    do
        core_id=$(echo $2 | cut -d "," -f $I)
        echo Assign irq $IRQ core_id $core_id
        affinity=$( core_to_affinity $core_id )
        echo $affinity > /proc/irq/$IRQ/smp_affinity
        I=$(( (I%cores) + 1 ))
    done

    rq_affinity_set $PCI_ADDR $RQ_AFFINITY
}

function affinity_restore()
{
    local affinity=$2
    for IRQ in $1
    do
        echo Restore irq $IRQ cpu mask $affinity
        echo $affinity > /proc/irq/$IRQ/smp_affinity
    done
}

function affinity_status()
{
    local cpu_mask=$2
    local affinity=0
    local affinity_set=0
    local affinity_restore=0
    for IRQ in $1
    do
        affinity=`cat /proc/irq/$IRQ/smp_affinity`
        if [ $affinity == $cpu_mask ]; then
            let affinity_restore=$affinity_restore+1
        else
            let affinity_set=$affinity_set+1
        fi
    done

    if [ $affinity_restore == 0 ]; then
        echo_n "info" "MPT2SAS has set CPU Affinity"
        return 0
    elif [ $affinity_set == 0 ]; then
        echo_n "info" "MPT2SAS has not set CPU Affinity"
        return 1
    else
        echo_n "info" "MPT2SAS has partially set CPU Affinity"
        return 2
    fi
}

case "$1" in
    set)
        AFFINITY_OP="set"
        PCI_ADDR=$2
        ;;
    restore)
        AFFINITY_OP="restore"
        PCI_ADDR=$2
        ;;
    status)
        AFFINITY_OP="status"
        PCI_ADDR=$2
        ;;
    *)
        echo "Usage: $0 {set|restore|status} <PCI_ADDRESS>"
        exit 2
        ;;
esac


MPT2SAS_DEVICE=`find $DEVICES -name $PCI_ADDR`
if [ $? != 0 ]; then
    echo_n "error" "can not find PCI device at address $PCI_ADDR"
fi

MPT2SAS_DRIVER=`readlink $MPT2SAS_DEVICE/driver | awk -F"/" '{ print $NF}'`
if [ $? != 0 ]; then
    echo_n "error" "can not get MPT2SAS driver at $MPT2SAS_DEVICE/driver"
fi
if [ "$MPT2SAS_DRIVER"x != "mpt2sas"x ]; then
    echo_n "error" "Device driver is not mpt2sas at $MPT2SAS_DEVICE/driver"
fi

if [ -f $MPT2SAS_DEVICE/$LOCAL_CPU ]; then
    CPU_MASK=`cat $MPT2SAS_DEVICE/$LOCAL_CPU`
else
    echo_n "error" "$MPT2SAS_DEVICE/$LOCAL_CPU does not exist"
fi

if [ -d $MPT2SAS_DEVICE/$MSI_IRQS ]; then
    IRQS=`ls $MPT2SAS_DEVICE/$MSI_IRQS | sort -n`
else
    echo_n "error" "$MPT2SAS_DEVICE/$MSI_IRQS does not exist or is not a directory"
fi
if [ "$IRQS"x == ""x ]; then
    echo_n "error" "There is no irq under $MPT2SAS_DEVICE/$MSI_IRQS"
fi

if [ -f $MPT2SAS_DEVICE/$LOCAL_CPULIST ]; then
    CPULIST=`cat $MPT2SAS_DEVICE/$LOCAL_CPULIST`
else
    echo_n "error" "$MPT2SAS_DEVICE/$LOCAL_CPULIST does not exist"
fi
CORES=$( echo $CPULIST | sed 's/,/ /g' | wc -w )
for word in $(seq 1 $CORES)
do
    SEQ=$(echo $CPULIST | cut -d "," -f $word | sed 's/-/ /')
    if [ "$(echo $SEQ | wc -w)" != "1" ]; then
        CPUS="$CPUS $( echo $(seq $SEQ) | sed 's/ /,/g' )"
    fi
done
if [ "$CPUS" != "" ]; then
    CPULIST=$(echo $CPUS | sed 's/ /,/g')
fi
CORES=$( echo $CPULIST | sed 's/,/ /g' | wc -w )

rc=0
case $AFFINITY_OP in
    set)
        affinity_set "$IRQS" "$CPULIST" "$CORES"
        ;;
    restore)
        affinity_restore "$IRQS" "$CPU_MASK"
        ;;
    status)
        affinity_status "$IRQS" "$CPU_MASK"
        rc=$?
        if [ $rc == 0 ]; then
            rc=0
        elif [ $rc == 1 ]; then
            rc=10
        else
            rc=20
        fi
        ;;
    *)
        rc=3
        ;;
esac

exit $rc
