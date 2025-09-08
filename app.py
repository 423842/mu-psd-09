# app.py

import os
from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

try:
    classifier = pipeline(
        "audio-classification", 
        model="superb/wav2vec2-base-superb-er"  # モデル名を修正
    )
    print("AIモデルが正常にロードされました。")
except Exception as e:
    print(f"モデルのロード中にエラーが発生しました: {e}")
    exit()

# 以下、変更なし
# ...
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/predict_emotion', methods=['POST'])
def predict_emotion():
    if 'audio_file' not in request.files:
        return jsonify({'error': '音声ファイルがアップロードされていません'}), 400
    
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400

    if audio_file:
        temp_file_path = "temp_audio_input.wav"
        audio_file.save(temp_file_path)

        try:
            prediction_result = classifier(temp_file_path)
            response = {
                'status': 'success',
                'predictions': prediction_result
            }
            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': f'音声処理または予測中にエラーが発生しました: {e}'}), 500
        finally:
            os.remove(temp_file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)