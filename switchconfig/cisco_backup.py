#!/usr/bin/env python
#
# Name:     cisco_backup.py
# Synopsis: Backup Cisco switches
# Requires: python-docopt, python-pexpect
# Author:   Wouter
#

""" 
Backup all or specified Cisco switches

Usage: cisco_backup.py


"""

# Ugly workaround for git module with cron
import os
import pwd
os.getlogin = lambda: pwd.getpwuid(os.getuid())[0]

# Imports
import re
import sys
import socket
import pexpect


def checkDevices(ip_addr, port):
  """ Connect to device and return result """
  # Create socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Set socket timeout
  s.settimeout(1)

  try:
    # Open socket
    s.connect((ip_addr, port))
  except socket.error:
    # Close socket
    s.close()

    # Return status
    return False
  else:
    # Close socket
    s.close()

    # Return status
    return True

def getConfig(hostname, ip_addr, auth_method, username, enable, password):
  """ Get Cisco config """
  try:
    if auth_method == "ssh":
      # Ssh to switch and get "sh run" output
      child = pexpect.spawn("ssh %s@%s" % (username, ip_addr))
    elif auth_method == "telnet":
      # Telnet to switch and get "sh run" output
      child = pexpect.spawn("telnet %s" % ip_addr)
      child.expect("Username:")
      child.sendline(username)

    child.expect("[pP]assword:")
    child.sendline(password)

    # Check if we are in enable mode
    i = child.expect(["%s>" % hostname, pexpect.TIMEOUT], timeout=1)

    if i == 0:
      # Switch to enable mode
      child.sendline("enable")
      child.expect("[pP]assword:")
      child.sendline(enable)
    
    child.expect("%s#" % hostname)

    # Disable paging
    child.sendline("terminal length 0")
    child.expect("%s#" % hostname)

    # Get Version
    child.sendline("sh version | i (image|Model number|interface|serial)")
    child.expect("%s#" % hostname)

    sh_version = child.before

    # Get VTP status
    child.sendline("sh vtp stat")
    child.expect("%s#" % hostname)
 
    sh_vtp_stat = child.before

    # Get VLANs
    child.sendline("sh vlan brief")
    child.expect("%s#" % hostname)

    sh_vlan = child.before

    # Get running-config
    child.sendline("sh run")
    child.expect("%s#" % hostname)

    sh_run = child.before

    # Logout
    child.sendline("exit")

    # Close child
    child.close()

    # Prepare cisco config
    config = _prepConfig(sh_version, sh_vtp_stat, sh_vlan, sh_run)
  except pexpect.ExceptionPexpect as error:
    # Return error
    return (error, False)

  # Return config
  return (config, True)

def _prepConfig(sh_version, sh_vtp_stat, sh_vlan, sh_run):
  """ Prepare cisco config """
  # Prepend lines
  sh_vtp_stat = '\n'.join("!VTP: %s" % i for i in sh_vtp_stat.splitlines()) 
  sh_vlan = '\n'.join("!VLAN: %s" % i for i in sh_vlan.splitlines())
  sh_version = '\n'.join("!VERS: %s" % i for i in sh_version.splitlines())

  # Strip first lines
  sh_vtp_stat = '\n'.join(sh_vtp_stat.split('\n')[2:])
  sh_vlan = '\n'.join(sh_vlan.split('\n')[2:])
  sh_run = '\n'.join(sh_run.split('\n')[4:])
  sh_version = '\n'.join(sh_version.split('\n')[1:])

  # Strip ntp clock-period
  sh_run = re.sub("ntp clock-period [0-9]*", '', sh_run)
		
  # Strip stupid CRLF line terminators - We are NOT Windows admins
  sh_vtp_stat = sh_vtp_stat.replace('\r', '')
  sh_vlan = sh_vlan.replace('\r', '')
  sh_run = sh_run.replace('\r', '')
  sh_version = sh_version.replace('\r', '')

  # Get everything together
  config = "%s\n!\n%s\n!\n%s\n!\n%s" % (sh_version, sh_vtp_stat, sh_vlan, sh_run)
  
  # Return config
  return config

def writeConfig(hostname, config, write_dir):
  """ Write Cisco config to file """
  # Create file
  with open("%s/%s.cfg" % (write_dir, hostname), "w") as fh:
    # Write config
    fh.write(config)

  # Close file handle
  fh.close()


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
