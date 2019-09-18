
# Number of Parallel tasks (make sure that they are multiples of 11 since we are running 11 QF per image)
num_parallel_tasks=10

img_delta_start=$num_parallel_tasks
img_start=1

# for (( folder = 1; folder < 2; folder++ ))
for (( folder = 26; folder < 51; folder++ ))
do


# Define the input path to files
input_path_to_files=/media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/Seq-RECONS-ffmpeg/$folder



# Generate the list of commands:
echo 'Generating Commands list and running batches of images'

# count the total number of commands
commands_count=0


# parallel group id
for (( group_id = 0; group_id < 10; group_id++ ))
do
  # create the start and end indices
 
  a=$((1000*($folder - 1)))
  b=$((100*($group_id) + 1))
  img_start=$((a+b))
  echo $a
  echo $b
  img_end=$((img_start+99))


  # creat the cmd:
  cmd="/usr/bin/python3.6 inference_classes_optimized.py  $img_start $img_end"
  cmd_array+=("$cmd")
  let "commands_count+=1"

done

# Execution part

# you need to make sure tha tyour start is 0
# you need to make sure that your end is always limited by the number of parallel tasks
# once you execute the commands, you clear up the cmd lists

# start of the commands list is always zero
start=0

# end cannot exceed the length of the YUV array
end=$num_parallel_tasks

  # Run in parallel
  while [  $start -lt $end ]; do {
    cmd="${cmd_array[start]}"
    echo "BLA BLA"
    echo "Process \"$start\" \"$cmd\" started";
    $cmd & pid=$!
    PID_LIST+=" $pid";
    start=$(($start + 1))
  } done

  trap "kill $PID_LIST" SIGINT
  echo "Parallel processes have started";
  wait $PID_LIST
  echo -e "\nAll processes have completed";


  # shift your commands array to the left for the tasks you already ran
  cmd_array=("${cmd_array[@]:$num_parallel_tasks}")

  # shift your PID list (clear it)
  #PID_LIST=("${PID_LIST[@]:$num_parallel_tasks}")
  PID_LIST=("${PID_LIST[@]:1}") # group by group

  echo "PID LIST Length: " ${#PID_LIST[@]}
  echo ${PID_LIST[0]} 


let "count_helper=$jpeg_files_count-1"


# Clear everything
# unset $PID_LIST
# unset $cmd_array

done # folder loop
#******#******#******#******#******#******#******#******#******#*****