const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  // other options...
  module: {
    rules: [
      // ... other rules omitted
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      }
    ]
  },
  plugins: [
    // ... Vue Loader plugin omitted
    new MiniCssExtractPlugin({
      filename: 'bloomLib.css'
    })
  ]
}
