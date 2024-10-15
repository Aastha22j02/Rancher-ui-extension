<template>
  
  <div>
    
    <!-- Dashboard Header with Namespace Selector -->
    <div class="dashboard-header">
      <div class="namespace-dropdown">
        <div>

        <!-- <label >Select Namespace:</label> -->
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
      <!-- <input type="file" ref="fileInput" />
      <button  @click="go">submit</button>
       -->
       <!-- <button
            class="btn role-primary"
            @click="go"
          >
         test
          </button> -->
    

      <div class="card-grid">
        
        <div class="col-md-6 mb-4">
        <div class="card shadow-sm card-spacing">
          <div class="card-body">
            <h5 class="card-title">Pod</h5>
            <p class="card-text">Manage and view your Pods in the selected namespace.</p>
            <br>
            <a @click="goToPods" class="btn btn-primary">Go to Pods</a>
          </div>
        </div>
      </div>

      <!-- Deployment Card -->
      <div class="col-md-6 mb-4">
        <div class="card shadow-sm card-spacing">
          <div class="card-body">
            <h5 class="card-title">Deployment</h5>
            <p class="card-text">View and manage your Deployments easily.</p>
            <br>

            <a @click="goToDeployments" class="btn btn-primary">Go to Deployments</a>
          </div>
        </div>
      </div>

      <!-- Services Card -->
      <div class="col-md-6 mb-4">
        <div class="card shadow-sm card-spacing">
          <div class="card-body">
            <h5 class="card-title">Services</h5>
            <p class="card-text">Explore the Services running in your cluster.</p>
            <br>

            <a @click="goToServices" class="btn btn-primary">Go to Services</a>
          </div>
        </div>
      </div>

      <!-- StorageClass Card -->
      <div class="col-md-6 mb-4">
        <div class="card shadow-sm card-spacing">
          <div class="card-body">
            <h5 class="card-title">StorageClass</h5>
            <p class="card-text">Manage and configure StorageClasses.</p>
            <br>

            <a @click="goToStorageClass" class="btn btn-primary">Go to StorageClass</a>
          </div>
        </div>
      </div>

      <!-- Secrets Card -->
      <div class="col-md-6 mb-4">
        <div class="card shadow-sm card-spacing">
          <div class="card-body">
            <h5 class="card-title">Secrets</h5>
            <p class="card-text">View and manage Kubernetes Secrets.</p>
            <br>

            <a @click="goToSecrets" class="btn btn-primary">Go to Secrets</a>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
// import ButtonDropdown from '@shell/components/ButtonDropdown';

// Setup the data and methods
const selectedNamespace = ref('');
const namespaces = ['default', 'kube-system', 'kube-public', 'custom-namespace'];

// Functions to handle button clicks for different sections
const goToPods = () => {
  console.log('Navigating to Pods');
  // Call the function to fetch Pods or navigate to the Pods page
};

const goToDeployments = () => {
  console.log('Navigating to Deployments');
  // Call the function to fetch Deployments or navigate to the Deployments page
};

const goToServices = () => {
  console.log('Navigating to Services');
  // Call the function to fetch Services or navigate to the Services page
};

const goToStorageClass = () => {
  console.log('Navigating to StorageClass');
  // Call the function to fetch StorageClasses or navigate to the StorageClasses page
};

const goToSecrets = () => {
  console.log('Navigating to Secrets');
  // Call the function to fetch Secrets or navigate to the Secrets page
};
</script>

<style scoped>
/* Container for aligning the namespace dropdown to the right */
.dashboard-header {
  display: flex;
  justify-content: flex-end; /* Align to the right */
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
  border: 1px solid #dee2e6; /* Add this line for the border */
}

.card-spacing:hover {
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
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
</style>
