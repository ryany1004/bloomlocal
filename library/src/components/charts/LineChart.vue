<script>
import {Line, mixins} from 'vue-chartjs'
const {reactiveProp} = mixins;

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: {
    chartData: {
      type: Object,
      default: null,
    },
    options: {
      type: Object,
      default: null
    }
  },
  watch: {
    // chartData: {
    //   handler: function (val) {
    //     if (val) {
    //       let gradient = this.$refs.canvas.getContext('2d').createLinearGradient(0, 0, 0, 450)
    //       gradient.addColorStop(0, 'rgba(74, 217, 145, 0.148239)')
    //       gradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.176942)');
    //
    //       val.datasets.forEach(function (dataset) {
    //         dataset.borderColor = '#4AD991';
    //         dataset.pointBackgroundColor = 'white';
    //         dataset.borderWidth = 1;
    //         dataset.pointBorderColor = 'white';
    //         dataset.backgroundColor = this.gradient;
    //       })
    //     }
    //   },
    //   immediate: true
    // }
  },
  data() {
    return {
     htmlLegend: null
    }
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>
