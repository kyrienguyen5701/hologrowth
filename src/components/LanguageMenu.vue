<template>
  <div class="menu-language">
    <div class="language">
      <div class="language-text-short flex-centered w-100">
        <span>{{ getSelectedLangShort() }} </span>
      </div>
      <div class="language-text flex-centered w-100">
        <span>{{ getSelectedLang() }} </span>
      </div>
    </div>
    <div
      class="language"
      v-for="lang in languages"
      v-bind:key="lang"
      v-on:click="setLang(lang)"
    >
      <div class="language-text flex-centered w-100">
        <span>{{ getLangText(lang) }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Emit, Vue } from "vue-property-decorator";
import * as Localization from "@/assets/ts/localize";
import * as Config from "@/assets/ts/config";

@Component
export default class LanguageMenu extends Vue {
  data() {
    return {
      selectedLang: localStorage.getItem("lang")
        ? localStorage.getItem("lang")
        : "en",
      languages: (() => {
        const result = [];
        const languages = Config.GetConfig().languages;
        for (let i = 0; i < languages.length; i++) {
          result.push(languages[i]);
        }
        return result;
      })(),
      getLangText(langCode: string) {
        return Localization.GetLocalizedText(`lang-${langCode}`);
      },
      getSelectedLang() {
        return Localization.GetLocalizedText(`lang-${this.selectedLang}`);
      },
      getSelectedLangShort() {
        return this.selectedLang?.toUpperCase();
      }
    };
  }

  @Emit("setLang")
  setLang(lang: string) {
    this.$data.selectedLang = lang;
    Localization.SetLang(lang);
  }
}
</script>

<style lang="scss" scoped>
.menu-language {
  &:hover {
    .language {
      display: block;
    }
  }

  .language {
    cursor: pointer;
    display: none;
    min-width: 120px;

    &:first-child {
      height: 100%;
      display: flex;
      margin: auto;
    }

    &:not(:first-child) {
      padding-top: 5px;

      .language-text {
        height: 40px;
      }
    }

    .language-text {
      &-short {
        display: none;
      }
      padding: 0 25px;
      background: var(--color-current);

      &:hover {
        background: var(--color-current-shade-25);
      }
    }
  }
}
</style>
<style lang="scss" scoped>
@media (max-width: 768px) {
  .menu-language {
    position: absolute;

    .language {
      min-width: 90px;

      &:first-child {
        position: fixed;
        top: 0;
        height: 60px;

        .language-text {
          display: none;

          &-short {
            display: flex;
            width: 50px !important;
          }

          span {
            margin: auto;
          }
        }
      }

      &-text {
        padding: 0 !important;

        span {
          padding-left: 15px;
          margin-left: 0;
        }
      }
    }
  }
}
</style>
