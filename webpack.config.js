var path = require('path');

module.exports = {
    entry: {
     store: "./product/static/js/apps/store/store.js",
    },
    output: {
        filename: '[name].js',
        path: __dirname + '/product/static/dist/js'
    },
    resolve: {
        alias: {
            // 'vue$': 'vue/dist/vue.esm.js',
            'vue': 'vue/dist/vue.min.js',
            '@': path.resolve('./product/static'),
        },
        extensions: ['*', '.js', '.vue', '.json']
      },
    module:{
        rules:[
            // {
            //     test: /\.vue$/,
            //     loader: 'vue-loader'
            // },
            // // this will apply to both plain `.js` files
            // // AND `<script>` blocks in `.vue` files
            // {
            //     test: /\.js$/,
            //     loader: 'babel-loader'
            // },
            {
                test: /\.css$/,
                use:[
                    'style-loader',
                    'css-loader'
                ]
            }
        ]
    }
};