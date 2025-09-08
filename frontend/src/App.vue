<template>
  <div id="app">
    <h1>音声感情分析アプリ</h1>
    <p>音声ファイルをアップロードして、感情を判定します。</p>
    
    <input type="file" @change="handleFileUpload" />
    
    <button @click="uploadFile" :disabled="!selectedFile || loading">
      {{ loading ? '解析中...' : 'アップロードして解析' }}
    </button>
    
    <div v-if="result">
      <h2>解析結果</h2>
      <p><strong>テキスト:</strong> {{ result.transcription }}</p>
      
      <h3>感情スコア</h3>
      <ul>
        <li
          v-for="emotion in result.emotions"
          :key="emotion.label"
          :style="{ 
            '--score-width': emotion.score + '%', 
            '--score-color': emotionColors[emotion.label] 
          }"
        >
          <div class="score-bar"></div>
          <strong>{{ emotion.label }}:</strong> {{ emotion.score }}%
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      selectedFile: null,
      result: null,
      loading: false,
      emotionColors: {
        '喜び': 'rgba(255, 255, 0, 0.3)',
        '悲しみ': 'rgba(0, 0, 255, 0.2)',
        '怒り': 'rgba(255, 0, 0, 0.2)',
        '驚き': 'rgba(255, 165, 0, 0.2)',
        '恐怖': 'rgba(128, 0, 128, 0.2)',
        '嫌悪': 'rgba(0, 128, 0, 0.2)',
        '中立': 'rgba(220, 220, 220, 0.4)',
        'その他': 'rgba(80, 80, 80, 0.3)'
      }
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      this.loading = true;

      try {
        const response = await axios.post("/api/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        this.result = response.data;
      } catch (error) {
        console.error("アップロード失敗:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #cccccc;
  color: #666666;
}

ul {
  list-style-type: none;
  padding: 0;
  max-width: 400px;
  margin: 20px auto;
  text-align: left;
}

li {
  position: relative;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 5px;
  overflow: hidden; /* バーがはみ出さないように */
  z-index: 1; /* コンテンツを前面に */
}

.score-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: var(--score-width);
  background-color: var(--score-color);
  z-index: -1; /* 背景に配置 */
  transition: width 0.5s ease-in-out;
}

li strong {
  z-index: 2; /* 文字がバーより手前になるように */
}
</style>