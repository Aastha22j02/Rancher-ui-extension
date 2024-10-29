<template>

  <div>


    <!-- Dashboard Header with Namespace Selector -->
    <div class="dashboard-header">

      <div class="namespace-dropdown" @click="fetchNamespaces">
        <div>
          <select v-model="selectedNamespace" class="border border-gray-300 p-2 rounded">
            <option disabled value="">Select Namespace</option>
            <option v-for="namespace in namespaces" :key="namespace" :value="namespace">
              {{ namespace }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Main Dashboard Content -->
    <div class="dashboard">
      <h1>k8sGPT Dashboard</h1>




      <div class="card-grid">


        <r-card>
          <template v-slot:title>
            <h3> Pod</h3>
          </template>

          <template v-slot:body>
          </template>

          <template v-slot:actions>
            <button class="btn btn-primary" @click="goToPods">Go to Pods</button>
          </template>
        </r-card>


        <r-card>
          <template v-slot:title>
            <h3> Deployment </h3>
          </template>

          <template v-slot:body>
          </template>

          <template v-slot:actions>
            <button class="btn btn-primary" @click="goToDeployments">Go to Deployments</button>
          </template>
        </r-card>



        <r-card>
          <template v-slot:title>
            <h3> Services </h3>
          </template>

          <template v-slot:body>
          </template>

          <template v-slot:actions>
            <button class="btn btn-primary" @click="goToServices">Go to Services</button>
          </template>
        </r-card>


        <r-card>
          <template v-slot:title>
            <h3> StorageClass</h3>
          </template>

          <template v-slot:body>
          </template>

          <template v-slot:actions>
            <button class="btn btn-primary" @click="goToStorageClass">Go to StorageClass</button>
          </template>
        </r-card>



        <r-card>
          <template v-slot:title>
            <h3> Secrets</h3>
          </template>

          <template v-slot:body>
          </template>

          <template v-slot:actions>
            <button class="btn btn-primary" @click="goToSecrets">Go to Secrets</button>
          </template>
        </r-card>


      </div>
    </div>

    <div v-if="showSuccessPopup" class="popup">
  <div class="popup-content">
    <p> <span v-html="successMessage"></span></p> <!-- Use v-html instead of {{ }} -->
    <br>
    <button @click="closePopup" class="btn btn-primary">Close</button>
  </div>
</div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';


import { Card as RCard, Button as RButton } from '@rancher/components';


const buttonText = ref('Get Pod')

const content = ref('data')
const showSuccessPopup = ref(false);
const successMessage = ref('');
// Setup the data and methods
const selectedNamespace = ref('');
const namespaces = ref([]);
console.log("namespace", namespaces)
const activeFilename = ref(''); // To store the active filename


// Fetch active cluster filename and namespaces
const fetchNamespaces = async () => {
  try {
    console.log("aastha")
    // Fetch the active cluster filename first
    const activeFilename = await fetchActiveClusterFilename();
    console.log("activefilename", activeFilename)
    if (!activeFilename) {
      console.error('No active cluster found.');
      return;
    }


    // Fetch namespaces based on the active cluster filename
    const response = await axios.get(`https://10.0.35.221:8000/get-namespaces`, {
      params: { filename: activeFilename }
    });
    console.log(response)

    // Set the namespaces dynamically based on the response
    namespaces.value = response.data.namespaces;
  } catch (error) {
    console.error('Error fetching namespaces:', error);
  }
};

// Fetch the active filename (already in your code)
const fetchActiveClusterFilename = async () => {
  try {
    const response = await axios.get('https://10.0.35.221:8000/get-cluster-names');
    const activeCluster = response.data.cluster_names.find(cluster => cluster.active);
    console.log("activecluster", activeCluster)

    if (activeCluster) {
      return activeCluster.filename;
    } else {
      throw new Error('No active cluster found');
    }
  } catch (error) {
    console.error('Error fetching cluster names:', error);
    return null;
  }
};
const goToPods = async () => {
      try {
        const activeFilename = await fetchActiveClusterFilename();
        if (!activeFilename) {
          successMessage.value = 'No active cluster found.';
          showSuccessPopup.value = true;
          return;
        }

        const apiUrl = 'https://10.0.35.221:8000/analyze';
        const params = {
          // kubeconfig_filename: activeFilename,
          backend: 'ollama',
          anonymize: false,
          custom_analysis: false,
          explain: true,
          filter: 'Pod',
          interactive: false,
          language: 'english',
          max_concurrency: 10,
          no_cache: false,
          output: 'text',
          with_doc: false,
          namespace: namespaces.value
        };

        const response = await axios.get(apiUrl, { params });
        if (response.status === 200) {
          const { status, results } = response.data;
          
          if (status === "OK" && results === null) {
            successMessage.value = 'Pods running! No error found.';
          } 
          else if (status === "ProblemDetected" && results) {
            let errorMessages = results.map((result, index) => {
              let errorText = result.error.map(err => `<span style="color: red;">${err.Text}</span>`).join('<br>');
              let solutionText = result.details.split('Solution:')[1].trim().split('\n').map((solution, idx) => `<li style = "list-style-type: none;">${solution}</li>`).join('');

              return `
                <div>
                  <h4><strong>Problem ${index + 1}: ${result.name}</strong></h4>
                  <p><strong>Error:</strong><br> ${errorText}</p>
                  <p><strong>Solution:</strong> 
                    <ol style="color: green;">${solutionText}</ol>
                  </p>
                  <hr>
                </div>
              `;
            }).join('');

            successMessage.value = `
              <h3 style="color: red;">Problems Detected (${response.data.problems}):</h3>
              ${errorMessages}
            `;
          } else {
            successMessage.value = 'Unknown response status.';
          }

          showSuccessPopup.value = true;
        } else {
          successMessage.value = 'Something went wrong. Please try again.';
          showSuccessPopup.value = true;
        }
      } catch (error) {
        console.error('Error fetching pods:', error);
        successMessage.value = 'Error: ' + error.message;
        showSuccessPopup.value = true;
      }
    };



// Function to close the pop-up
const closePopup = () => {
  showSuccessPopup.value = false;
};

const goToDeployments = async () => {
  try {
        const activeFilename = await fetchActiveClusterFilename();
        if (!activeFilename) {
          successMessage.value = 'No active cluster found.';
          showSuccessPopup.value = true;
          return;
        }

        const apiUrl = 'https://10.0.35.221:8000/analyze';
        const params = {
          kubeconfig_filename: activeFilename,
          anonymize: false,
          custom_analysis: false,
          explain: true,
          filter: 'Deployment',
          interactive: false,
          language: 'english',
          max_concurrency: 10,
          no_cache: false,
          output: 'text',
          with_doc: false,
        };

        const response = await axios.get(apiUrl, { params });
        if (response.status === 200) {
          const { status, results } = response.data;
          
          if (status === "OK" && results === null) {
            successMessage.value = 'Deployments running! No error found.';
          } 
          else if (status === "ProblemDetected" && results) {
            let errorMessages = results.map((result, index) => {
              let errorText = result.error.map(err => `<span style="color: red;">${err.Text}</span>`).join('<br>');
              let solutionText = result.details.split('Solution:')[1].trim().split('\n').map((solution, idx) => `<li>${solution}</li>`).join('');

              return `
                <div>
                  <h4><strong>Problem ${index + 1}: ${result.name}</strong></h4>
                  <p><strong>Error:</strong><br> ${errorText}</p>
                  <p><strong>Solution:</strong> 
                    <ol style="color: green;">${solutionText}</ol>
                  </p>
                  <hr>
                </div>
              `;
            }).join('');

            successMessage.value = `
              <h3 style="color: red;">Problems Detected (${response.data.problems}):</h3>
              ${errorMessages}
            `;
          } else {
            successMessage.value = 'Unknown response status.';
          }

          showSuccessPopup.value = true;
        } else {
          successMessage.value = 'Something went wrong. Please try again.';
          showSuccessPopup.value = true;
        }
      } catch (error) {
        console.error('Error fetching Deployments:', error);
        successMessage.value = 'Error: ' + error.message;
        showSuccessPopup.value = true;
      }
};


const goToServices = async () => {
  try {
        const activeFilename = await fetchActiveClusterFilename();
        if (!activeFilename) {
          successMessage.value = 'No active cluster found.';
          showSuccessPopup.value = true;
          return;
        }

        const apiUrl = 'https://10.0.35.221:8000/analyze';
        const params = {
          // kubeconfig_filename: activeFilename,
          backend: 'ollama',

          anonymize: false,
          custom_analysis: false,
          explain: true,
          filter: 'Service',
          interactive: false,
          language: 'english',
          max_concurrency: 10,
          no_cache: false,
          output: 'text',
          with_doc: false,
        };

        const response = await axios.get(apiUrl, { params });
        if (response.status === 200) {
          const { status, results } = response.data;
          
          if (status === "OK" && results === null) {
            successMessage.value = 'Service running! No error found.';
          } 
          else if (status === "ProblemDetected" && results) {
            let errorMessages = results.map((result, index) => {
              let errorText = result.error.map(err => `<span style="color: red;">${err.Text}</span>`).join('<br>');
              let solutionText = result.details.split('Solution:')[1].trim().split('\n').map((solution, idx) => `<li style = "list-style-type: none;">${solution}</li>`).join('');

              return `
                <div>
                  <h4><strong>Problem ${index + 1}: ${result.name}</strong></h4>
                  <p><strong>Error:</strong><br> ${errorText}</p>
                  <p><strong>Solution:</strong> 
                    <span style="color: blue;">${solutionText}</span>
                  </p>
                  ${solutionText}
                  <hr>
                </div>
              `;
            }).join('');

            successMessage.value = `
              <h3 style="color: red;">Problems Detected (${response.data.problems}):</h3>
              ${errorMessages}
            `;
          } else {
            successMessage.value = 'Unknown response status.';
          }

          showSuccessPopup.value = true;
        } else {
          successMessage.value = 'Something went wrong. Please try again.';
          showSuccessPopup.value = true;
        }
      } catch (error) {
        console.error('Error fetching service:', error);
        successMessage.value = 'Error: ' + error.message;
        showSuccessPopup.value = true;
      }
};



const goToStorageClass = async () => {
  try {
    // API URL
    const apiUrl = 'https://10.0.35.221:8000/analyze';
    const params = {
      // kubeconfig_filename: '036b3e3d-3dee-4764-a5b4-8ded9a1b8610.txt',
      backend: 'ollama',

      anonymize: false,
      custom_analysis: false,
      explain: true,
      filter: 'Pod',
      interactive: false,
      language: 'english',
      max_concurrency: 10,
      no_cache: false,
      output: 'text',
      with_doc: false,
    };

    // Make the API request using Axios
    const response = await axios.get(apiUrl, { params });

    // If the response is OK, show the success pop-up
    if (response.status === 200) {
      successMessage.value = 'StorageClass  running!! No Error found.';
      showSuccessPopup.value = true;
    } else {
      successMessage.value = 'Something went wrong. Please try again.';
      showSuccessPopup.value = true;
    }
  } catch (error) {
    console.error('Error fetching StorageClass :', error);
    successMessage.value = 'Error: ' + error.message;
    showSuccessPopup.value = true;
  }
};

const goToSecrets = async () => {
  try {
    // API URL
    const apiUrl = 'https://10.0.35.221:8000/analyze';
    const params = {
      kubeconfig_filename: '036b3e3d-3dee-4764-a5b4-8ded9a1b8610.txt',
      anonymize: false,
      custom_analysis: false,
      explain: true,
      filter: 'Pod',
      interactive: false,
      language: 'english',
      max_concurrency: 10,
      no_cache: false,
      output: 'text',
      with_doc: false,
    };

    // Make the API request using Axios
    const response = await axios.get(apiUrl, { params });

    // If the response is OK, show the success pop-up
    if (response.status === 200) {
      successMessage.value = 'Secrets running!! No Error found.';
      showSuccessPopup.value = true;
    } else {
      successMessage.value = 'Something went wrong. Please try again.';
      showSuccessPopup.value = true;
    }
  } catch (error) {
    console.error('Error fetching Secrets :', error);
    successMessage.value = 'Error: ' + error.message;
    showSuccessPopup.value = true;
  }
};
</script>

<style scoped>
/* Container for aligning the namespace dropdown to the right */
.dashboard-header {
  display: flex;
  justify-content: flex-end;
  /* Align to the right */
  align-items: center;
  padding: 10px;
  background-color: #f4f4f4;
}

.namespace-dropdown {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Main dashboard styles */
.dashboard {
  padding: 20px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

/* Styling for buttons */
.r-button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.r-button:hover {
  background-color: #0056b3;
}

.card-spacing {
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
  border: 1px solid #dee2e6;
  /* Add this line for the border */
}

.card-spacing:hover {
  box-shadow: 0 0 20px rgba(146, 196, 117, 0.1);
}

.card-title {
  font-size: 1.25rem;
  color: #006fbb;
}

.card-text {
  color: #4a4a4a;
}

.btn-primary {
  background-color: #297DB4;
  border-color: #297DB4;
  color: white;
}

.btn-primary:hover {
  background-color: #005a99;
  border-color: #005a99;
}

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgb(227, 241, 239);
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  z-index: 1000;
}

.popup-content {
  text-align: left;
}
</style>
