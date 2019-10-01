
i=$1
idx=$(printf "%08d\n" $i)
echo 'ID: ' ILSVRC2012_val_$idx
grep "" /media/h2amer/MULTICOM-104/Gen/Seq-Stats/ILSVRC2012_val_$idx*