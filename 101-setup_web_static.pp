# rewrite task 0 using puppet

exec {'update':
    command => 'apt-get update',
    path    => '/usr/bin:usr/sbin:/bin',
}

package{'nginx':
    ensure   => 'installed',
    provider => 'apt',
}

file {'Hoberlton School':
    ensure  => 'present',
    path    => '/data/web_static/releases/test/index.html',
    content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

exec {'remove symlink':
    command => 'rm -rf /data/web_static/current',
    path    => '/usr/bin:/bin',
    before  => File['/data/web_static/current'],
}

file {'/data/web_static/current':
    ensure => 'link',
    path   => '/data/web_static/current',
    target => '/data/web_static/releases/test/',
}

file {'chowner-group':
    ensure  => 'directory',
    path    => '/data',
    owner   => 'shegz',
    group   => 'sudo',
    recurse => 'true',
}

file_line{'add hbnb_static':
    ensure => 'present',
    path   => '/etc/nginx/sites-available/default',
    line   => "\n\
        location /hbnb_static {\n\
                alias /data/web_static/current/;\n\
        }",
    after  => 'server_name _;',
}

exec {'nginx restart':
    command => 'sudo /usr/sbin/service nginx restart',
    path    => '/usr/sbin:/usr/bin:/bin',
}# rewrite task 0 using puppet

exec {'update':
    command => 'apt-get update',
    path    => '/usr/bin:usr/sbin:/bin',
}

package{'nginx':
    ensure   => 'installed',
    provider => 'apt',
}

file {'Hoberlton School':
    ensure  => 'present',
    path    => '/data/web_static/releases/test/index.html',
    content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

exec {'remove symlink':
    command => 'rm -rf /data/web_static/current',
    path    => '/usr/bin:/bin',
    before  => File['/data/web_static/current'],
}

file {'/data/web_static/current':
    ensure => 'link',
    path   => '/data/web_static/current',
    target => '/data/web_static/releases/test/',
}

file {'chowner-group':
    ensure  => 'directory',
    path    => '/data',
    owner   => 'shegz',
    group   => 'sudo',
    recurse => 'true',
}

file_line{'add hbnb_static':
    ensure => 'present',
    path   => '/etc/nginx/sites-available/default',
    line   => "\n\
        location /hbnb_static {\n\
                alias /data/web_static/current/;\n\
        }",
    after  => 'server_name _;',
}

exec {'nginx restart':
    command => 'sudo /usr/sbin/service nginx restart',
    path    => '/usr/sbin:/usr/bin:/bin',
}
