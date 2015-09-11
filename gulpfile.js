var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var livereload = require('gulp-livereload');

var baseCodeDir = 'tracker/site'
var baseTemplateDir = 'tracker/templates';
var baseSrcDir = 'tracker/static-dev';
var baseDestDir = 'tracker/static';

gulp.task('sass', function () {
    gulp.src(baseSrcDir + '/scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest(baseSrcDir + '/css'))
        .pipe(livereload());
});

gulp.task('copy-foundation-fonts', function () {
	gulp.src(baseSrcDir + '/components/foundation-icon-fonts/foundation-icons.{ttf,woff,eot,svg}')
		.pipe(gulp.dest(baseDestDir + '/css/'));
});



gulp.task('concat-js', function() {
	gulp.src([
			baseSrcDir + '/components/fastclick/lib/fastclick.js',
			baseSrcDir + '/components/jquery/dist/jquery.min.js',
			baseSrcDir + '/components/foundation/js/foundation.min.js',
			baseSrcDir + '/components/chosen/chosen.jquery.min.js',
			baseSrcDir + '/js/app.js'
		])
		.pipe(concat('app.built.js'))
		.pipe(gulp.dest(baseDestDir + '/js'));
});


gulp.task('copy-styles', function () {
	gulp.src([
			baseSrcDir + '/css/*.css',
			baseSrcDir + '/components/chosen/chosen-sprite.png',
			baseSrcDir + '/components/chosen/chosen-sprite@2x.png'
		])
		.pipe(gulp.dest(baseDestDir + '/css/'));
});

gulp.task('copy-js', function () {
	gulp.src(baseSrcDir + '/components/modernizr/modernizr.js').pipe(gulp.dest(baseDestDir + '/js/'));
});

gulp.task('html', function () {
	gulp.src(baseTemplateDir + '/**/*.html')
		.pipe(changed('.'))
		.pipe(livereload());
});

gulp.task('code', function () {
	gulp.src(baseCodeDir + '/*.py')
		.pipe(livereload());
});

gulp.task('build-styles', ['sass', 'copy-foundation-fonts'])

// Watch task
// Watches SASS
gulp.task('watch', function() {
  livereload.listen();
  gulp.watch(baseSrcDir + '/scss/*.scss', ['sass']);
  gulp.watch(baseTemplateDir + '/**/*.html', ['html']);
  gulp.watch(baseCodeDir + '/*.py', ['code']);
});

gulp.task('build', ['build-styles', 'copy-styles', 'copy-js', 'concat-js'])
gulp.task('default', ['build-styles', 'watch']);
