<template>
  <div id="app">
    <h1>音声感情分析アプリ</h1>
    <p>音声ファイルをアップロードして、感情を判定します。</p>
    
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadFile" :disabled="!selectedFile">アップロードして解析</button>

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

      try {
        const response = await axios.post("/api/upload", formData, {
  	headers: {
    	"Content-Type": "multipart/form-data",
  		},
	});

        this.result = response.data;
      } catch (error) {
        console.error("アップロード失敗:", error);
      }
    },
  },
};
</script>

<style>
#app {
  max-width: 600px;
  margin: 30px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fafafa;
}
button {
  margin-top: 10px;
  padding: 8px 12px;
}
</style>
