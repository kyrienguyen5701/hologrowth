import "@babel/polyfill";
import "mutationobserver-shim";
import Vue from "vue";
import "./plugins/bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import BranchMenu from "./components/BranchMenu.vue";
import LanguageMenu from "./components/LanguageMenu.vue";
import MemberChart from "./components/MemberChart.vue";
import HoloChart from "./components/HoloChart.vue";
import ChartSwiper from "./components/ChartSwiper.vue";
import MusicPlayer from "./components/MusicPlayer.vue";

Vue.config.productionTip = false;

Vue.component("BranchMenu", BranchMenu);
Vue.component("LanguageMenu", LanguageMenu);
Vue.component("MemberChart", MemberChart);
Vue.component("HoloChart", HoloChart);
Vue.component("ChartSwiper", ChartSwiper);
Vue.component("MusicPlayer", MusicPlayer);

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
