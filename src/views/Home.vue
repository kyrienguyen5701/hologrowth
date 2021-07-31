<template>
  <div class="home">
    <div class="sidebar">
      <div class="searchbar">
        <input type="text" />
      </div>
      <div class="members">
        <div class="member" v-for="mem in members" :key="mem.name">
          <div class="member-banner">
            <div class="overlay"></div>
            <img :src="mem.banner" width="320" height="105" :alt="mem.name" />
          </div>
          <div class="member-avatar">
            <img :src="mem.avatar" :alt="mem.name" />
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
import Member from "@/components/MemberHome.vue";
import Stats from "@/components/Stats.vue";
import { TalentAvatar }  from "@/assets/ts/interfaces";
import talents from "@/assets/json/talents.json";

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
        const res = Array<TalentAvatar>();
        talents.forEach(talent => {
          res.push({
            name: talent.name,
            avatar: require(`@/assets/talentAvatars/medium/${talent.name}.png`),
            banner: require(`@/assets/talentBanners/medium/${talent.name}_320 x 52.png`)
          });
        });
        return res;
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
    max-width: 320px;
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
        position: relative;
        height: 105px;

        &:hover {
          cursor: pointer;
          background: mix(black, $bg_sidebar, 25);
          &-avatar {
            background: black;
          }
          .member-banner {
            .overlay {
              opacity: 0;
            }
          }
          .member-avatar {
            opacity: 1;
          }
        }

        &-banner {
          position: relative;
          .overlay {
            position: absolute;
            width: 100%;
            height: 100%;
            background: white;
            opacity: 0.6;
            transition: all 0.75s ease;
          }
        }

        &-avatar {
          background: white;
          position: absolute;
          right: 0;
          bottom: 0;
          border-radius: 50%;
          border: 1px solid var(--color-current);
          padding: 4px;
          opacity: 0;
          transition: all 0.5s ease;
          img {
            border: 1px solid var(--color-current);
            height: 40px;
            width: 40px;
            border-radius: 50%;
          }
        }

        &-banner {
          display: flex;
          height: 100%;

          img {
            height: 100%;
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
