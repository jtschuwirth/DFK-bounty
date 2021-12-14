var gulp = require('gulp');
var fs = require("fs");
var browserify = require("browserify");
gulp.task('default', function () {
    browserify("src/js/main.js")
        .transform("babelify", {presets: ["@babel/preset-env", "@babel/preset-react"], "plugins": ["@babel/plugin-transform-runtime"]})
        .bundle()
        .pipe(fs.createWriteStream("build/bundle.js"));
});

