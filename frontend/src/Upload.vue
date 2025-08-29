<!-- frontend/src/components/Upload.vue -->
<template>
  <div style="padding:16px;border:1px solid #e6e6e6;border-radius:8px;background:#fafafa;">
    <div>
      <label for="wav">WAVファイルを選択:</label>
      <input id="wav" type="file" accept=".wav" @change="onFileChange" />
    </div>

    <div style="margin-top:12px;">
      <button @click="uploadFile" :disabled="!file || loading" style="padding:8px 12px;background:#007bff;color:white;border:none;border-radius:6px;cursor:pointer;">
        {{ loading ? '解析中...' : 'アップロードして解析' }}
      </button>
    </div>

    <div v-if="error" style="color:#c00;margin-top:12px;">{{ error }}</div>

    <div v-if="result" style="margin-top:18px;">
      <h3>文字起こし</h3>
      <div style="white-space:pre-wrap;padding:8px;background:white;border:1px solid #ddd;border-radius:6px;">{{ result.transcription }}</div>

      <h3 style="margin-top:12px;">感情スコア（各ラベル）</h3>
      <canvas ref="canvas" width="800" height="320"></canvas>

      <div style="margin-top:8px;">
        <strong>最有力:</strong>
        <span v-if="result.top_emotion">{{ result.top_emotion.label }} ({{ (result.top_emotion.score*100).toFixed(1) }}%)</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Chart, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default {
  data() {
    return {
      file: null,
      loading: false,
      error: null,
      result: null,
      chart: null
    }
  },
  methods: {
    onFileChange(e) {
      this.file = e.target.files[0];
    },
    async uploadFile() {
      if (!this.file) {
        this.error = "ファイルを選択してください";
        return;
      }
      this.loading = true;
      this.error = null;

      const formData = new FormData();
      formData.append("file", this.file);

      try {
        // /api/upload に proxy で転送される設定（vite.config.js）
        const res = await axios.post("/api/upload", formData, {
  		headers: { "Content-Type": "multipart/form-data" },
  		timeout: 120000
		});

        this.result = res.data;
        this.drawChart();
      } catch (err) {
        this.error = err.response?.data?.error || err.message;
      } finally {
        this.loading = false;
      }
    },
    drawChart() {
      if (!this.result || !this.result.emotions) return;

      const labels = this.result.emotions.map(e => e.label);
      const values = this.result.emotions.map(e => (e.score * 100));

      if (this.chart) {
        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = values;
        this.chart.update();
        return;
      }

      const ctx = this.$refs.canvas.getContext("2d");
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: '確率（％）',
            data: values,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, max: 100 }
          }
        }
      });
    }
  }
}
</script>

<style scoped>
/* optional */
</style>
