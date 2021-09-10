from audiomentations import (Compose, 
    AddBackgroundNoise, 
    AddGaussianNoise, 
    AddGaussianSNR,
    AddImpulseResponse, 
    ApplyImpulseResponse,
    AddShortNoises, 
    BandPassFilter,
    Clip,
    ClippingDistortion,
    FrequencyMask,
    Gain,
    HighPassFilter,
    LoudnessNormalization,
    LowPassFilter,
    Mp3Compression,
    Normalize,
    PitchShift,
    PolarityInversion,
    Resample,
    Reverse,
    Shift,
    TimeMask,
    TimeStretch,
    Trim)

SAMPLE_RATE = 16000

def aug_factory(description, args):
    description = description.split(',')
    transformations = []
    for effect in description:
        if effect == 'AddGaussianNoise':
            transformations.append(AddGaussianNoise(p=1.0))
        elif effect == 'AddGaussianSNR':
            transformations.append(AddGaussianSNR(p=1.0, min_snr_in_db=30, max_snr_in_db=90))
        elif effect == 'FrequencyMask':
            transformations.append(FrequencyMask(p=1.0))
        elif effect == 'TimeMask':
            transformations.append(TimeMask(p=1.0))
        elif effect == 'TimeStretch' :
            transformations.append(TimeStretch(p=1.0))
        elif effect == 'PitchShift':
            transformations.append(PitchShift(p=1.0))
        elif effect == 'Shift':
            transformations.append(Shift(p=1.0))
        elif effect == 'Normalize':
            transformations.append(Normalize(p=1.0))
        elif effect == 'PolarityInversion':
            transformations.append(PolarityInversion(p=1.0))
        elif effect == 'Gain':
            transformations.append(Gain(p=1.0))
        elif effect == 'AddBackgroundNoise':
            transformations.append(AddBackgroundNoise(sounds_path=args.background_noise, p=1.0))
        elif effect == 'AddShortNoise':
            transformations.append(AddShortNoises(sounds_path=args.background_noise, p=1.0))
        elif effect == 'ClippingDistortion':
            transformations.append(ClippingDistortion(max_percentile_threshold=10, p=1.0))
        elif effect == 'Clip':
            transformations.append(Clip(p=1.0))
        elif effect == 'HighPassFilter':
            transformations.append(HighPassFilter(p=1.0))
        elif effect == 'LowpassFilter':
            transformations.append(LowPassFilter(p=1.0))
        elif effect == 'BandPassFilter':
            transformations.append(BandPassFilter(p=1.0))
        elif effect == 'Reverse':
            transformations.append(Reverse(p=1.0))
        elif effect == 'none':
            pass
        else:
            raise RuntimeError(f'Unknown augmentation type {effect}')
    augment = Compose(transformations)
    return augment
