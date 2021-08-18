<template>
  <div class="menu-branch" v-bind:class="{ clicked: menuOpened }">
    <div class="menu-button" v-on:click="toggleMenu()">
      <div class="menu-button-inner open">
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="menu-button-inner close">
        <div class="line"></div>
        <div class="line"></div>
      </div>
    </div>
    <div
      class="branch"
      v-for="branchData in menuData"
      v-bind:key="branchData.branchName"
    >
      <div class="branch-name flex-centered h-100">
        <span>{{ branchData.branchName }}</span>
      </div>
      <div class="branch-gens">
        <div
          class="branch-gen"
          v-for="genData in branchData.branchGenData"
          v-bind:key="genData.genName"
        >
          <span class="gen-name">{{ genData.genName }}</span>
          <div class="gen-members">
            <div
              class="member flex-centered"
              v-for="memberData in genData.genMember"
              v-bind:key="memberData.memberName"
              v-on:click="setTalent(memberData.memberName)"
            >
              <span>{{ memberData.memberDisplayName }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
// import * as interfaces from "@/assets/ts/interfaces";
// import * as Localization from "@/assets/ts/localize";
import { Component, Emit, Vue } from "vue-property-decorator";
import talents from "@/assets/json/talents.json";
import { Categorize, GetTalentCSSName, GetYoutubeURL } from "@/assets/ts/common";
import * as Localization from "@/assets/ts/localize";
import {
  BranchMenuData,
  DataType,
  GenMenuData,
  MemberMenuData,
  TalentData
} from "@/assets/ts/interfaces";
import * as Colors from "@/assets/ts/colors";

@Component
export default class BranchMenu extends Vue {
  data() {
    return {
      menuData: ((): BranchMenuData[] => {
        const result = [];

        const talentByBranch = Categorize(
          talents as TalentData[],
          DataType.Branch
        );

        for (const [branch, talents] of Object.entries(talentByBranch)) {
          const branchData = {} as BranchMenuData;

          const genMenuData = [] as GenMenuData[];
          const talentByGen = Categorize(talents, DataType.GenNumber);

          for (const [gen, talents] of Object.entries(talentByGen)) {
            const genData = {} as GenMenuData;
            const memberMenuData = [] as MemberMenuData[];

            for (let i = 0; i < talents.length; i++) {
              const memberData = {} as MemberMenuData;
              memberData.memberName = talents[i].name.replaceAll(" ", "-");
              memberData.memberDisplayName = Localization.GetLocalizedText(
                `menu-${talents[i].name.toLowerCase().replaceAll(" ", "-")}`
              );
              memberData.memberURL = GetYoutubeURL(talents[i].channelId);

              memberMenuData.push(memberData);
            }

            genData.genName = Localization.GetLocalizedText(
              `menu-${branch}-gen-${gen.toLowerCase().replaceAll(" ", "-")}`
            );
            genData.genMember = memberMenuData;

            genMenuData.push(genData);
          }

          branchData.branchName = Localization.GetLocalizedText(
            `menu-${branch}`
          );
          branchData.branchGenData = genMenuData;
          result.push(branchData);
        }

        return result;
      })(),
      selectedMember: "",
      menuOpened: false
    };
  }

  toggleMenu() {
    this.$data.menuOpened = !this.$data.menuOpened;
  }

  @Emit("setTalent")
  setTalent(memberName: string) {
    this.$data.selectedMember = memberName;
    const talentName = GetTalentCSSName(memberName);
    Colors.ChangeColor(talentName);
  }
}
</script>

<style lang="scss" scoped>
.menu-button {
  display: none;
}
.menu-branch {
  @extend %flex;
  z-index: 99;

  .branch {
    cursor: pointer;
    width: 100px;
    margin: 0px 10px;

    &:hover {
      background: var(--color-current-shade-25);

      .branch-gens {
        display: block;
        padding-top: 5px;
      }
    }

    .branch-gens {
      display: none;
      width: 220px;
    }

    .gen-members {
      width: fit-content;
      height: fit-content;
      display: none;
    }

    .branch-gen {
      @extend %flex;
      height: 40px;
      margin: 5px 0;

      &:first-child {
        margin-top: 0;
      }

      .gen-name {
        min-width: 220px;
        height: 40px;
        background: var(--color-current);
        padding: 5px 0px;
      }

      &:hover {
        .gen-members {
          display: block;
        }
      }

      .member {
        background: var(--color-current);
        width: 220px;
        height: 40px;
        margin: 0 0 5px 5px;
        display: flex;

        &:hover {
          background: var(--color-current-shade-25);
        }
      }
    }
  }
}
</style>
<style lang="scss" scoped>
@media (max-width: 768px) {
  .menu-button {
    display: flex;
    position: fixed;
    top: 0;
    right: 0;
    width: 60px;
    height: 60px;

    &-inner {
      width: 30px;
      height: 30px;
      margin: auto;
      display: flex;
      flex-direction: column;

      &.open {
        display: flex;
      }
      &.close {
        display: none;
      }

      .line {
        background: var(--color-text);
        width: 100%;
        height: 3px;
        margin: auto;
      }
    }
  }
  .menu-branch {
    &.clicked {
      .branch {
        display: block;
      }

      .menu-button-inner {
        &.open {
          display: none;
        }
        &.close {
          display: flex;

          .line {
            width: 30px;
            position: absolute;
            top: 50%;
            &:nth-child(1) {
              transform: rotate(45deg);
            }
            &:nth-child(2) {
              transform: rotate(-45deg);
            }
          }
        }
      }
    }
    --padding-menu: 30px;
    flex-direction: column;
    width: 75%;
    margin-left: auto;
    margin-top: 5px;

    .branch {
      display: none;
      margin: 0;
      margin-bottom: 5px;
      width: 100%;

      &-name {
        background: var(--color-current);
        height: 40px !important;
        padding-right: var(--padding-menu);
        flex-direction: column;
        text-align: right;

        span {
          margin: auto 0;
        }
      }

      &:hover {
        background: none;
        .branch-gens {
          display: block;
        }
      }

      .branch-gens {
        width: 90%;
        margin-left: auto;
      }

      .gen-members {
        display: block;
        height: 0;
        margin-left: auto;
        margin-top: 2.5px;
        overflow: hidden;
        transition: all 0.1s ease;
      }

      .branch-gen {
        display: flex;
        height: initial;
        flex-direction: column;

        .gen-name {
          text-align: right;
          padding-right: var(--padding-menu);
        }

        &:hover {
          .gen-members {
            height: 100%;
          }
        }

        .member {
          margin: 0 0 2.5px 0;
          background: var(--color-current-tint-25);

          span {
            margin: auto 0 auto auto;
            padding-right: var(--padding-menu);
          }
        }
      }
    }
  }
}
@keyframes appear {
  0% {
    height: 0;
  }

  100% {
    height: 100%;
  }
}
</style>
