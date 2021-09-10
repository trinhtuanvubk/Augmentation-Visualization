# **Voice-Augmentations**
# **Setup**
## - Create a new enviroment to avoid error
## - To install [audiomentations](https://github.com/iver56/audiomentations) : 
* `pip install audiomentations` 
## - To install [WavAugment](https://github.com/facebookresearch/WavAugment) :
* `git clone git@github.com:facebookresearch/WavAugment.git`
* `cd WavAugment`
* `python3 setup.py develop`
## - Notes 
* if you get wrong with  `python3 setup.py develop` , try `python setup.py develop` or `sudo python3 setup.py develop` 
* if you get wrong with `sox` when using WavAugment, try `sudo apt install sox`
# **Usage**

## - Audiomentations : 
```zsh       
         python3 main.py -input "InputFolder/" \
                         -output "OutputFolder/" \
                         audiomentations \
                         --compose "ListOfEffects"
```
* List of effects :  AddBackgroundNoise, AddGaussianNoise, AddGaussianSNR, AddShortNoises,BandPassFilter, Clip, ClippingDistortion, FrequencyMask, Gain, HighPassFilter, LowPassFilter,
Normalize, PitchShift, PolarityInversion, Reverse, Shift, TimeMask, TimeStretch
* Example : --compose "AddGaussianSNR,PitchShift"
## - WavAugment : 
```zsh
        python3 main.py --input "InputFolder/" \
                         -output "OutputFolder/" \
                         wavaugment \
                         --chain "ListOfEffects"
```
* List of effects : bandreject, pitch, reverb, time_drop, clip, contrast, ...
* Example : --chain "pitch,clip"
# **Visualization**
## - To visualize transformations at local,  : 
* `cd visualization`
* `streamlit run app.py`
                         
