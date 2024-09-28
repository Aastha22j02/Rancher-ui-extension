<template>
  <div>
    <!-- Dashboard Header with Namespace Selector -->
    <div class="dashboard-header">
      <h2>k8sGPT API Demo</h2>
    </div>

    <!-- Main Dashboard Content -->
    <div class="dashboard">
      <h1>API Call Test</h1>
      <input type="file" ref="fileInput" />
      <button @click="uploadFile">Submit</button>

      <div v-if="filename">
        <h3>File uploaded successfully: {{ filename }}</h3>
        <input type="text" v-model="kubeconfigFilename" placeholder="Kubeconfig Filename" />
        <button @click="installOperator">Install Operator</button>
      </div>
    </div>
  </div>
</template>

<script>
import { Card as RCard, Button as RButton } from '@rancher/components';
import axios from 'axios';

export default {
  components: {
    RCard,
    RButton,
  },
  data() {
    return {
      filename: null, // Store the uploaded filename here
      kubeconfigFilename: '', // Store filename for operator installation
    };
  },
  methods: {
    async uploadFile() {
      console.log('Uploading file...');

      const formData = new FormData();
      const fileInput = this.$refs.fileInput;
      formData.append('file', fileInput.files[0]);

      try {
        const response = await axios.post('https://10.0.35.221:5000/upload_kubeconfig', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        // Access the response data and set the filename
        this.filename = response.data.filename;
        this.kubeconfigFilename = this.filename; // Automatically populate the input with filename
        console.log('File uploaded successfully:', this.filename);
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    },

    async installOperator() {
      if (!this.kubeconfigFilename) {
        alert('Please enter the kubeconfig filename.');
        return;
      }

      try {
        const response = await axios.post('https://10.0.35.221:5000/install-operator', null, {
          params: {
            kubeconfig_filename: this.kubeconfigFilename,
          },
        });

        console.log('Operator installation response:', response.data);
        alert('Operator installed successfully!');
      } catch (error) {
        console.error('Error installing operator:', error);
        alert('Failed to install operator.');
      }
    },
  },
};
</script>

<style scoped>
.dashboard-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background-color: #f4f4f4;
}

.dashboard {
  padding: 20px;
}

button {
  background-color: #297DB4;
  color: white;
  border: none;
  /* border-radius: 5px; */
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}

input {
  padding: 10px;
  margin-top: 10px;
  display: block;
  width: 100%;
  max-width: 400px;
}
</style>
