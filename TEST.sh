 

 # ffmpeg -y -f rawvideo -pix_fmt yuv420p -s:v 504x384 -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/test/1/ILSVRC2012_val_00000651_504_384_RGB.yuv -c:v hevc -crf 51 -f hevc -preset ultrafast -x265-params no-deblock no-sao  /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265
 # ffmpeg -y -f rawvideo -pix_fmt yuv420p -s:v 504x384 -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/test/1/ILSVRC2012_val_00000651_504_384_RGB.yuv -c:v hevc -crf 51 -f hevc -x265-params no-deblock /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265


echo '(((((((((((((((((((((((((((((((((('
du -h /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265
# ffmpeg -y -f rawvideo -pix_fmt yuv420p -s:v 504x384 -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/test/1/ILSVRC2012_val_00000651_504_384_RGB.yuv -c:v hevc -crf 51 -f hevc -preset ultrafast /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265


#ffmpeg -y -f rawvideo -pix_fmt yuv420p -s:v 504x384 -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/test/1/ILSVRC2012_val_00000651_504_384_RGB.yuv -c:v libx265 -crf 51 -f hevc  -preset ultrafast /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265

ffmpeg -y -f rawvideo -pix_fmt yuv420p -s:v 504x384 -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/test/1/ILSVRC2012_val_00000651_504_384_RGB.yuv -c:v libx265 -crf 51 -f hevc  -preset ultrafast -x265-params no-deblock=1:no-sao=1:ctu=16:min-cu-size=16:max-tu-size16 /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265

#ffmpeg -y -f rawvideo -pix_fmt yuv420p -s:v 504x384 -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/test/1/ILSVRC2012_val_00000651_504_384_RGB.yuv -c:v hevc -crf 51 -f hevc -preset ultrafast -x265-params no-deblock=1  /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265
du -h /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265
echo '))))))))))))))))))))))))))))))))))))'

ffmpeg  -y  -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265 -s 504x384 -c:v rawvideo -pix_fmt yuv420p /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-RECONS-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.yuv

cp /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-RECONS-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.yuv ~/Desktop/

