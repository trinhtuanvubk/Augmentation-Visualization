from logging import debug

import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports 
from multipages import MultiPage
from pages import audiometations_pages,wavaugment # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
display = Image.open('figures/ftech.png')
display = np.array(display)
st.image(display, width = 400)
st.title("Voice - Augmentation")
# col1, col2 = st.beta_columns(2)
# col1.image(display, width = 400)
# col2.title("VOICE-AUGMENTATIONS")

# Add all your application here
app.add_page("audiomentations-lib", audiometations_pages.main)
app.add_page("WavAugment-lib", wavaugment.main)

# The main app
app.run()
