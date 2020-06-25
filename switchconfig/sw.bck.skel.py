# Imports
import re
import sys
import socket
import pexpect


def checkDevices(ip_addr, port):
    return True

def getConfig(hostname, ip_addr, auth_method, username, enable, password):
  """ Get Cisco config """
    # Disable paging
    # Get Version
    # Get VTP status
    # Get VLANs
    # Get running-config
    # Logout
    # Close child

    # Prepare cisco config
    config = _prepConfig(sh_version, sh_vtp_stat, sh_vlan, sh_run)
  # Return config
  return (config, True)

def _prepConfig(sh_version, sh_vtp_stat, sh_vlan, sh_run):
  """ Prepare cisco config """
  # Prepend lines

  # Strip first lines

  # Strip ntp clock-period
		
  # Strip stupid CRLF line terminators - We are NOT Windows admins
  #sh_vtp_stat = sh_vtp_stat.replace('\r', '')

  # Get everything together
  config = "%s\n!\n%s\n!\n%s\n!\n%s" % (sh_version, sh_vtp_stat, sh_vlan, sh_run)
  
  # Return config
  return config

def writeConfig(hostname, config, write_dir):
  """ Write Cisco config to file """
  # Create file
  # Close file handle


def main():
  """ Main part of script """
  # Global vars
  username = "lab"
  enable ="lab123"
  password = "lab123"
  write_dir = "configs"
  
  ip_addr = '10.200.0.1'
  hostname = 'LAB01'
  
  auth_method = "telnet"
  # Get config
  print "Getting config from %s" % hostname
  (config, got_config) = getConfig(hostname, ip_addr, auth_method, 
    username, enable, password)

  if got_config == True:
    # Write config to file
    print "Writing config from %s to file" % hostname
    writeConfig(hostname, config, write_dir)

    # Add and commit config
    #print "Adding and commiting config from %s" % hostname
    #commitConfig(hostname, username, git_repo)
  else:
    # For debugging purposes only
    #print config
    print "ERROR: Could not get config from %s" % hostname 


# Exucute main
if __name__ == "__main__":
  main()
