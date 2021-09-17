#!/bin/bash 

for folder in ~/get-data-TTS/data/*/;
do 
    # python3 main.py -input "$file" \
    #                 -output "/home/trinhtuanvu/get-data-TTS/augment-data/" \
    #                 wavaugment \
    #                 --chain "time_drop"
    python3 main.py -input "$folder" \
                    -output "/home/trinhtuanvu/get-data-TTS/augment-data/" \
                    audiomentations \
                    --compose "TimeMask"
# (PitchShift,AddGaussianSNR),(Shift,Gain),(Clip,FrequencyMask),(TimeMask)
    echo "COMPLETE"

done 

