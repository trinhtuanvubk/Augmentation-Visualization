import numpy as np
import augment
import torch

#  Some functions to help effects 
def RandomPitchShift(shift_max = 300):
    return np.random.randint(-shift_max,shift_max)

def RandomClipFactor(factor_min=0.0, factor_max=1.0):
    return np.random.triangular(factor_min, factor_max, factor_max)

def RandomReverb():
    reverberance_min: int = 50
    reverberance_max: int = 50
    damping_min: int = 50
    damping_max: int = 50
    room_scale_min: int = 0
    room_scale_max: int = 100
    reverberance = np.random.randint(reverberance_min, reverberance_max + 1)
    damping = np.random.randint(damping_min,damping_max + 1)
    room_scale = np.random.randint(room_scale_min, room_scale_max + 1)
    return [reverberance, damping, room_scale]

def SpecAugmentBand(sample_rate, scaler):
    def freq2mel(f):
        return 2595. * np.log10(1 + f / 700)
    def mel2freq(m):
        return ((10.**(m / 2595.) - 1) * 700)
    F = 27.0 * scaler
    melfmax = freq2mel(sample_rate / 2)
    meldf = np.random.uniform(0, melfmax * F / 256.)
    melf0 = np.random.uniform(0, melfmax - meldf)
    low = mel2freq(melf0)
    high = mel2freq(melf0 + meldf)
    return f'{high}-{low}'
def Noise_Generator(x):
    return torch.zeros_like(x).uniform_()

def aug_factory(description, sample_rate, args):
    chain = augment.EffectChain()
    description = description.split(',')

    for effect in description:
        if effect == 'bandreject':
            chain = chain.sinc('-a', '120', SpecAugmentBand(sample_rate, args.band_scaler))
        elif effect == 'pitch':
            pitch_randomizer = RandomPitchShift(args.pitch_shift_max)
            if args.pitch_quick:
                chain = chain.pitch('-q', pitch_randomizer).rate('-q', sample_rate)
            else:
                chain = chain.pitch(pitch_randomizer).rate(sample_rate)
        elif effect == 'reverb':
            randomized_params = RandomReverb(args.reverberance_min, args.reverberance_max, 
                                args.damping_min, args.damping_max, args.room_scale_min, args.room_scale_max)
            chain = chain.reverb(randomized_params).channels()
        elif effect == 'time_drop':
            chain = chain.time_dropout(max_seconds=args.t_ms / 1000.0)
        elif effect == 'clip':
            chain = chain.clip(RandomClipFactor(args.clip_min, args.clip_max))
    # use additive_noise if you have noise data
        # elif effect == 'additive_noise': 
        #     noise = Noise_Generator(x= data)
        #     chain = chain.additive_noise(noise_generator,snr=args.snr_additive_noise)
        elif effect == 'contrast':
            chain = chain.contrast()
        elif effect == 'none':
            pass
        else:
            raise RuntimeError(f'Unknown augmentation type {effect}')
    return chain