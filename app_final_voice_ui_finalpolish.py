import streamlit as st
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
from gtts import gTTS
import tempfile, os, base64, random, datetime, pandas as pd, requests
from streamlit_lottie import st_lottie

# =========================================================
# CONFIG
# =========================================================
MODEL_PATH = "ai_real_unified_best_strong.pth"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FEEDBACK_LOG = "feedback_log.csv"

# =========================================================
# LOAD MODEL
# =========================================================
@st.cache_resource
def load_model():
    from torchvision import models
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, 2)
    ckpt = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(ckpt["model"] if "model" in ckpt else ckpt)
    model.to(DEVICE).eval()
    return model

model = load_model()

# =========================================================
# IMAGE TRANSFORM
# =========================================================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# =========================================================
# CSV INITIALIZATION / AUTO-FIX
# =========================================================
def ensure_csv_schema():
    required_cols = ["Filename", "Prediction", "Correct", "Confidence", "Timestamp"]
    if not os.path.exists(FEEDBACK_LOG):
        pd.DataFrame(columns=required_cols).to_csv(FEEDBACK_LOG, index=False)
        return
    try:
        df = pd.read_csv(FEEDBACK_LOG)
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
        df = df[required_cols]
        df.to_csv(FEEDBACK_LOG, index=False)
    except Exception:
        pd.DataFrame(columns=required_cols).to_csv(FEEDBACK_LOG, index=False)

ensure_csv_schema()

# =========================================================
# LOTTIE LOADER
# =========================================================
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None

ai_loader = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_tutvdkg0.json")
if ai_loader is None:
    ai_loader = {
        "v": "5.5.7",
        "fr": 30,
        "ip": 0,
        "op": 60,
        "w": 200,
        "h": 200,
        "nm": "loader",
        "ddd": 0,
        "assets": [],
        "layers": [{
            "ty": 4,
            "nm": "circle",
            "ks": {
                "o": {"k": 100},
                "r": {"k": 0},
                "p": {"k": [100, 100, 0]},
                "a": {"k": [0, 0, 0]},
                "s": {"k": [100, 100, 100]}
            },
            "shapes": [{
                "ty": "el",
                "p": {"k": [0, 0]},
                "s": {"k": [150, 150]},
                "nm": "Ellipse Path 1"
            },
            {
                "ty": "st",
                "c": {"k": [0.1, 0.8, 1, 1]},
                "o": {"k": 100},
                "w": {"k": 8},
                "lc": 2,
                "lj": 2,
                "nm": "Stroke 1"
            }]
        }]
    }

# =========================================================
# AUTO VOICE OUTPUT
# =========================================================
def get_voice_html(text, lang="English", autoplay=False):
    if lang == "English":
        tts = gTTS(text=text, lang="en")
    elif lang == "Hindi":
        text = text.replace("This image is real.", "Yeh tasveer asli hai.")
        text = text.replace("This image is fake.", "Yeh tasveer nakli hai.")
        tts = gTTS(text=text, lang="hi")
    elif lang == "Both":
        text = text + " " + text.replace("This image is real.", "Yeh tasveer asli hai.")\
                                .replace("This image is fake.", "Yeh tasveer nakli hai.")
        tts = gTTS(text=text, lang="en")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    with open(tmp.name, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    autoplay_attr = "autoplay" if autoplay else ""
    audio_html = f"""
    <audio controls {autoplay_attr} style="width: 100%; margin-top: 10px;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    try: os.remove(tmp.name)
    except PermissionError: pass
    return audio_html

# =========================================================
# PREDICTION
# =========================================================
def predict_image(img):
    img_t = transform(img).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        out = model(img_t)
        prob = torch.nn.functional.softmax(out, dim=1)[0].cpu().numpy()
    label = "Real" if np.argmax(prob) == 1 else "Fake"
    conf = prob[np.argmax(prob)] * 100
    return label, conf

# =========================================================
# DYNAMIC BACKGROUND (continuous animation)
# =========================================================
def dynamic_background():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(-45deg, #0f2027, #203A43, #2C5364, #243B55);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    @keyframes gradientShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# STYLING
# =========================================================
st.set_page_config(page_title="AI Image Realness Detector Deluxe", layout="wide")
dynamic_background()

st.markdown("""
<style>
h1 {
    text-align:center;
    background: linear-gradient(90deg,#00E5FF,#FF4081);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8em;
}
.result-card {
    padding: 25px;
    border-radius: 18px;
    margin-top: 25px;
    transition: all 0.4s ease;
    background: rgba(255,255,255,0.07);
    box-shadow: 0 0 25px rgba(0,229,255,0.25);
}
.result-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 40px rgba(255,255,255,0.3);
}
.feedback-btn {
    border: none;
    padding: 10px 20px;
    font-size: 1em;
    font-weight: 600;
    border-radius: 10px;
    cursor: pointer;
    color: white;
    margin: 5px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.feedback-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 0 20px rgba(255,255,255,0.3);
}
.green-btn { background-color: #00E676; }
.red-btn { background-color: #FF1744; }
footer {
    text-align:center;
    color:#ccc;
    margin-top:40px;
    font-size:0.9em;
}
.stats-box {
    background: rgba(0,0,0,0.3);
    border-radius: 15px;
    padding: 15px;
    text-align:center;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("<h1>🧠 AI Real vs Fake Image Detector Deluxe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ddd;'>Upload one or more images, hear bilingual feedback, and give ratings to help the AI learn.</p>", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
lang_option = st.sidebar.radio("🗣️ Voice Output", ["English", "Hindi", "Both"], index=0)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.info("🎨 Dynamic background runs smoothly and adapts automatically.")

# =========================================================
# UPLOAD + SUMMARY
# =========================================================
uploaded_files = st.file_uploader("📸 Upload images", type=["jpg","jpeg","png"], accept_multiple_files=True)

def display_summary():
    ensure_csv_schema()
    df = pd.read_csv(FEEDBACK_LOG)
    total = len(df)
    correct = len(df[df["Correct"] == "Yes"])
    real = len(df[df["Prediction"] == "Real"])
    fake = len(df[df["Prediction"] == "Fake"])
    acc = (correct / total * 100) if total > 0 else 0
    avg_conf = df["Confidence"].mean() if total > 0 else 0
    st.markdown(f"""
    <div class='stats-box'>
    <b>📊 Total:</b> {total} | 
    ✅ <b>Correct:</b> {correct} | 
    💡 <b>Real:</b> {real} | 
    ⚠️ <b>Fake:</b> {fake} | 
    🎯 <b>Accuracy:</b> {acc:.1f}% | 
    🔒 <b>Avg Confidence:</b> {avg_conf:.1f}%
    </div>
    """, unsafe_allow_html=True)

display_summary()

# =========================================================
# MAIN LOGIC
# =========================================================
if uploaded_files:
    with st.spinner("Analyzing images..."):
        st_lottie(ai_loader, height=180, key="ai_load")

        for idx, file in enumerate(uploaded_files):
            img = Image.open(file).convert("RGB")
            label, conf = predict_image(img)
            color = "#00E676" if label == "Real" else "#FF1744"
            bg = "rgba(0,255,150,0.15)" if label == "Real" else "rgba(255,50,50,0.15)"

            st.markdown(f"""
            <div class='result-card' style='border-left:6px solid {color};background:{bg};'>
            <h3 style='color:{color};text-align:center;'>{file.name}</h3>
            <p style='text-align:center;'>
            <b>Prediction:</b> {label}<br>
            <b>Confidence:</b> {conf:.2f}%
            </p>
            </div>
            """, unsafe_allow_html=True)

            st.image(img, width=350)

            if idx == 0:
                st.markdown(get_voice_html(f"This image is {label.lower()}.", lang_option, autoplay=True), unsafe_allow_html=True)
            else:
                st.markdown(get_voice_html(f"This image is {label.lower()}.", lang_option, autoplay=False), unsafe_allow_html=True)

            if label == "Fake":
                st.markdown("<div style='text-align:center;color:#FF4444;'>⚡ Warning: Looks suspicious!</div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Prediction Correct ({file.name})", key=f"yes_{file.name}"):
                    entry = {"Filename": file.name, "Prediction": label, "Correct": "Yes",
                             "Confidence": conf, "Timestamp": datetime.datetime.now()}
                    pd.DataFrame([entry]).to_csv(FEEDBACK_LOG, mode='a', index=False, header=False)
                    st.success("Feedback saved ✅")
            with col2:
                if st.button(f"❌ Prediction Wrong ({file.name})", key=f"no_{file.name}"):
                    entry = {"Filename": file.name, "Prediction": label, "Correct": "No",
                             "Confidence": conf, "Timestamp": datetime.datetime.now()}
                    pd.DataFrame([entry]).to_csv(FEEDBACK_LOG, mode='a', index=False, header=False)
                    st.error("Feedback saved ❌")

        display_summary()

st.markdown("<footer>Made with ❤️ by Sangam Rai</footer>", unsafe_allow_html=True)

