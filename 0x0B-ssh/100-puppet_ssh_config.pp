# Define the SSH client configuration file path
$ssh_config_file = '/etc/ssh/ssh_config'

# Ensure SSH client configuration file is properly configured
file_line { 'Turn off passwd auth':
  path   => $ssh_config_file,
  line   => 'PasswordAuthentication no',
}

file_line { 'Declare identity file':
  path   => $ssh_config_file,
  line   => 'IdentityFile ~/.ssh/school',
}


