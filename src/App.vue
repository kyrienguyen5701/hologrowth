<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/tests-color">Color Test</router-link>
      <div class="color-change">
        <button v-on:click="SetColor('fubuki')">Change color: FBK</button>
        <button v-on:click="SetColor('sora')">Change color: Sora</button>
      </div>
    </div>
    <router-view />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import VueRouter from "vue-router";
import AboutVue from "./views/About.vue";
import Home from "./views/Home.vue";
import Color from "./views/tests/Color.vue";

import * as Colors from "./assets/ts/colors";

const routes = [
  { path: "/", component: Home },
  { path: "/about", component: AboutVue },
  { path: "/tests-color", component: Color }
];

const router = new VueRouter({
  routes
});

export default Vue.extend({
  router: router,
  methods: {
    SetColor(name: string) {
      Colors.ChangeColor(name);
    }
  }
});
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
