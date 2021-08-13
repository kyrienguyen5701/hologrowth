<template>
  <div id="app">
    <div id="navbar">
      <div class="logo p-10 flex-centered">
        <div class="logo-text">
          <a href="/">Hologrowth</a>
        </div>
      </div>
      <div class="menus">
        <BranchMenu
          :key="currentLang"
          v-on:setTalent="changeTalent($event)"
        ></BranchMenu>
        <LanguageMenu v-on:setLang="changeLang($event)"></LanguageMenu>
      </div>
    </div>
    <div class="content">
      <router-view :key="currentLang" />
    </div>
    <MusicPlayer v-bind:currentLang="currentLang"></MusicPlayer>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import router from "./router/index";
import * as Colors from "./assets/ts/colors";

export default Vue.extend({
  router: router,
  methods: {
    changeColor(name: string) {
      Colors.ChangeColor(name);
    },
    changeLang(value: string) {
      this.currentLang = value;
    },
    changeTalent(talentName: string) {
      router.push(`/member/${talentName}`);
    }
  },
  data() {
    return {
      currentLang: localStorage.getItem("lang")
    };
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
  position: fixed;
  top: 0;
  width: 100%;
  box-shadow: 0px 0px 10px var(--color-current-shade-50);
  background: var(--color-current);
  color: var(--color-text);
  height: 80px;
  z-index: 100;
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
      font-size: 2rem;
    }
  }

  .menus {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
}
.content {
  margin-top: 80px;
}
</style>
<style lang="scss" scoped>
@media (max-width: 600px) {
  .content {
    margin-top: 60px;
    margin-bottom: 40px;
  }

  #navbar {
    height: 60px;

    .logo {
      width: 100%;
      display: flex;

      a {
        margin: auto;
        font-size: 1.25rem;
      }
    }

    .menus {
      position: absolute;
      top: 60px;
      flex-direction: column;
    }
  }
}
</style>