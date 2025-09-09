// script.js
async function uploadAudio() {
    const audioFile = document.getElementById('audioFile').files[0];
    const resultDiv = document.getElementById('result');

    if (!audioFile) {
        resultDiv.innerText = 'ファイルが選択されていません。';
        return;
    }

    resultDiv.innerText = '分析中...';

    const formData = new FormData();
    formData.append('audio_file', audioFile);

    try {
        const response = await fetch('http://127.0.0.1:5000/predict_emotion', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);

        if (data.status === 'success') {
            const predictions = data.predictions;
            // スコアが最も高い感情を取得
            const topPrediction = predictions.reduce((prev, current) => (prev.score > current.score) ? prev : current);
            resultDiv.innerText = `予測結果: ${topPrediction.label} (スコア: ${topPrediction.score.toFixed(2)})`;
        } else {
            resultDiv.innerText = `エラー: ${data.error}`;
        }
    } catch (error) {
        resultDiv.innerText = `エラーが発生しました: ${error.message}`;
        console.error('Fetch error:', error);
    }
}