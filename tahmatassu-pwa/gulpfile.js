'use strict';
 
var path = require('path');
var gulp = require('gulp');
var sass = require('gulp-sass');
var htmlmin = require('gulp-htmlmin');
var sourcemaps = require('gulp-sourcemaps');
var browserSync = require('browser-sync').create();

//Handlebars
var gulphandlebars = require('gulp-handlebars');

var wrap = require('gulp-wrap');
var declare = require('gulp-declare');
var concat = require('gulp-concat');

var gulp = require('gulp');
var gulpWebpack = require('gulp-webpack');

var webpack = require('webpack');
var gulp = require('gulp');
var clean = require('gulp-clean');
 
const Uglify = require("uglifyjs-webpack-plugin");


gulp.task('clean', function () {
    return gulp.src('dist', {read: false})
        .pipe(clean());
});

gulp.task('webpack', function() {
  return gulp.src('src/index.js')
    .pipe(gulpWebpack({
      output: {
        filename: 'index.js'
      },
      plugins: [
        //Expose Global libraries
        new webpack.ProvidePlugin({
          $: "jquery",
          jQuery: "jquery",
          "window.jQuery": "jquery"
        }),
      ],
      devtool: "eval",
      resolve: {
        fallback: path.join(__dirname, "helpers")
      },
      module: {
        loaders: [{ 
          test: /\.hbs$/,
          loader: "handlebars-loader" 
        }]
      }      
    }))
    .pipe(gulp.dest('dist/'));
});

gulp.task('copy-images', function () {
  return gulp.src('./src/images/*')
             .pipe(gulp.dest('./dist/images'));
});

gulp.task('copy-manifest', function () {
  return gulp.src('./src/manifest.json')
             .pipe(gulp.dest('./dist/manifest.json'));
});

gulp.task('copy-favicon', function () {
  return gulp.src('./src/favicons/*')
             .pipe(gulp.dest('./dist/favicons/'));
});

gulp.task('copy-icons', function () {
  return gulp.src('./src/icons/*')
             .pipe(gulp.dest('./dist/icons/'));
});

gulp.task('copy-javascript', function() {
  return gulp.src('./src/js/*').pipe(gulp.dest('./dist/js/'));             
});

gulp.task('copy-serviceworker', function() {
  return gulp.src('./src/serviceworker.js').pipe(gulp.dest('./dist/serviceworker.js'));
});

const sassSettings = {
  outputStyle: 'compact', 
  sourceMap: true,
  outFile: 'style.css'
};

gulp.task('compile-handlebar-templates', function(){
  gulp.src('src/templates/**/*.hbs')
    .pipe(gulphandlebars())
    .pipe(wrap('Handlebars.template(<%= contents %>)'))
    .pipe(declare({
      namespace: 'App',
      noRedeclare: true, // Avoid duplicate declarations 
    }))
    .pipe(concat('templates.js'))
    .pipe(gulp.dest('dist/templates/'));
});

gulp.task('sass', function () {
  return gulp.src('./src/styles/master.scss')
    .pipe(sourcemaps.init())
    .pipe(sass(sassSettings).on('error', sass.logError))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./dist/styles/'));    
});
 
gulp.task('minify', function() {
  return gulp.src('src/*.html')
    .pipe(htmlmin({collapseWhitespace: true}))
    .pipe(gulp.dest('./dist/'));
});

// Static server
gulp.task('browser-sync', function() {
    browserSync.init({
        server: {
            baseDir: "./dist/"
        },
        open: 'none'
    });

    gulp.watch("src/**/*", ['sass','minify','webpack']);
    gulp.watch("dist/**/*").on('change', browserSync.reload);

});

/**
 * Build distributable version 
 */
gulp.task('build', [
  'sass',
  'minify',
  'copy-icons',
  'copy-favicon',
  'copy-manifest',
  'copy-images',
  'copy-serviceworker',
  'webpack'
]);

//Watch task
gulp.task('watch', function () {
  gulp.watch('src/**/*', ['sass','minify']);
});

gulp.task('default', ['browser-sync']);



