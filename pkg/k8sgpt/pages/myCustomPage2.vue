<template>
  <div>
    <!-- Dashboard Header with Namespace Selector -->
    <div class="dashboard-header">
      <h2>K8s Cluster Management API</h2>
    </div>

    <!-- Main Dashboard Content -->
    <div class="dashboard">
      <!-- Row with input, Upload File button, and Install Operator button -->
      <div class="file-upload-row">
        <input type="file" ref="fileInput" />
        <button @click="uploadFile">Upload File</button>

        <!-- Install Operator button stays until the success message disappears -->
        <button v-if="filename && !hideInstallButton" @click="installOperator">
          Install Operator
        </button>
      </div>

      <!-- Success message for file upload -->
      <div v-if="uploadSuccess" class="success-message">
        File uploaded successfully!
      </div>

      <!-- Success message for install operator -->
      <div v-if="installSuccess" class="success-message">
        Operator installed successfully!
      </div>

      <!-- Cluster Names Table -->
      <div class="cluster-table">
        <table>
          <thead>
            <tr>
              <th>Serial Number</th>
              <th>Cluster Name</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cluster, index) in clusterNames" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ cluster.cluster_name }}</td>
              <td>
                <button @click="removeCluster(cluster.filename)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Success message for file deletion -->
      <div v-if="deleteSuccess" class="success-message">
        File deleted successfully!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Reactive variables
const fileInput = ref(null);
const filename = ref(null);
const kubeconfigFilename = ref('');
const uploadSuccess = ref(false);
const installSuccess = ref(false);
const hideInstallButton = ref(false); // For controlling button visibility
const clusterNames = ref([]); // Holds the cluster names fetched from the API
const deleteSuccess = ref(false);

// Function to fetch cluster names
const fetchClusterNames = async () => {
  try {
    const response = await axios.get('https://10.0.35.221:8000/get-cluster-names');
    clusterNames.value = response.data.cluster_names;
  } catch (error) {
    console.error('Error fetching cluster names:', error);
  }
};

// Fetch cluster names on component mount
onMounted(() => {
  fetchClusterNames();
});

// Function to upload file
// Function to upload file
const uploadFile = async () => {
  const formData = new FormData();
  formData.append('file', fileInput.value.files[0]);

  try {
    const response = await axios.post('https://10.0.35.221:8000/upload_kubeconfig', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    filename.value = response.data.filename;
    kubeconfigFilename.value = filename.value;

    // Show success message for 5 seconds
    uploadSuccess.value = true;
    setTimeout(() => {
      uploadSuccess.value = false;
    }, 5000);

    // Fetch the updated cluster names after successful upload
    await fetchClusterNames();  // Fetch new cluster names after file upload
  } catch (error) {
    console.error('Error uploading file:', error);
  }
};


// Function to install operator
const installOperator = async () => {
  if (!kubeconfigFilename.value) return;

  try {
    const response = await axios.post('https://10.0.35.221:8000/install-operator', null, {
      params: {
        kubeconfig_filename: kubeconfigFilename.value,
      },
    });

    // Show success message for 5 seconds
    installSuccess.value = true;
    setTimeout(() => {
      installSuccess.value = false;
      hideInstallButton.value = true; // Hide the button after 5 seconds
    }, 5000);
  } catch (error) {
    console.error('Error installing operator:', error);
  }
};

// Function to delete a cluster by filename
const removeCluster = async (filename) => {
  try {
    const response = await axios.delete(`https://10.0.35.221:8000/remove-kubeconfig`, {
      params: { filename },
    });

    // Show success message for 5 seconds
    deleteSuccess.value = true;
    setTimeout(() => {
      deleteSuccess.value = false;
    }, 5000);

    // Refresh the cluster names list after deletion
    fetchClusterNames();
  } catch (error) {
    console.error('Error deleting kubeconfig file:', error);
  }
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

.file-upload-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  /* background-color: rgb(250, 247, 247); */
}

button {
  background-color: #297DB4;
  color: white;
  border: none;
  cursor: pointer;
  /* padding: 10px 15px; */
}

button:hover {
  background-color: #0056b3;
}

.cluster-table {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.success-message {
  margin-top: 10px;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  font-weight: bold;
  text-align: center;
  border-radius: 5px;
}
</style>
