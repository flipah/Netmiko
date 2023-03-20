# Netmiko
This is my work in progress to bring network automation to a network and use a known good

To be able to use these scripts you first must install netmiko - Use the following commands on your linux box
 -Ubuntu 
  - get-install update
  - get-install upgrade
  - get-install python3
  - get-install python3-pip
  - pip3 install netmiko
 -Redhat
  - yum update
  - yum install python3
  - yum install python3-pip
  - pip3 install netmiko

Things to do
  1. Record hostname to name files (Complete)
  2. Backup to external share drive (Partial; Saves locally right now to a new directory)
  3. Parse through data to see if the config already has the commands in
  4. Automatic times script runs (weekly)
