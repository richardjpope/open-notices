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
        tasks: ['sass']
      },
      scripts: {
        files: 'open_notices/assets/**/*.js',
        tasks: ['copy']
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy')
  grunt.registerTask('default',['watch']);
}