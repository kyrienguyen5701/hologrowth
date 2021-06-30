<template>
  <div class="home">
    <div class="sidebar">
      <div class="searchbar">
        <input type="text" />
      </div>
      <div class="members">
        <div class="member" v-for="mem in members" :key="mem.name">
          <div class="member-avatar">
            <img :src="mem.avatar" alt="" />
          </div>
        </div>
      </div>
    </div>
    <div class="chart flex-centered">
      <div class="col-11">
        <!-- replace this chart -->
        <MemberChart v-bind:memberData="{name: 'Hoshimachi Suisei', CSSname: 'suisei'}"></MemberChart>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import Member from "@/components/MemberHome.vue"; // @ is an alias to /src
import Stats from "@/components/Stats.vue";

@Component({
  components: {
    Member,
    Stats
  }
})
export default class Home extends Vue {
  data() {
    return {
      members: (() => {
        return [
          {
            name: "fubuki",
            avatar: require("@/assets/talentAvatars/medium/fubuki.png")
          },
          {
            name: "sora",
            avatar: require("@/assets/talentAvatars/medium/sora.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          },
          {
            name: "suisei",
            avatar: require("@/assets/talentAvatars/medium/suisei.png")
          }
        ];
      })()
    };
  }
}
</script>

<style lang="scss" scoped>
$bg_sidebar: #ccc;
.home {
  display: flex;
  .sidebar {
    min-width: 100px;
    background: $bg_sidebar;

    .searchbar {
      padding: 10px;
      input {
        width: 100%;
        text-align: center;
      }
    }

    .members {
      height: calc(90vh - 100px);
      overflow-y: scroll;
      &::-webkit-scrollbar {
        display: none;
      }
      scrollbar-width: none;

      .member {
        padding: 10px 0;

        &:hover {
          cursor: pointer;
          background: mix(black, $bg_sidebar, 25);
        }

        &-avatar {
          img {
            width: 50px;
            height: 50px;
            border-radius: 50%;
          }
        }
      }
    }
  }
  .chart {
    width: calc(100% - 100px);
  }
}
</style>
