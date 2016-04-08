module.exports = function (grunt) {
    require('jit-grunt')(grunt);
    require('time-grunt')(grunt);

    grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
        base_path: 'src/static/{{ cookiecutter.short_name }}/',
        copy: {
            misc: {
                files: [{
                    expand: true,
                    cwd: '<%= base_path %>src/misc/',
                    src: ['**'],
                    dest: '<%= base_path %>dist/misc/'
                }]
            },
            favicons: {
                files: [{
                    expand: true,
                    cwd: '<%= base_path %>src/favicons/',
                    src: ['**'],
                    dest: '<%= base_path %>dist/favicons/'
                }]
            }
        },
		sass: {
			options: {
				indentedSyntax: true,
				sourceMap: true
			},
			dist: {
				files: [
                    {
                        src: '<%= base_path %>src/styles/masters/main.sass',
                        dest: '<%= base_path %>dist/styles/main.css',
                        nonull: true
                    },
					{
                        src: '<%= base_path %>src/styles/masters/ie.sass',
                        dest: '<%= base_path %>dist/styles/ie.css',
                        nonull: true
                    },
					{
                        src: '<%= base_path %>src/styles/masters/print.sass',
                        dest: '<%= base_path %>dist/styles/print.css',
                        nonull: true
                    },
                    {
                        src: '<%= base_path %>src/styles/masters/admin.sass',
                        dest: '<%= base_path %>dist/styles/admin.css',
                        nonull: true
                    }
				]
			}
		},
		autoprefixer: {
			dist: {
				options: {
					map: true
				},
				files: [
                    {
                        src: '<%= base_path %>dist/styles/main.css',
                        dest: '<%= base_path %>dist/styles/main.css',
                        nonull: true
                    },
					{
                        src: '<%= base_path %>dist/styles/ie.css',
                        dest: '<%= base_path %>dist/styles/ie.css',
                        nonull: true
                    },
					{
                        src: '<%= base_path %>dist/styles/print.css',
                        dest: '<%= base_path %>dist/styles/print.css',
                        nonull: true
                    },
                    {
                        src: '<%= base_path %>dist/styles/print.css',
                        dest: '<%= base_path %>dist/styles/print.css',
                        nonull: true
                    }
				]
			}
		},
        cssmin: {
            options: {
                sourceMap: true,
                shorthandCompacting: false,
                roundingPrecision: -1/*,
                relativeTo: '<%= base_path %>dist/styles/',
                rebase: true*/
            },
            dist: {
                files: [
                    {
                        src: [
                            'bower_components/normalize.css/normalize.css',
                            'bower_components/jquery-ui/themes/base/core.css',
                            'bower_components/jquery-ui/themes/base/datepicker.css',
                            '<%= base_path %>dist/styles/main.css'
                        ],
                        dest: '<%= base_path %>dist/styles/all.css',
                        nonull: true
                    },
	                {
                        src: [
                            '<%= base_path %>dist/styles/ie.css'
                        ],
                        dest: '<%= base_path %>dist/styles/ie.css',
                        nonull: true
                    },
	                {
                        src: [
                            '<%= base_path %>dist/styles/print.css'
                        ],
                        dest: '<%= base_path %>dist/styles/print.css',
                        nonull: true
                    },
                    {
                        src: [
                            '<%= base_path %>dist/styles/admin.css'
                        ],
                        dest: '<%= base_path %>dist/styles/admin.css',
                        nonull: true
                    }
                ]
            }
        },
        jshint: {
            all: ['Gruntfile.js', '<%= base_path %>src/scripts/**/*.js']
        },
        modernizr: {
            dist: {
                dest: '<%= base_path %>dist/scripts/modernizr.js',
                parseFiles: true,
                //"devFile": "/PATH/TO/modernizr-dev.js",
                //"outputFile": "/PATH/TO/modernizr-output.js",
                "tests": [
                    "canvas",
                    "input",
                    "svg",
                    "touchevents",
                    "cssanimations",
                    "appearance",
                    "backdropfilter",
                    "backgroundblendmode",
                    "backgroundcliptext",
                    "bgpositionshorthand",
                    "bgpositionxy",
                    [
                        "bgrepeatspace",
                        "bgrepeatround"
                    ],
                    "backgroundsize",
                    "bgsizecover",
                    "borderimage",
                    "borderradius",
                    "boxshadow",
                    "boxsizing",
                    "csscalc",
                    "csscolumns",
                    "ellipsis",
                    "flexbox",
                    "flexboxlegacy",
                    "fontface",
                    "cssgradients",
                    "csshairline",
                    "cssmask",
                    "mediaqueries",
                    "multiplebgs",
                    "opacity",
                    "csspositionsticky",
                    "rgba",
                    "textshadow",
                    "csstransforms",
                    "preserve3d",
                    "csstransitions",
                    "placeholder",
                    "sizes",
                    "srcset",
                    "svgasimg",
                    "inlinesvg"
                ],
                options: [
                    'setClasses'
                ]
            }
        },
        uglify: {
            //options: {
            //     mangle: false,
            //     compress: false,
            //     beautify: true
            //},
            dist_all: {
                files: [
                    {
                        src: [
                            '<%= base_path %>dist/scripts/modernizr.js',
                            'bower_components/jquery/dist/jquery.js',
                            '<%= base_path %>src/scripts/tabs.js',
                            '<%= base_path %>src/scripts/alert.js'
                        ],
                        dest: '<%= base_path %>dist/scripts/all.js',
                        nonull: true
                    }
                ]
            },
            dist_admin: {
                files: [
                    {
                        src: [
                            'bower_components/jquery/dist/jquery.js'
                        ],
                        dest: '<%= base_path %>dist/scripts/admin.js',
                        nonull: true
                    }
                ]
            },
            dist_ie: {
                files: [
                    {
                        src: [
                            'bower_components/html5shiv/dist/html5shiv.js',
                            '<%= base_path %>src/scripts/ie8-shim.js',
                            'bower_components/selectivizr-bower/selectivizr.js'
                        ],
                        dest: '<%= base_path %>dist/scripts/ie.js',
                        nonull: true
                    }
                ]
            }
        },
        imagemin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= base_path %>src/images/',
                    src: ['**/*.{png,jpg,jpeg,gif,svg}'],
                    dest: '<%= base_path %>dist/images/'
                }]
            }
        },
        grunticon: {
            icons: {
                files: [{
                    expand: true,
                    cwd: "<%= base_path %>src/icons/",
                    src: ["*.svg"],
                    dest: "<%= base_path %>dist/icons/"
                }],
	            options: {
		            cssprefix: '.icn-'
	            }
            }
        },
		watch: {
            options: {
                livereload: {
                    host: '0.0.0.0',
                    port: 35728
                }
            },
			css: {
				files: '<%= base_path %>src/styles/**/*',
				tasks: ['css']
			},
			js: {
				files: [
                    '<%= base_path %>src/scripts/**/*.js'
                ],
				tasks: ['js']
			},
            html: {
                files: ['**/templates/**/*.html']
            }
		},
        clean: ['<%= base_path %>dist/*'],
        concurrent: {
            all: ['js', 'images', 'icons', 'css'],
            css: [
                'sass:dist'
            ],
            js: [
                'jshint',
                'uglify:dist_all',
                'uglify:dist_admin',
                'uglify:dist_ie'
            ]
        }
	});

	grunt.registerTask('default', ['watch']);

    grunt.registerTask('js', ['modernizr', 'concurrent:js']);
	grunt.registerTask('css', ['concurrent:css', 'autoprefixer', 'cssmin']);
	grunt.registerTask('images', ['imagemin']);
	grunt.registerTask('icons', ['grunticon']);

	grunt.registerTask('build', [
        'clean',
        'copy',
        'images',
        'icons',
        'js',
        'css'
    ]);
};
