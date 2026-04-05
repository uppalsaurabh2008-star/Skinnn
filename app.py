import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("AI Skin Analyzer")
st.write("Upload your face image")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

def analyze_skin(image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    analysis = {}

    brightness = np.mean(gray)
    analysis["Dull Skin"] = brightness < 100

    red_channel = img[:, :, 2]
    analysis["Redness / Acne"] = np.mean(red_channel) > 150

    h, w = gray.shape
    eye_region = gray[int(h*0.4):int(h*0.6), int(w*0.3):int(w*0.7)]
    analysis["Dark Circles"] = np.mean(eye_region) < brightness - 20

    analysis["Uneven Skin"] = np.var(gray) > 1500

    return analysis

def suggest(analysis):
    tips = []

    if analysis["Dull Skin"]:
        tips.append("Drink more water + Vitamin C")

    if analysis["Redness / Acne"]:
        tips.append("Avoid sugar + use salicylic facewash")

    if analysis["Dark Circles"]:
        tips.append("Sleep 7-8 hours + reduce screen time")

    if analysis["Uneven Skin"]:
        tips.append("Use sunscreen + exfoliate")

    if not tips:
        tips.append("Skin looks good! Maintain routine")

    return tips

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

    result = analyze_skin(image)

    st.write("### Skin Analysis")
    st.write(result)

    st.write("### Suggestions")
    for t in suggest(result):
        st.write("- " + t)
