
import augment
from numpy.core.fromnumeric import squeeze
import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
import torch
import io
import librosa
import numpy as np
import streamlit as st
import audiomentations
import librosa.display
from scipy.io import wavfile
import wave
import pydub
from pages import utils

def plot_audio_transform_WavAugment(y, sr, pipeline_out, name_effects):
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
    for index, individual_transformation in enumerate(name_effects):
        transformation_name = (str(individual_transformation))
        modified = pipeline_out[index]
        fig = utils.plot_transformation((torch.squeeze(modified)).numpy(), sr, transformation_name=transformation_name)
        y = modified

        col1, col2, col3 = st.beta_columns(cols)

        with col1:
            st.markdown(f"<h4 style='text-align: center; color: black;'>{transformation_name}</h5>",
                        unsafe_allow_html=True)
            st.pyplot(fig)
        with col2:
            st.markdown(f"<h4 style='text-align: center; color: black;'>Wave plot </h5>",
                        unsafe_allow_html=True)
            st.pyplot(utils.plot_wave(torch.squeeze(modified).numpy(), sr))
            utils.spacing()

        with col3:
            st.markdown(f"<h4 style='text-align: center; color: black;'>Audio</h5>",
                        unsafe_allow_html=True)
            utils.spacing()
            st.audio(utils.create_audio_player(torch.squeeze(modified).numpy(), sr))
        st.markdown("---")
        plt.close("all")

# def load_audio_sample(file):
#     y, sr = librosa.load(file, sr=16000)
#     return y, sr


def create_pipeline(transformations: list):
    pipeline = []
    name_effects = []
    for index, transformation in enumerate(transformations):
        if transformation:
            pipeline.append(index_to_transformation(index)[0])
            name_effects.append(index_to_transformation(index)[1])

    return pipeline, name_effects
# banreject,pitch,reverb,time_drop,clip,contrast
def index_to_transformation(index: int):
    chain = augment.EffectChain()
    if index == 0:
        return chain.sinc('-a', '120', '500-100'), "Banreject"
    elif index == 1:
        random_pitch_shift = lambda: np.random.randint(-400, +400)
        return chain.pitch("-q", random_pitch_shift).rate(16000) , "Pitch"
    elif index == 2:
        return chain.reverb(50, 50, 50).channels(1), "Reverb"
    elif index == 3:
        return chain.time_dropout(max_seconds=0.3) , "Time_Drop"
    elif index == 4:
        return chain.clip(0.25) , "Clip"
    elif index == 5:
        return chain.contrast(), "Contrast"

   

def action(file_uploader, transformations):
    if file_uploader is not None:
        y, sr = utils.handle_uploaded_audio_file(file_uploader)
        # y = torch.Tensor(y)
    pipeline , name_effects = create_pipeline(transformations)
    pipeline_out = []
    for p in pipeline :
        p = p.apply(torch.Tensor(y),
                    src_info=dict(rate=16000),
                    target_info=dict(rate=16000,channel=1))
        pipeline_out.append(p)
    plot_audio_transform_WavAugment(y, sr, pipeline_out,name_effects)


def main():
    placeholder = st.empty()
    placeholder2 = st.empty()
    placeholder.markdown(
                         "### Select the components of the pipeline in the sidebar.\n"
                         "Once you have chosen augmentation techniques, select or upload an audio file\n. "
                         "Then click \"Apply\" to start!\n ")
    placeholder2.markdown(
        "After clicking start, the individual steps of the pipeline are visualized. The original audio is the input to all effects.")
    placeholder.write("Create your audio pipeline by selecting augmentations in the sidebar.")
    st.sidebar.markdown("Choose the transformations here:")
    banreject = st.sidebar.checkbox("banreject")
    pitch = st.sidebar.checkbox("pitch")
    reverb = st.sidebar.checkbox("reverb")
    time_drop = st.sidebar.checkbox("time_drop")
    clip = st.sidebar.checkbox("clip")
    contrast = st.sidebar.checkbox("contrast")

    st.sidebar.markdown("---")
    st.sidebar.markdown("Upload an audio file here:")
    file_uploader = st.sidebar.file_uploader(label="", type=[".wav", ".wave", ".flac", ".mp3", ".ogg"])

    st.sidebar.markdown("---")
    if st.sidebar.button("Apply"):
        placeholder.empty()
        placeholder2.empty()
        transformations = [banreject,pitch,reverb,time_drop,clip,contrast]
        action(file_uploader=file_uploader,
               transformations=transformations)