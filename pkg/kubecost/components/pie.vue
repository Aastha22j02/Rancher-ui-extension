<script>
import { Pie } from 'vue-chartjs/legacy';

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

export default {
  name:       'PieChart',
  components: { Pie },
  props:      {
    labels: {
      type:    Array,
      default: () => []
    },
    data: {
      type:    Array,
      default: () => []
    },
    backgroundColor: {
      type:    Array,
      default: () => []
    },
    costs: {
      type:    Array,
      default: () => []
    },
    chartId: {
      type:    String,
      default: 'pie-chart'
    },
    datasetIdKey: {
      type:    String,
      default: 'label'
    },
    width: {
      type:    Number,
      default: 400
    },
    height: {
      type:    Number,
      default: 400
    },
    cssClasses: {
      default: '',
      type:    String
    },
    styles: {
      type:    Object,
      default: () => {}
    },
    plugins: {
      type:    Array,
      default: () => []
    }
  },
  computed: {
    chartData() {
      let labels;
      let data;
      const backgroundColor = ['#FF0000', '#00FF00', '#0000FF', '#FFA500', '#FFFF00', '#4B0082'];

      if (this.costs.length) {
        labels = this.costs.filter(item => item.name !== 'Total').map(item => item.name);
        data = this.costs.filter(item => item.name !== 'Total').map(item => item.rawValue);
      }

      return {
        labels,
        datasets: [
          {
            backgroundColor,
            data,
          }
        ]
      };
    }
  },

  data() {
    return {
      chartOptions: {
        responsive:          true,
        maintainAspectRatio: false
      }
    };
  }
};
</script>

<template>
  <Pie
    class="custom-pie-chart"
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
  />
</template>

<style lang="scss" scoped>
.custom-pie-chart {
  margin-top: 40px;
}
</style>
