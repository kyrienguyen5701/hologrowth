<template>
  <div class="menu-branch">
    <div
      class="branch flex-centered"
      v-for="branchData in data"
      v-bind:key="branchData.branchName"
    >
      <div class="branch-name">
        {{ branchData.branchName }}
      </div>
      <div class="branch-gens">
        <div
          class="branch-gen"
          v-for="genData in branchData.branchGenData"
          v-bind:key="genData.genName"
        >
          <div class="gen-name">
            {{ genData.genName }}
          </div>
          <div class="gen-members">
            <div
              class="member"
              v-for="memberData in genData.genMember"
              v-bind:key="memberData.memberName"
            >
              {{ memberData.memberName }}
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
import { Component, Prop, Vue } from "vue-property-decorator";
import talents from "@/assets/json/talents.json";
import { Categorize, GetYoutubeURL } from "@/assets/ts/common";
import {
  BranchMenuData,
  DataType,
  GenMenuData,
  MemberMenuData,
  TalentData
} from "@/assets/ts/interfaces";

@Component
export default class BranchMenu extends Vue {
  @Prop() data!: BranchMenuData[];
  mounted() {
    this.data = [];

    const talentByBranch = Categorize(talents as TalentData[], DataType.Branch);

    for (const [branch, talents] of Object.entries(talentByBranch)) {
      const branchData = {} as BranchMenuData;

      const genMenuData = [] as GenMenuData[];
      const talentByGen = Categorize(talents, DataType.GenNumber);

      const genData = {} as GenMenuData;
      for (const [gen, talents] of Object.entries(talentByGen)) {
        const memberMenuData = [] as MemberMenuData[];

        for (let i = 0; i < talents.length; i++) {
          const memberData = {} as MemberMenuData;
          memberData.memberName = talents[i].name;
          memberData.memberURL = GetYoutubeURL(talents[i].channelId);

          memberMenuData.push(memberData);
        }

        genData.genName = gen;
        genData.genMember = memberMenuData;
      }

      branchData.branchName = branch;
      branchData.branchGenData = genMenuData;
      this.data.push(branchData);
    }

    console.log(this.data);
  }
}
</script>

<style lang="scss" scoped>
.menu-branch {
  @extend %flex;

  .branch {
    cursor: pointer;
    min-width: 100px;

    &:hover {
      background: var(--color-current-shade-25);

      > .talent-name {
        display: block;
      }
    }
  }
}
</style>
