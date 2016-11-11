module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    sass: {
      options: {
          loadPath: ['community/assets/vendor/foundation-sites/scss']
        },
      dist: {
        files: {
          'community/static/css/main.css' : 'community/assets/scss/main.scss'
        }
      }
    },
    copy: {
      target: {
        files: [
          {
            expand: true,
            cwd: 'community/assets/javascript',
            src: ['*.js'], 
            dest: 'community/static/javascript', 
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
        files: 'community/assets/**/*.js',
        tasks: ['javascript']
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy')
  grunt.registerTask('default',['watch']);
}