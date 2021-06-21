<template>
  <div class="music-player">
    <div class="player-button" v-on:click="togglePlay()">
      <span>
        <svg
          class="icon"
          ref="iconPlay"
          height="50"
          width="50"
          viewBox="0 0 50 50"
        >
          <polygon points="10,5 40,25 10,45" />
        </svg>
        <svg
          class="icon"
          ref="iconPause"
          height="50"
          width="50"
          viewBox="0 0 50 50"
          style="display: none"
        >
          <rect x="10" y="5" width="10" height="40" />
          <rect x="30" y="5" width="10" height="40" />
        </svg>
      </span>
    </div>
    <div class="player-button" v-on:click="prevSong()">
      <span>
        <svg
          class="icon"
          ref="iconPrev"
          height="50"
          width="50"
          viewBox="0 0 50 50"
        >
          <polygon points="40,10 20,25 40,40" />
          <polygon points="25,10 5,25 25,40" />
        </svg>
      </span>
    </div>
    <div class="player-info flex-centered">
      <div class="player-text">
        <span class="inner">{{ getCurrentSongName() }}</span>
      </div>
      <div class="player-seek">
        <input class="slider" type="range" />
      </div>
    </div>
    <div class="player-button" v-on:click="nextSong()">
      <span>
        <svg
          class="icon"
          ref="iconNext"
          height="50"
          width="50"
          viewBox="0 0 50 50"
        >
          <polygon points="10,10 30,25 10,40" />
          <polygon points="25,10 45,25 25,40" />
        </svg>
      </span>
    </div>
    <div class="player-button volume">
      <span>
        <svg
          class="icon"
          ref="iconVolume"
          height="50"
          width="50"
          viewBox="-100 -100 712 712"
          enable-background="new 0 0 512 512"
        >
          <!-- <path
            d="m291.9,438.3l-144.2-112.4v-138.2l144.2-112.3v362.9 5.68434e-14zm-185.4-122.8h-54.3v-117.7h54.3v117.7zm194.7-300.2l-180.1,141.9h-89.5c-11.4,0-20.6,9.1-20.6,20.3v158.2c0,11.2 9.2,20.3 20.6,20.3h91.2l178.4,140.7c12.8,10.1 31.9,1.1 31.9-15.1v-451.2c0-16.2-19-25.3-31.9-15.1z"
          /> -->
          <path
            d="m291.9,438.3l-144.2-112.4v-138.2l144.2-112.3v362.9 5.68434e-14zm-185.4-122.8h-54.3v-117.7h54.3v117.7z"
          />
          <path
            d="m394.7,143.2c-6.8-9-19.7-10.8-28.8-4.2-9.1,6.7-11,19.4-4.2,28.4 36.6,48.4 36.6,130.3 0,178.7-6.8,9-5,21.8 4.2,28.4 11.7,8.3 24.8,1.2 28.8-4.2 48.1-63.6 48.1-163.4 0-227.1z"
          />
          <path
            d="m444.8,76.8c-6.8-9-19.7-10.9-28.8-4.2-9.1,6.7-11,19.4-4.2,28.4 64.8,85.9 64.8,225.6 0,311.5-6.8,9-5.1,21.9 4.2,28.4 11.4,7.9 24.8,1.2 28.8-4.2 74.9-99.1 74.9-260.6 0-359.9v-1.42109e-14z"
          />
        </svg>
      </span>
      <div class="player-volume-container">
        <input
          id="player-volume"
          class="slider"
          orient="vertical"
          type="range"
          step="0.5"
          min="0"
          max="100"
          :value="100"
          @change="volumeChange()"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { SongData } from "@/assets/ts/interfaces";
import * as Localization from "@/assets/ts/localize";
import songData from "@/assets/json/songs.json";

@Component
export default class MusicPlayer extends Vue {
  songList = () => {
    const res = Array<string>();
    const r = require.context("@/assets/sounds/solo/Hoshimachi Suisei/", false);
    r.keys().forEach((path: string) => res.push(r(path)));
    return res;
  };
  isPlaying = true;
  currentSongIndex = 0;
  
  get currentAudio(): HTMLAudioElement {
    const songPath = this.songList()[this.currentSongIndex];
    console.log(songPath)
    return new Audio(songPath);
  }

  set currentAudio(value: HTMLAudioElement) {
    value.play();
  }

  get currentSong(): string {
    const originalPathSegments = this.songList()[this.currentSongIndex].split("/")[1].split(".");
    const originPath = `${originalPathSegments[0]}.${originalPathSegments[2]}`;
    const data = Object.entries(songData).find(kv => kv[1].path === originPath);
    if (data) {
      return data[0];
    }
    return '';
  }

  togglePlay() {
    if (this.isPlaying) {
      (this.$refs["iconPlay"] as HTMLElement).style.display = "none";
      (this.$refs["iconPause"] as HTMLElement).style.display = "block";
      this.currentAudio.pause();
    } else {
      (this.$refs["iconPlay"] as HTMLElement).style.display = "block";
      (this.$refs["iconPause"] as HTMLElement).style.display = "none";
      this.currentAudio.play();
    }
    this.isPlaying = !this.isPlaying;
  }

  getCurrentSongName(): string {
    const name = this.currentSong;
    return Localization.GetLocalizedSong(`${name}`);
  }

  prevSong() {
    this.currentAudio.pause();
    this.currentSongIndex === 0 
      ? this.currentSongIndex = this.songList().length 
      : this.currentSongIndex;
    this.currentSongIndex--;
    this.currentAudio.play();
    console.log("Prev");
  }

  nextSong() {
    this.currentAudio.pause();
    this.currentSongIndex === this.songList().length - 1 
      ? this.currentSongIndex = -1 
      : this.currentSongIndex;
    this.currentSongIndex++;
    this.currentAudio.play();
    console.log("Next");
  }

  volumeChange() {
    const value = Number((document.getElementById('player-volume') as HTMLInputElement).value) / 100;
    this.currentAudio.volume = value;
    localStorage.setItem('player-volume', String(value));
  }
}
</script>

<style lang="scss" scoped>
input.slider {
  width: 100%;
  -webkit-appearance: none;
  appearance: none;
  outline: none;

  &::-webkit-slider-runnable-track {
    background: white;
    height: 8px;
  }

  &::-webkit-slider-thumb {
    background: var(--color-current-complement);
    margin-top: -3px;
    -webkit-appearance: none;
    appearance: none;
    width: 10px;
    height: 14px;
  }
}

.music-player {
  position: fixed;
  bottom: 50px;
  right: 75px;
  display: flex;

  svg {
    width: 40px;
    height: 40px;

    &.icon {
      fill: var(--color-text);
    }
  }

  .player-button {
    background: var(--color-current);
    cursor: pointer;

    &:hover {
      background: var(--color-text);

      svg.icon {
        fill: var(--color-current);
      }
    }
  }

  .player-info {
    width: 200px;
    height: 40px;
    background: var(--color-current);
    color: var(--color-text);
    overflow: hidden;
    padding: 0 10px;

    &:hover {
      .player-seek {
        display: block;
      }
      .player-text {
        display: none;
      }
    }

    .player-text {
      animation: move 5s infinite;
      animation-timing-function: linear;

      .inner {
        white-space: nowrap;
      }
    }

    .player-seek {
      display: none;
      width: 100%;
      padding: 0 5px 0 10px;
      line-height: 0;

      input.slider {
        height: 40px;
        background: var(--color-current);
      }
    }
  }

  .player-button {
    &.volume {
      &:hover {
        .player-volume-container {
          display: block;
        }
      }
    }
  }

  .player-volume-container {
    display: none;
    position: absolute;
    right: 0;
    bottom: 0;
    line-height: 0;
    z-index: -1;

    input {
      height: 40px;
      width: 200px;
      background: var(--color-current);
      outline: none;
      transform: rotate(90deg);
      transform-origin: 100% 0%;
      padding: 15px;
    }
  }
}

@keyframes move {
  0% {
    transform: translateX(0%);
  }
  32% {
    opacity: 1;
  }
  33% {
    transform: translateX(-100%);
    opacity: 0;
  }
  66% {
    transform: translateX(100%);
    opacity: 0;
  }
  67% {
    opacity: 1;
  }
  100% {
    transform: translateX(0%);
  }
}
</style>
