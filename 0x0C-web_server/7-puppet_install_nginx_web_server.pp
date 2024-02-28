# Install Nginx web server using Puppet

# Ensure Nginx package is installed
package { 'nginx':
  ensure => installed,
}

# Add a rewrite rule to redirect /redirect_me to a specified URL
file_line { 'nginx-redirect':
  ensure => 'present',
  path   => '/etc/nginx/sites-available/default',
  after  => 'listen 80 default_server;',
  line   => 'rewrite ^/redirect_me https://github.com/Anagha-lin permanent;',
}

# Create index.html file with "Hello World!" content
file { '/var/www/html/index.html':
  content => 'Hello World!',
}

# Ensure Nginx service is running
service { 'nginx':
  ensure  => running,
  require => Package['nginx'],
}

