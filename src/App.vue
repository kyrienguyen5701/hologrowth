<template>
  <div id="app">
    <div id="navbar">
      <div class="logo p-10 flex-centered">
        <div class="logo-text">
          <a href="/">Hologrowth</a>
        </div>
      </div>
      <div class="menus">
        <BranchMenu :key="currentLang"></BranchMenu>
        <LanguageMenu v-on:setLang="changeLang($event)"></LanguageMenu>
      </div>
    </div>
    <router-view />
    <div class="body">
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
      <router-link to="/member">Member</router-link>
      <router-link to="/tests-color">Color Test</router-link>
      <div class="color-change">
        <button v-on:click="SetColor('fubuki')">Change color: FBK</button>
        <button v-on:click="SetColor('sora')">Change color: Sora</button>
      </div>
    </div>
    <MusicPlayer v-bind:lang="currentLang"></MusicPlayer>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import router from "./router/index";
import * as Colors from "./assets/ts/colors";

export default Vue.extend({
  router: router,
  methods: {
    SetColor(name: string) {
      Colors.ChangeColor(name);
    },
    changeLang(value: string) {
      this.currentLang = value;
    }
  },
  data() {
    return {
      currentLang: localStorage.getItem("lang")
    }
  }
});
</script>

<style lang="scss">
#app {
  // -webkit-font-smoothing: antialiased;
  // -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

// div {
//   padding: 0 !important;
// }

#navbar {
  background: var(--color-current);
  color: var(--color-text);
  height: 80px;
  @extend %flex;

  a {
    color: #fff;

    &.router-link-exact-active {
      color: #fff;
    }
  }

  .logo {
    * > {
      margin: auto;
    }
    a {
      font-size: 1.5rem;
    }
  }

  .menus {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
}
</style>
