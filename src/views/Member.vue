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
            <div class="member-name">{{ getLocalizedMemberName() }}</div>
            <div class="member-description">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. In
              perferendis reiciendis nobis ab facilis nostrum ratione, unde
              architecto vero aut et pariatur velit explicabo officiis aspernatur
              maxime fugiat. Iure, optio.
            </div>
            <div class="member-link">
              <div v-for="link in $data.links" :key="link" class="link-logo">
                <a :href="link.destination" class="img-holder" target="_blank">
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
        <div class="member-content-more-info">
          <div class="more-info-images">
            <div class="more-info-avatar">
              <div class="img-holder">
                <img :src="getMemberAvatarURL()" />
              </div>
            </div>
            <div class="more-info-signature">
              <div class="img-holder">
                <img :src="getMemberSignatureURL('default')" />
              </div>
            </div>
          </div>
          <div class="more-info-text">
            <div v-for="info in moreInfo" :key="info.key" class="more-info">
              <div class="more-info-key">
                <div class="more-info-key-text">
                  {{ info.key }}
                </div>
              </div>
              <div class="more-info-value">
                <div class="more-info-value-text">
                  {{ info.value }}
                </div>
              </div>
            </div>
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
import talents from "@/assets/json/talents.json";
import { TalentBasicInfo } from "@/assets/ts/interfaces";
import { GetLocalizedText } from "@/assets/ts/localize";

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
      basicInfo: {} as TalentBasicInfo,
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
      ],
      officialBio: "",
      moreInfo: [] as Array<{ key: string; value: string }>
    };
  }

  @Watch("$route", { immediate: true, deep: true })
  onMemberChange() {
    this.$data.memberName = this.$route.params.talentName;
    const talentData = talents.find(talent => {
      return talent.name === this.getMemberName();
    })
    this.$data.basicInfo = talentData?.basicInfo;
    this.$data.links[0].destination = `https://www.youtube.com/channel/${talentData?.channelId}`;
    this.$data.links[1].destination = `https://twitter.com/${talentData?.twitter}`;
    this.$data.links[2].destination =
      localStorage.getItem("lang") == "en"
        ? talentData?.basicInfo.officialWebsiteEN
        : talentData?.basicInfo.officialWebsiteJP;
    this.$data.officialBio = talentData?.officialBio;

    let k: keyof TalentBasicInfo;
    for (k in talentData?.basicInfo) {
      const v = talentData?.basicInfo[k];
      this.$data.moreInfo.push({
        key: GetLocalizedText(k),
        value: GetLocalizedText(v || "")
      })
    }
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

  getLocalizedMemberName() {
    return GetLocalizedText(this.getMemberName());
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
    return Common.GetTalentCSSName(this.$data.memberName);
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
  }
}

.member-content-chart {
  margin: 30px 0;
  .member-chart {
    height: 520px;
  }
}

.member-content-more-info {
  margin-top: 20px;
  width: 80%;
  margin: auto;
  display: flex;

  .more-info-images {
    width: 30%;
    .more-info {
      &-avatar {
        img {
          border-radius: 50%;
          width: 200px;
          height: 200px;
        }
      }
      &-signature {
        img {
          width: 200px;
        }
      }
    }
  }
  .more-info-text {
    width: 70%;
    .more-info {
      display: flex;
      height: 50px;

      &-key {
        width: 50%;

        &-text {
          text-align: left;
        }
      }
      &-value {
        width: 50%;
        position: relative;
        display: flex;

        &:after {
          content: "";
          position: absolute;
          bottom: 0px;
          right: 0px;
          width: 150%;
          height: 3px;
          background: var(--color-current);
        }

        &-text {
          margin-top: auto;
          margin-left: auto;
        }
      }
    }
  }
}
</style>
