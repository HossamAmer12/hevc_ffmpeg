
i=$1
idx=$(printf "%08d\n" $i)
echo 'ID: ' ILSVRC2012_val_$idx
grep "" /media/h2amer/MULTICOM-104/validation_generated_QF_TXT_5/shard-0/3/ILSVRC2012_val_$idx*