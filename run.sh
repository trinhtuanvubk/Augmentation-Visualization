#!/bin/bash 

for folder in ~/get-data-TTS/data/*/;
do 
    # python3 main.py -input "$folder" \
    #                 -output "your output folder" \
    #                 wavaugment \
    #                 --chain "time_drop"
    python3 main.py -input "$folder" \
                    -output "your output folder" \
                    audiomentations \
                    --compose "TimeMask"
# (PitchShift,AddGaussianSNR),(Shift,Gain),(Clip,FrequencyMask),(TimeMask)
    echo "COMPLETE"

done 

