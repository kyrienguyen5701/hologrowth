module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "/hologrowth/" : "",
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
