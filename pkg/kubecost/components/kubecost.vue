<script>
import Loading from '@shell/components/Loading';
import LabelValue from '@shell/components/LabelValue';
import { mapGetters } from 'vuex';
import { getKubecostData } from '../kubecostModule';
import PieChart from './pie.vue';

export default {
  name: 'RunningCosts',

  components: {
    Loading, LabelValue, PieChart
  },

  props: {
    resource: {
      type:     Object,
      required: true,
    }
  },

  async fetch() {
    if (this.resource.kind === 'Cluster') {
      // for cluster dashboard card
      this.costs = await getKubecostData({
        aggregate: 'cluster',
        window:    'month',
        clusterId: this.clusterId,
        ctx:       this
      });
    } else {
      // namespace tab
      this.costs = await getKubecostData({
        aggregate:       'namespace',
        window:          'month',
        targetNamespace: this.resource.id,
        clusterId:       this.clusterId,
        ctx:             this
      });
    }
  },
  watch: {
    $route: {
      handler(neu) {
        if (neu.hash && neu.hash.includes('#Kubecost')) {
          this.key = this.generateString(10);
        }
      },
      deep: true
    }
  },

  data() {
    return { costs: undefined, key: this.generateString(10) };
  },

  computed: {
    ...mapGetters(['clusterId']),

    info() {
      if (this.costs?.type && this.costs?.msg) {
        return this.costs;
      }

      return null;
    }
  },

  methods: {
    generateString(length) {
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

      let result = ' ';
      const charactersLength = characters.length;

      for ( let i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
      }

      return result;
    }
  }
};
</script>

<template>
  <div class="main">
    <Loading
      v-if="$fetchState.pending"
      mode="relative"
    />
    <div v-else class="main-content">
      <h3 class="mb-40">
        {{ t('kubecost.title') }}
      </h3>
     
    
      <PieChart
        v-if="costs.length"
        :key="key"
        :costs="costs"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.main-content {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;

  h3 {
    text-align: center;
  }

  .label-values {
    display: flex;
    flex-direction: row;

    .label-value {
      padding-right: 20px;
    }
  }
}
</style>
