import io
import librosa
import numpy as np
import streamlit as st
import audiomentations
from matplotlib import pyplot as plt
import librosa.display
from pages import utils



def create_pipeline(transformations: list):
    pipeline = []
    for index, transformation in enumerate(transformations):
        if transformation:
            pipeline.append(index_to_transformation(index))

    return pipeline

def plot_audio_transformations(y, sr, pipeline: audiomentations.Compose):
    cols = [1, 1, 1]

    col1, col2, col3 = st.beta_columns(cols)
    with col1:
        st.markdown(f"<h4 style='text-align: center; color: black;'>Original</h5>",
                    unsafe_allow_html=True)
        st.pyplot(utils.plot_transformation(y, sr, "Original"))
    with col2:
        st.markdown(f"<h4 style='text-align: center; color: black;'>Wave plot </h5>",
                    unsafe_allow_html=True)
        st.pyplot(utils.plot_wave(y, sr))
    with col3:
        st.markdown(f"<h4 style='text-align: center; color: black;'>Audio</h5>",
                    unsafe_allow_html=True)
        utils.spacing()
        st.audio(utils.create_audio_player(y, sr))
    st.markdown("---")

    y = y
    sr = sr
    for col_index, individual_transformation in enumerate(pipeline.transforms):
        transformation_name = str(type(individual_transformation)).split("'")[1].split(".")[-1]
        modified = individual_transformation(y, sr)
        fig = utils.plot_transformation(modified, sr, transformation_name=transformation_name)
        y = modified

        col1, col2, col3 = st.beta_columns(cols)

        with col1:
            st.markdown(f"<h4 style='text-align: center; color: black;'>{transformation_name}</h5>",
                        unsafe_allow_html=True)
            st.pyplot(fig)
        with col2:
            st.markdown(f"<h4 style='text-align: center; color: black;'>Wave plot </h5>",
                        unsafe_allow_html=True)
            st.pyplot(utils.plot_wave(modified, sr))
            utils.spacing()

        with col3:
            st.markdown(f"<h4 style='text-align: center; color: black;'>Audio</h5>",
                        unsafe_allow_html=True)
            utils.spacing()
            st.audio(utils.create_audio_player(modified, sr))
        st.markdown("---")
        plt.close("all")


def load_audio_sample(file):
    y, sr = librosa.load(file, sr=22050)

    return y, sr


def index_to_transformation(index: int):
    if index == 0:
        return audiomentations.AddGaussianNoise(p=1.0)
    elif index == 1:
        return audiomentations.AddGaussianSNR(p=1.0, min_snr_in_db=30, max_snr_in_db=90)
    elif index == 2:
        return audiomentations.FrequencyMask(p=1.0)
    elif index == 3:
        return audiomentations.TimeMask(p=1.0)
    elif index == 4:
        return audiomentations.TimeStretch(p=1.0)
    elif index == 5:
        return audiomentations.PitchShift(p=1.0)
    elif index == 6:
        return audiomentations.Shift(p=1.0)
    elif index == 7:
        return audiomentations.Normalize(p=1.0)
    elif index == 8:
        return audiomentations.PolarityInversion(p=1.0)
    elif index == 9:
        return audiomentations.Gain(p=1.0)
    elif index == 10:
        return audiomentations.AddBackgroundNoise(sounds_path="background_noise", p=1.0)
    elif index == 11:
        return audiomentations.AddShortNoises(sounds_path="background_noise", p=1.0)
    elif index == 12:
        return audiomentations.ClippingDistortion(max_percentile_threshold=10, p=1.0)
    elif index == 13:
        return audiomentations.Clip(p=1.0)
    elif index == 14:
        return audiomentations.HighPassFilter(p=1.0)
    elif index == 15:
        return audiomentations.LowPassFilter(p=1.0)
    elif index == 16:
        return audiomentations.BandPassFilter(p=1.0)
    elif index == 17:
        return audiomentations.Reverse(p=1.0)


def action(file_uploader, transformations):
    if file_uploader is not None:
        y, sr = utils.handle_uploaded_audio_file(file_uploader)


    pipeline = audiomentations.Compose(create_pipeline(transformations))
    plot_audio_transformations(y, sr, pipeline)


def main():
    placeholder = st.empty()
    placeholder2 = st.empty()
    placeholder.markdown(#"# Visualize an audio pipeline\n"
                        #  "# Audio Augmentation Visualization\n"
                         "### Select the components of the pipeline in the sidebar.\n"
                         "Once you have chosen augmentation techniques, select or upload an audio file\n. "
                         "Then click \"Apply\" to start!\n ")
    placeholder2.markdown(
        "After clicking start, the individual steps of the pipeline are visualized. The ouput of the previous step is the input to the next step.")
    placeholder.write("Create your audio pipeline by selecting augmentations in the sidebar.")
    st.sidebar.markdown("Choose the transformations here:")
    gaussian_noise = st.sidebar.checkbox("GaussianNoise")
    gaussian_noise_snr = st.sidebar.checkbox("GaussianNoise with random SNR")
    frequency_mask = st.sidebar.checkbox("FrequencyMask")
    time_mask = st.sidebar.checkbox("TimeMask")
    time_strech = st.sidebar.checkbox("TimeStretch")
    pitch_shift = st.sidebar.checkbox("PitchShift")
    shift = st.sidebar.checkbox("Shift")
    normalize = st.sidebar.checkbox("(Peak-)Normalize")
    polarity_inversion = st.sidebar.checkbox("PolarityInversion")
    gain = st.sidebar.checkbox("Gain")
    background_noise = st.sidebar.checkbox("AddBackgroundNoise", help="Adds a random background noise")
    add_short_noises = st.sidebar.checkbox("AddShortNoises", help="Mixes bursts of random sounds into the audio signal")
    clipping_distortion = st.sidebar.checkbox("ClippingDistortion")
    clip = st.sidebar.checkbox("Clip")
    highpass = st.sidebar.checkbox("HighPassFilter")
    lowpass = st.sidebar.checkbox("LowPassFilter")
    bandpass = st.sidebar.checkbox("BandPassFilter")
    reverse = st.sidebar.checkbox("Reverse")

    st.sidebar.markdown("---")
    st.sidebar.markdown("Upload an audio file here:")
    file_uploader = st.sidebar.file_uploader(label="", type=[".wav", ".wave", ".flac", ".mp3", ".ogg"])

    st.sidebar.markdown("---")
    if st.sidebar.button("Apply"):
        placeholder.empty()
        placeholder2.empty()
        transformations = [gaussian_noise, gaussian_noise_snr, frequency_mask, time_mask, time_strech, pitch_shift,
                           shift, normalize, polarity_inversion, gain, background_noise, add_short_noises,
                           clipping_distortion, clip, highpass, lowpass, bandpass, reverse]

        action(file_uploader=file_uploader,
               transformations=transformations)
