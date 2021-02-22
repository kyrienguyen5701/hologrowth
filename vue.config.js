module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "/hologrowth/" : "",
  css: {
    loaderOptions: {
      sass: {
        prependData: `
        @import "~@/assets/css/base.scss";
        `
      }
    }
  }
};
