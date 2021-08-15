<template>
  <div class="member-page" :key="memberName">
    <div class="member-banner">
      <img :src="getMemberBannerURL()" :lazy="getMemberBannerURL(true)" />
    </div>
    <div class="member-background">
      <div class="overlay"></div>
      <div
        class="member-background-col"
        v-for="i in background.nCol"
        :key="`col-${i}`"
      >
        <div
          class="img-holder"
          v-for="j in background.nRow"
          :key="`row-${j}`"
          style="width: 250px"
        >
          <img
            v-if="i % 2 == 0 && j % 2 == 0"
            :src="getMemberSignatureURL('random')"
          />
          <img
            v-if="i % 2 == 0 && j % 2 != 0"
            :src="getMemberIconURL()"
            :height="250 / 3"
          />
          <img
            v-if="i % 2 != 0 && j % 2 != 0"
            :src="getMemberSignatureURL('random')"
          />
          <img
            v-if="i % 2 != 0 && j % 2 == 0"
            :src="getMemberIconURL()"
            :height="250 / 3"
          />
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
              {{ getLocalizedMemberBio() }}
            </div>
            <div class="member-link">
              <div v-for="link in links" :key="link.type" class="link-logo">
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
            <div class="more-info-title">
              <div class="title-text">
                Basic Information
              </div>
            </div>
            <div class="more-info-banner">
              <div class="img-holder">
                <img :src="getMemberBannerURL('medium')" />
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
import { Component, Vue, Watch } from "vue-property-decorator";
import Stats from "@/components/Stats.vue";
import * as Common from "@/assets/ts/common";
import talents from "@/assets/json/talents.json";
import { TalentBasicInfo, TalentData } from "@/assets/ts/interfaces";
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
    this.$data.moreInfo = []; // reset info to avoid stacking when navigating within router
    this.$data.memberName = this.$route.params.talentName;
    const talentData = talents.find(talent => {
      return talent.name === this.getMemberName();
    }) as TalentData;
    this.$data.basicInfo = talentData.basicInfo;
    this.$data.links[0].destination = `https://www.youtube.com/channel/${talentData.channelId}`;
    this.$data.links[1].destination = `https://twitter.com/${talentData.twitter}`;
    this.$data.links[2].destination =
      localStorage.getItem("lang") == "en"
        ? talentData.officialWebsiteEN
        : talentData.officialWebsiteJP;
    this.$data.officialBio = talentData.officialBio;

    let k: keyof TalentBasicInfo;
    for (k in talentData.basicInfo) {
      if (!k.includes("officialWebsite")) {
        const v = talentData.basicInfo[k];
        this.$data.moreInfo.push({
          key: GetLocalizedText(k),
          value: GetLocalizedText(v || "")
        });
      }
    }
  }

  getMemberBannerURL(placeholder = false, res = "default") {
    let size = placeholder ? "1138 x 188" : "2560 x 423";
    switch (res) {
      case "medium":
        size = placeholder ? "320 x 52" : "640 x 105";
        break;
    }
    try {
      return require(`@/assets/talentBanners/${res}/${this.getMemberName()}_${size}.png`);
    } catch {
      return "";
    }
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

  getLocalizedMemberBio() {
    return GetLocalizedText(this.$data.officialBio);
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
        width: 90%;
        text-align: right;
        padding-left: 40px;
        padding-right: 10px;

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
  width: 90%;
  margin: auto;
  display: flex;

  .more-info-images {
    width: 30%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    margin: 5px 0;

    .more-info {
      &-title {
        .title {
          &-member {
            font-size: 2rem;
            color: var(--color-current);
          }
          &-text {
            font-size: 1.5rem;
            color: var(--color-current-complement);
          }
        }
      }
      &-banner {
        .img-holder {
          img {
            width: 100%;
          }
        }
      }
    }
  }
  .more-info-text {
    width: 70%;
    margin-left: 20px;
    .more-info {
      display: flex;
      height: 50px;
      margin: 5px 0;

      &-key {
        width: 50%;
        position: relative;
        display: flex;

        &:before {
          content: "";
          position: absolute;
          bottom: 0px;
          left: 0px;
          height: 80%;
          background: var(--color-current);
          border-radius: 0 100px 0 0;
        }
        &:after {
          content: "";
          position: absolute;
          bottom: 0px;
          left: 0px;
          width: 200%;
          height: 5px;
          background: var(--color-current);
        }

        &-text {
          margin-top: auto;
          text-align: left;
          padding-left: 15px;
          z-index: 1;
        }
      }

      &-value {
        width: 50%;
        position: relative;
        display: flex;

        &-text {
          margin-top: auto;
          margin-left: auto;
          padding-right: 15px;
          z-index: 1;
        }
      }

      @for $i from 1 to 6 {
        &:nth-child(#{$i}) .more-info-key:before {
          width: percentage($i * 0.3);
        }
      }
    }
  }
}
</style>
<style lang="scss" scoped>
@media (max-width: 600px) {
  .member {
    &-background {
      &-col {
        display: none;
      }
    }

    &-content {
      &-section {
        margin: 0;
        width: 100%;
        border: none;
      }

      .member-content {
        &-info {
          flex-direction: column;
          &-avatar {
            width: 60%;
            margin: auto;
          }
          &-info {
            width: 100%;
            text-align: center;
            padding: 0px 15px;

            .member-name {
              line-height: 1.5;
            }

            .member-description {
              &:after {
                right: 15%;
              }
            }

            .member-link {
              .link-logo {
                &:first-child {
                  margin-right: auto;
                }
                &:last-child {
                  margin-left: auto;
                }
              }
            }
          }
        }
      }

      &-more-info {
        .more-info {
          &-images {
            display: none;
          }
          &-text {
            width: 100%;
            margin: 0px;

            .more-info {
              &-key {
                &-text {
                  padding-left: 10px;
                }
              }
              &-value {
                &-text {
                  padding-right: 10px;
                }
              }
            }
          }
        }
      }
    }
  }
}
</style>
