INPUT_FILE="./test_file/ILSVRC2012_val_00001000_504_336_RGB.yuv"
OUTPUT_ENC_FILE="./test_file/1000_0.265"
OUTPUT_DEC_FILE="./test_file/1000_0.yuv"
QP=0
# ffmpeg -i $INPUT_FILE -c:v libx265 -crf 0 output.mp4

# ffmpeg -f rawvideo -vcodec rawvideo -s 504x336 -pix_fmt yuv420p -i $INPUT_FILE -c:v libx265 -crf $QP -preset medium -x265-params profile=main:level-idc=50:high-tier:vbv-bufsize=100000:vbv-maxrate=100000 $OUTPUT_DEC_FILE
ffmpeg -f rawvideo -vcodec rawvideo -s 504x336 -pix_fmt yuv420p -i $INPUT_FILE -c:v libx265 -crf $QP -preset medium $OUTPUT_DEC_FILE1
#ffmpeg -f rawvideo -vcodec rawvideo -s 504x336 -pix_fmt yuv420p -i $INPUT_FILE -c:v libx265 -crf $QP -preset ultrafast $OUTPUT_DEC_FILE2
ls -lah $OUTPUT_DEC_FILE

