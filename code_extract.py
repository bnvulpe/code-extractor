import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

# Web page configuration ---------------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Image Code Extractor")

st.write("## Obtain your code in seconds!")
st.write(
    "Try uploading a photo or screenshot to watch the code magically appear. Full code can be downloaded from the sidebar. This code is open source and available [here](https://github.com/bnvulpe/code-extractor) on GitHub."
)
st.sidebar.write("## Upload and download full code :gear:")

# MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Functions ---------------------------------------------------------------------------------------------------------------------------------------
# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im
    
# Resize image
def resize_image_to_dpi(image_path, target_dpi = 600):
    img = Image.open(image_path)

    # Get the current DPI (dots per inch) of the image
    current_dpi = img.info.get("dpi", (300, 300))

    # Calculate the resize factor
    resize_factor = target_dpi / current_dpi[0]

    # Calculate the new size in pixels
    new_width = int(img.width * resize_factor)
    new_height = int(img.height * resize_factor)

    # Resize the image
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)

    # Set the new DPI
    resized_img.info["dpi"] = (target_dpi, target_dpi)
    
    return np.array(resized_img)
    

def fix_image(upload):
    # Show original image on the left
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    # Get and show obtained code
    fixed = remove(image)
    col2.write("Obtained code :wrench:")
    col2.image(fixed)
    #st.sidebar.markdown("\n")
    #st.sidebar.download_button(label="Download obtained code", data=convert_image(fixed), file_name="fixed.png", mime="image/png")

# Main ---------------------------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    #if my_upload.size > MAX_FILE_SIZE:
        #st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    #else:
    fix_image(upload=my_upload)
else:
    fix_image("./zebra.jpg")
