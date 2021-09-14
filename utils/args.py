import argparse

def main_args():
    parser = argparse.ArgumentParser() 
    parser.add_argument('-input', type=str, help='File to procecss',default='input/')
    parser.add_argument('-output', type=str, help='Output file',default='output/')  
    subparser = parser.add_subparsers(dest='library')
    audiomentations = subparser.add_parser('audiomentations')
    wavaugment = subparser.add_parser('wavaugment') 

    # parameters of audiomentations
    audiomentations.add_argument('--compose', type=str, help='Comma-separated list of effects to apply, e.g. "pitch,dropout"',
        default='AddGaussianNoise')
    audiomentations.add_argument('--min_snr_in_db', type=int, help='', default=50)
    audiomentations.add_argument('--max_snr_in_db', type=int, help='', default=90)
    audiomentations.add_argument('--background_noise',type =str, help='Folder path of noise', default='none')
    
    # parameters of wavaugment
    wavaugment.add_argument('--chain', type=str, help='Comma-separated list of effects to apply, e.g. "pitch,dropout"',
        default='pitch')
    wavaugment.add_argument('--t_ms', type=int, help='Size of a time dropout sequence', default=50)
    wavaugment.add_argument('--pitch_shift_max', type=int, help='Amplitude of a pitch shift; measured in 1/100th of a tone', default=300)
    wavaugment.add_argument('--pitch_quick', action='store_true', help='Speech up the pitch effect at some quality cost')
    wavaugment.add_argument('--room_scale_min', type=int, help='Minimal room size used in randomized reverb (0..100)', default=0)
    wavaugment.add_argument('--room_scale_max', type=int, help='Maximal room size used in randomized reverb (0..100)', default=100)
    wavaugment.add_argument('--reverberance_min', type=int, help='Minimal reverberance used in randomized reverb (0..100)', default=50)
    wavaugment.add_argument('--reverberance_max', type=int, help='Maximal reverberance used in randomized reverb (0..100)', default=50)
    wavaugment.add_argument('--damping_min', type=int, help='Minimal damping used in randomized reverb (0..100)', default=50)
    wavaugment.add_argument('--damping_max', type=int, help='Maximal damping used in randomized reverb (0..100)', default=50)
    wavaugment.add_argument('--clip_min', type=float, help='Minimal clip factor (0.0..1.0)', default=0.5)
    wavaugment.add_argument('--clip_max', type=float, help='Maximal clip factor (0.0..1.0)', default=1.0)
    wavaugment.add_argument('--snr_additive_noise',type=int, help='snr',default=15)
  
    args = parser.parse_args()
    if args.library == wavaugment : 
        args.chain = args.chain.lower()

#  Raise Error for WavAugment
        if not (0 <= args.room_scale_min <= args.room_scale_max <= 100):
            raise RuntimeError('It should be that 0 <= room_scale_min <= room_scale_max <= 100')

        if not (0 <= args.reverberance_min <= args.reverberance_max <= 100):
            raise RuntimeError('It should be that 0 <= reverberance_min <= reverberance_max <= 100')

        if not (0 <= args.damping_min <= args.damping_max <= 100):
            raise RuntimeError('It should be that 0 <= damping_min <= damping_max <= 100')

        if not (0.0 <= args.clip_min <= args.clip_max <= 1.0):
            raise RuntimeError('It should be that 0 <= clip_min <= clip_max <= 1.0')

        if args.library == 'none':
            raise RuntimeError('You need to choose the library')

    return args



