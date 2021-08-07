<template>
  <div class="member-page" :key="$data.memberName">
    <div class="member-banner">
      <img :src="getMemberBannerURL()" />
    </div>
    <div class="member-background">
      <div class="overlay"></div>
      <div class="member-background-col" v-for="i in $data.background.nCol" :key="i">
        <div class="img-holder" v-for="j in $data.background.nRow" :key="j" style="width: 250px">
          <img v-if="i % 2 == 0 && j % 2 == 0" :src="getMemberSignatureURL('random')" />
          <img v-if="i % 2 == 0 && j % 2 != 0" :src="getMemberIconURL()" :height="250 / 3"/>
          <img v-if="i % 2 != 0 && j % 2 != 0" :src="getMemberSignatureURL('random')" />
          <img v-if="i % 2 != 0 && j % 2 == 0" :src="getMemberIconURL()" :height="250 / 3"/>
        </div>
      </div>
    </div>
    <div class="member-content">
      <div class="member-content-section">
        <div class="member-content-info">
          <div class="member-content-info-avatar">
            <div class="img-holder">
              <img :src="getMemberAvatarURL()" />
            </div>
          </div>
          <div class="member-content-info-info">
            <div class="member-name">{{ getMemberName() }}</div>
            <div class="member-description">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. In
              perferendis reiciendis nobis ab facilis nostrum ratione, unde
              architecto vero aut et pariatur velit explicabo officiis aspernatur
              maxime fugiat. Iure, optio.
            </div>
            <div class="member-link">
              <div v-for="link in $data.links" :key="link" class="link-logo">
                <a :href="link.destination" class="img-holder">
                  <img :src="getLinkTypeURL(link.type)" />
                </a>
              </div>
            </div>
          </div>
        </div>
        <div class="member-content-chart">
          <div class="member-chart">
            <ChartSwiper
              v-bind:memberData="{
                name: getMemberName(),
                CSSname: getMemberCSSName()
              }"
            ></ChartSwiper>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import Stats from "@/components/Stats.vue";
import * as Common from "@/assets/ts/common";

@Component({
  components: {
    Stats
  }
})
export default class MemberPage extends Vue {
  data() {
    return {
      memberName: this.$route.params.talentName,
      background: {
        nCol: Math.round(window.innerWidth / 250),
        nRow: Math.round(window.innerHeight / 250)
      },
      links: [
        {
          type: "youtube",
          destination: ""
        },
        {
          type: "twitter",
          destination: ""
        },
        {
          type: "hololive",
          destination: ""
        }
      ]
    };
  }

  @Watch("$route")
  onMemberChange() {
    this.$data.memberName = this.$route.params.talentName;
  }

  mounted() {
    // this.createSignatureIconBackground();
  }

  getMemberBannerURL() {
    return require(`@/assets/talentBanners/default/${this.getMemberName()}_2560 x 423.png`);
  }

  getMemberIconURL() {
    try {
      return require(`@/assets/talentIcons/default/${this.getMemberName()}.svg`);
    } catch {
      return "";
    }
  }

  getMemberAvatarURL() {
    try {
      return require(`@/assets/talentAvatars/medium/${this.getMemberName()}.png`);
    } catch {
      return "";
    }
  }

  getMemberName() {
    return Common.GetTalentName(this.$data.memberName);
  }

  getMemberSignatureURL(res: string) {
    if (res == undefined) res = "default";
    if (res == "random") {
      const arr = ["high", "medium", "default"];
      res = arr[Math.floor(Math.random() * arr.length)];
    }
    try {
      return require(`@/assets/talentSignatures/${res}/${this.getMemberName()}.png`);
    } catch {
      return "";
    }
  }

  getMemberCSSName() {
    return this.$data.memberName.split("-")[1];
  }

  getLinkTypeURL(linkType: string) {
    try {
      return require(`@/assets/logos/${linkType}.png`);
    } catch {
      return "";
    }
  }
}
</script>

<style lang="scss" scoped>
.member-banner {
  img {
    width: 100%;
  }
  border-bottom: 10px solid var(--color-current);
}
.member-background {
  position: fixed;
  top: 0;
  height: 100vh;
  width: 100vw;
  z-index: -1;
  display: flex;

  .overlay {
    position: absolute;
    width: 100%;
    height: 100%;
    background: var(--color-current);
    opacity: 0.3;
  }

  &-col {
    display: flex;
    flex-direction: column;

    .img-holder {
      margin: auto;
      display: flex;

      img {
        margin: auto;
        transform: rotate(-45deg);
      }
    }
  }
}
.member-content {
  display: flex;

  &-section {
    width: 70%;
    padding: 20px 0px;
    margin: auto;
    background: white;
    border: 10px solid var(--color-current);
    border-top: 0;
    border-bottom: 0;
  }

  .member-content {
    &-info {
      display: flex;
      flex-direction: row-reverse;
      margin-bottom: 40px;

      &-avatar {
        width: 20%;
        display: flex;

        .img-holder {
          width: 80%;
          margin: auto;

          img {
            width: 100%;
            border: 5px solid var(--color-current);
            border-radius: 50%;
          }
        }
      }

      &-info {
        width: 80%;
        text-align: right;
        padding-left: 20px;

        .member {
          &-name {
            color: var(--color-current);
            font-size: 300%;
          }

          &-description {
            position: relative;
            padding-bottom: 10px;

            &:after {
              content: "";
              width: 70%;
              position: absolute;
              bottom: 0;
              right: 0;
              height: 5px;
              background: var(--color-current);
            }
          }

          &-link {
            margin-top: 5px;
            display: flex;
            flex-direction: row-reverse;

            .link-logo {
              margin: 5px;

              .img-holder {
                width: 50px;
                height: 50px;
                display: flex;

                img {
                  margin: auto;
                  max-width: 50px;
                  height: 100%;
                }
              }
            }
          }
        }
      }
    }

    &-chart {
      .member-chart {
        cursor: pointer;
      }
    }
  }
}

.member-chart {
  height: 100vh;
}
</style>
