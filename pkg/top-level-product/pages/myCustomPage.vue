<template>
  <div>
    <!-- Dashboard Header with Namespace Selector -->
    <div class="dashboard-header">
      <div class="namespace-dropdown">
        <label for="namespace">Select Namespace:</label>

        <!-- Dropdown for namespaces -->
        <ButtonDropdown
          v-bind="{
            buttonLabel: selectedNamespace || 'Select Namespace',
            dropdownOptions: namespaces,
            size: 'sm'
          }"
          @option-selected="selectNamespace"
        />
      </div>
    </div>

    <!-- Main Dashboard Content -->
    <div class="dashboard">
      <h1>k8sGPT Dashboard</h1>

      <div class="card-grid">
        <!-- Cards for various Kubernetes objects -->
        <r-card title="Pod" :description="'Manage and view your Pods'">
          <template #footer>
            <button class="r-button">Go to Pod</button>
          </template>
        </r-card>

        <r-card title="Deployment" :description="'Manage your Deployments'">
          <template #footer>
            <button class="r-button">Go to Deployment</button>
          </template>
        </r-card>

        <r-card title="Services" :description="'View and configure Services'">
          <template #footer>
            <button class="r-button">Go to Services</button>
          </template>
        </r-card>

        <r-card title="StorageClass" :description="'View StorageClass details'">
          <template #footer>
            <button class="r-button">Go to StorageClass</button>
          </template>
        </r-card>

        <r-card title="Secrets" :description="'Manage application Secrets'">
          <template #footer>
            <button class="r-button">Go to Secrets</button>
          </template>
        </r-card>
      </div>
    </div>
  </div>
</template>

<script>
import { Card as RCard, Button as RButton } from '@rancher/components';
import ButtonDropdown from '@shell/components/ButtonDropdown'; // Rancher ButtonDropdown component
 
export default {
  components: {
    RCard,
    RButton,
    ButtonDropdown,
  },
  data() {
    return {
      namespaces: [], // Use array for better dropdown management
      selectedNamespace: null,
    };
  },
  methods: {
    async fetchNamespaces() {
      try {
        const response = await fetch("/v3/projects/{projectId}/namespaces", {
          method: "GET",
          // No need for token if using session-based Rancher auth
        });
        const data = await response.json();
        this.namespaces = this.formatNamespaces(data.data);
      } catch (error) {
        console.error("Error fetching namespaces:", error);
      }
    },
    formatNamespaces(namespacesArray) {
      return namespacesArray.map(namespace => ({
        label: namespace.id, // Assuming 'id' is the namespace identifier
        value: namespace.id,
      }));
    },
    selectNamespace(namespace) {
      this.selectedNamespace = namespace;
      console.log("Selected namespace:", namespace);
    },
  },
  mounted() {
    this.fetchNamespaces(); // Fetch namespaces when the component is mounted
  },
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
</style>
