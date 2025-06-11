import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator

st.set_page_config(page_title="Batch Image Translator", layout="wide")

st.title("📄🈂️ Batch Image Translator")
st.markdown("Upload multiple images, and this app will extract and translate all the text at once.")

uploaded_files = st.file_uploader("Upload Image(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
target_lang = st.text_input("Target Language (e.g., 'en' for English, 'ja' for Japanese)", value="en")

translator = Translator()

def extract_text(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image).strip()

if uploaded_files and target_lang:
    with st.spinner("Processing images..."):
        results = []
        for img in uploaded_files:
            filename = img.name
            try:
                extracted_text = extract_text(img)
                if not extracted_text:
                    translated = "(No text found)"
                else:
                    translated = translator.translate(extracted_text, dest=target_lang).text
                results.append((filename, translated))
            except Exception as e:
                results.append((filename, f"(Error: {str(e)})"))

    st.success("Translation complete!")
    for filename, translated in results:
        st.subheader(f"🖼 {filename}")
        st.text_area("Translation", value=translated, height=150)
else:
    st.info("Please upload image(s) and enter a target language.")
