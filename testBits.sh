
# Test1:
# INPUT_FILE="./test_file/ILSVRC2012_val_00001000_504_336_RGB.yuv"
# OUTPUT_ENC_FILE="./test_file/1000_0.265"
# OUTPUT_DEC_FILE="./test_file/1000_0.yuv"
# QP=0

#Test2:
INPUT_FILE="/media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/pics/1/ILSVRC2012_val_00001000_504_336_RGB.yuv"
OUTPUT_ENC_FILE="/media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg/1/ILSVRC2012_val_00001000_504_336_RGB_0.265"
OUTPUT_DEC_FILE="/media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/Seq-Recons-ffmpeg/1/ILSVRC2012_val_00001000_504_336_RGB_0.yuv"
QP=0



# ffmpeg -i $INPUT_FILE -c:v libx265 -crf 0 output.mp4

# 265
# ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 504x336  -i $INPUT_FILE -c:v hevc -crf $QP -f hevc -preset ultrafast $OUTPUT_ENC_FILE

# Final 265
ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 504x336  -i $INPUT_FILE -c:v hevc -crf $QP -f hevc -preset ultrafast $OUTPUT_ENC_FILE
echo "ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 504x336  -i $INPUT_FILE -c:v hevc -crf $QP -f hevc -preset ultrafast $OUTPUT_ENC_FILE"


# ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 504x336-i /media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/pics/1/ILSVRC2012_val_00001000_504_336_RGB.yuv -c:v hevc -crf 0 -f hevc -preset ultrafast /media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg/1/ILSVRC2012_val_00001000_504_336_RGB_0.265
# yuv
# ffmpeg -f rawvideo -vcodec rawvideo -s 504x336 -pix_fmt yuv420p -i $INPUT_FILE -c:v libx265 -crf $QP -preset ultrafast $OUTPUT_DEC_FILE

# Final yuv
#ffmpeg -f rawvideo -vcodec rawvideo -s 504x336 -pix_fmt yuv420p -i $INPUT_FILE -c:v hevc -crf $QP -preset ultrafast $OUTPUT_DEC_FILE

./calc_frame_size.sh $OUTPUT_DEC_FILE

./hevcesbrowser_console_linux -i $OUTPUT_ENC_FILE
# frame_size=$(grep '^0x*' go.txt) # lines start with
# echo $frame_size
# rm go.txt


FILESIZE=$(stat -c%s "$OUTPUT_ENC_FILE")
echo "Total size of $OUTPUT_ENC_FILE = $FILESIZE bytes."


# ffmpeg -f rawvideo -vcodec rawvideo -s 504x336 -pix_fmt yuv420p -i $INPUT_FILE -c:v libx265 -crf $QP -preset medium -x265-params profile=main:level-idc=50:high-tier:vbv-bufsize=100000:vbv-maxrate=100000 $OUTPUT_DEC_FILE
#ffmpeg -f rawvideo -vcodec rawvideo -s 504x336 -pix_fmt yuv420p -i $INPUT_FILE -c:v libx265 -crf $QP -preset medium $OUTPUT_DEC_FILE1
#ffmpeg -f rawvideo -vcodec rawvideo -s 504x336 -pix_fmt yuv420p -i $INPUT_FILE -c:v libx265 -crf $QP -preset ultrafast $OUTPUT_DEC_FILE2

