# backend/app.py
import os
os.environ["PATH"] = r"C:\ffmpeg\bin;" + os.environ["PATH"]
import tempfile
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
from transformers import pipeline
import torch

# ---------- Config ----------
EMOTION_MODEL = os.environ.get("EMOTION_MODEL", "koshin2001/Japanese-to-emotions")
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "small")  # tiny / base / small / medium / large
MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", 50))

# ---------- App ----------
app = Flask(__name__)
CORS(app)  # フロントをプロキシしない場合は適宜オリジン制限を追加すること
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_MB * 1024 * 1024

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".wav", ".wave"}

def allowed_filename(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

# ---------- Load models (on startup) ----------
logger.info(f"Loading Whisper ASR model: {WHISPER_MODEL}")
asr_model = whisper.load_model(WHISPER_MODEL)

device = 0 if torch.cuda.is_available() else -1
logger.info(f"Loading emotion model: {EMOTION_MODEL} (device={'cuda' if device==0 else 'cpu'})")

# モデルとトークナイザを個別にロードして、token_type_idsの問題に対処
from transformers import AutoModelForSequenceClassification, AutoTokenizer
model = AutoModelForSequenceClassification.from_pretrained(EMOTION_MODEL)
tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL)
model.to("cpu" if device == -1 else "cuda:0") # モデルを正しいデバイスに配置

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "whisper": WHISPER_MODEL, "emotion_model": EMOTION_MODEL})

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file field 'file' in request"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_filename(f.filename):
        return jsonify({"error": "Unsupported file extension. Only .wav allowed"}), 400

    # save to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        f.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Whisper transcription (日本語)
        logger.info("Transcribing audio with Whisper...")
        whisper_result = asr_model.transcribe(tmp_path, language="ja")
        text = whisper_result.get("text", "").strip()
        logger.info(f"Transcription: {text[:100]}")

        if not text:
            return jsonify({
                "transcription": "",
                "emotions": [],
                "top_emotion": None,
                "warning": "Transcription empty"
            }), 200

        # 手動によるトークン化と感情分類
        logger.info("Running emotion classification pipeline...")
        inputs = tokenizer(text, return_tensors="pt")
        if "token_type_ids" in inputs:
            del inputs["token_type_ids"]
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        logits = outputs.logits.squeeze(0)
        scores = torch.nn.functional.softmax(logits, dim=-1)

        # 感情ラベルをマッピングするための辞書
        emotion_map = {
            "LABEL_0": "喜び",
            "LABEL_1": "悲しみ",
            "LABEL_2": "怒り",
            "LABEL_3": "驚き",
            "LABEL_4": "恐怖",
            "LABEL_5": "嫌悪",
            "LABEL_6": "中立"
        }
        
        id2label = model.config.id2label
        emotions = [{"label": emotion_map.get(id2label[i], id2label[i]), "score": float(scores[i])} for i in range(len(scores))]
        
        emotions_sorted = sorted(emotions, key=lambda x: x["score"], reverse=True)
        top = emotions_sorted[0] if emotions_sorted else None

        return jsonify({
            "transcription": text,
            "emotions": emotions_sorted,
            "top_emotion": top
        }), 200

    except Exception as e:
        logger.exception("Processing error")
        return jsonify({"error": "Processing error", "detail": str(e)}), 500

    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)