import streamlit as st
from PIL import Image
import numpy as np
import shared
import foto
import recorte

# Web page configuration ---------------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Image Code Extractor")

st.write("## Obtain your code in seconds!")
st.write(
    "Try uploading a photo or screenshot to watch the code magically appear. This code is open source and available [here](https://github.com/bnvulpe/code-extractor) on GitHub."
)

# Functions ----------------------------------------------------------------------------------------------------------------------------------

def extract_from_image(upload, recorte_var):
    # Show original image on the left
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    # Get and show obtained code

    image_array = np.array(Image.open(upload))

    if recorte_var:
        code = recorte.ocr(image_array, tesseract_path = r'Tesseract-OCR\tesseract.exe')
    else:
        code = foto.ocr(image_array, tesseract_path = r'Tesseract-OCR\tesseract.exe')
    
    col2.write("Obtained code :wrench:")
    col2.text(code)
    #st.sidebar.markdown("\n")
    #st.sidebar.download_button(label="Download obtained code", data=convert_image(fixed), file_name="fixed.png", mime="image/png")

# Main ---------------------------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns(2)
recorte_input = None
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
option = st.sidebar.selectbox(
   "What kind of image are we dealing with?",
   ("Computer screen photo", "Screenshot"),
   index=None,
   placeholder="Select contact method...",
)
st.sidebar.write('You selected:', option)

if option == "Computer screen photo":
    recorte_input = False

if option == "Screenshot":
    recorte_input = True

if my_upload is not None and recorte_input is not None:
    extract_from_image(upload=my_upload, recorte_var = recorte_input)

else:
    extract_from_image("images/primes.jpg", False)




