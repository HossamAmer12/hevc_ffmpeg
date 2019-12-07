n=1;
max=50;
set -- # this sets $@ [the argv array] to an empty list.

while [ "$n" -le "$max" ]; do
    # set -- "$@" "Seq-265-ffmpeg-noInLoop/$n" # this adds s$n to the end of $@
    #set -- "$@" "Seq-RECONS-ffmpeg-noInLoop/$n" # this adds s$n to the end of $@
    set -- "$@" "/media/h2amer/MULTICOM-104/103_HA/MULTICOM103/set_yuv/Seq-Stats-ffmpeg-noInLoop_168/$n" # this adds s$n to the end of $@
    
    n=$(( $n + 1 ));
done 

mkdir "$@"
