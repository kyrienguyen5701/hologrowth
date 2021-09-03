module.exports = {
  publicPath: "/",
  css: {
    loaderOptions: {
      sass: {
        additionalData: `
        @import "~@/assets/css/fonts.scss";
        @import "~@/assets/css/base.scss";
        `
      }
    }
  },
  configureWebpack: {
    devtool: "source-map"
  }
};
