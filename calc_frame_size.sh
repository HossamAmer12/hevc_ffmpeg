f="./test_file/ILSVRC2012_val_00001000_504_336_RGB_0_1.265"

# frame_size=$(ffprobe -show_frames $f | grep pkt_size=)
# frame_size=$(echo $frame_size | tr -cd [:digit:])
# echo 'frame_size:' $frame_size

#frame_size=$(./hevcesbrowser_console -i $f)
./hevcesbrowser_console_linux -i $f >> go.txt
frame_size=$(grep '^0x*' go.txt) # lines start with
echo $frame_size
rm go.txt

