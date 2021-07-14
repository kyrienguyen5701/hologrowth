<template>
  <div class="menu-branch">
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
import { Categorize, GetYoutubeURL } from "@/assets/ts/common";
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
              memberData.memberName = talents[i].name
                .replaceAll(" ", "-")
                .toLowerCase();
              memberData.memberDisplayName = Localization.GetLocalizedText(
                `menu-${talents[i].name.replaceAll(" ", "-").toLowerCase()}`
              );
              memberData.memberURL = GetYoutubeURL(talents[i].channelId);

              memberMenuData.push(memberData);
            }

            genData.genName = Localization.GetLocalizedText(
              `menu-${branch}-gen-${gen}`
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
      selectedMember: ""
    };
  }

  @Emit("setTalent")
  setTalent(memberName: string) {
    this.$data.selectedMember = memberName;
    Colors.ChangeColor(memberName.split("-")[1]);
  }
}
</script>

<style lang="scss" scoped>
.menu-branch {
  @extend %flex;
  z-index: 99;

  .branch {
    cursor: pointer;
    width: 100px;

    &:hover {
      background: var(--color-current-shade-25);

      .branch-gens {
        display: block;
        padding-top: 5px;
      }
    }

    .branch-gens {
      display: none;
      width: 150px;
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
        min-width: 150px;
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
        width: 200px;
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
