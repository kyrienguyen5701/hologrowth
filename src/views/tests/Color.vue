<template>
  <div>
    <div class="color-text">
      <div class="color-default">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="color-tint-25">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="color-tint-50">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="color-shade-25">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="color-shade-50">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="color-complement">
        The quick brown fox jumps over the lazy dog.
      </div>
    </div>
    <div class="color-bg">
      <div class="bg-default">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="bg-tint-25">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="bg-tint-50">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="bg-shade-25">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="bg-shade-50">
        The quick brown fox jumps over the lazy dog.
      </div>
      <div class="bg-complement">
        The quick brown fox jumps over the lazy dog.
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default class Color extends Vue {}
</script>

<style lang="scss" scoped>
div {
  padding: 10px;
}
.color-text {
  div {
    cursor: pointer;
  }
}
.color-bg {
  div {
    color: #fff;
  }
}
</style>
