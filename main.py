import os
from utils import main_args 

import torchaudio
import WavAugment_lib

import librosa
import audiomentations_lib
import soundfile
from audiomentations.core.utils import convert_float_samples_to_int16

if __name__ == '__main__':
    args = main_args()
    SAMPLE_RATE = 16000

    if args.library == "wavaugment" : 
        for file in os.listdir(args.input):
            path = os.path.join(args.input,file)
            data, sampling_rate = torchaudio.load(path)
            augment = WavAugment_lib.aug_factory(args.chain, sample_rate=SAMPLE_RATE,args=args)

            y = augment.apply(data, 
                    src_info=dict(rate=sampling_rate, length=data.size(1), channels=data.size(0)),
                    target_info=dict(rate=sampling_rate, length=0))
            torchaudio.save("{}/wavaugment_{}.wav".format(args.output,file[:-4]), y, SAMPLE_RATE)

    if args.library == "audiomentations" : 
        for file in os.listdir(args.input):
            path = os.path.join(args.input,file)
            data,sr = librosa.load(path,sr= SAMPLE_RATE)
            augment = audiomentations_lib.aug_factory(args.compose, args)
            y = augment(samples=data, sample_rate=SAMPLE_RATE)
            y = convert_float_samples_to_int16(y)
            soundfile.write("{}/audiomentations_{}.wav".format(args.output,file[:-4]), y, samplerate=SAMPLE_RATE)
