module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    sass: {
      options: {
          loadPath: ['open_notices/assets/vendor/foundation-sites/scss']
        },
      dist: {
        files: {
          'open_notices/static/css/main.css' : 'open_notices/assets/scss/main.scss'
        }
      }
    },
    cssmin: {
      target: {
        files: [{
          expand: true,
          cwd: 'open_notices/static/css/',
          src: ['*.css', '!*.min.css'],
          dest: 'open_notices/static/css/',
          ext: '.min.css'
        }]
      }
    },
    copy: {
      target: {
        files: [
          {
            expand: true,
            cwd: 'open_notices/assets/javascript',
            src: ['*.js'],
            dest: 'open_notices/static/javascript',
            filter: 'isFile'
          }
        ]
      }
    },
    watch: {
      css: {
        files: '**/*.scss',
        tasks: ['sass', 'cssmin']
      },
      scripts: {
        files: 'open_notices/assets/**/*.js',
        tasks: ['copy']
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy')
  grunt.registerTask('default',['watch']);
}
