#!/bin/bash 

for folder in ~/get-data-TTS/data-trash/*/;
do 
    # python3 main.py -input "$file" \
    #                 -output "out2/" \
    #                 wavaugment \
    #                 --chain "clip,pitch"
    python3 main.py -input "$folder" \
                    -output "/home/trinhtuanvu/get-data-TTS/augment-data/" \
                    audiomentations \
                    --compose "PitchShift,AddGaussianSNR"

    echo "COMPLETE"
    
done 

