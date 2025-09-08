<template>
  <div id="app">
    <h1>音声感情分析アプリ(ベータ版)</h1>
    <p>音声ファイルをアップロードして、感情を判定します。</p>
    
    <input type="file" @change="handleFileUpload" />
    
    <button @click="uploadFile" :disabled="!selectedFile || loading">
      {{ loading ? '解析中...' : 'アップロードして解析' }}
    </button>
    
    <div v-if="result">
      <h2>解析結果</h2>
      <p><strong>感情:</strong> {{ result.top_emotion.label }}</p>
      <p><strong>テキスト:</strong> {{ result.transcription }}</p>
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

/* ボタンのスタイル */
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
  background-color: #45a358; 
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #206524;
  color: #CECECE;
}
</style>