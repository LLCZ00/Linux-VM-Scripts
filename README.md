# Setup/QoL Scripts for GNU/Linux Virutal Machines
Various scripts for facilitating the quick start up of malware analysis environments on (REMnux) virtual machines.<br/>
WIP
## remnux_setup.sh
Automates my inital setup of REMnux virtual machines.<br/>
Currently, remnux_setup.sh performs the following actions:
- Updating and upgrading distro/tools with *remnux upgrade* and *apt update*/*upgrade*
- Downloading and installing Sublime Text, a code/text editor that prefer over the default Scite
- Adding any given aliases
### Usage
```
./remnux_setup.sh [options]

Options:
  -h, --help                          Show usage (this page)
  -d, --no-setup                      DISABLE Initial Setup
  -s, --sublime                       Install Sublime Text
  -a  --alias="COMMAND='ALIAS'",      Create aliases (enclosed in double-quotes, comma seperated)

  Examples:
  	./remnux_setup.sh 
  	./remnux_setup.sh -s -a "ls='ls -li --color=auto'","c='clear'"
  	./remnux_setup.sh -alias="ls='ls -lia --color=auto'" -d

```
### Issues & TODO
- The Initial Setup occasionally fails, but is successful upon re-run. I do not know why.
- Add more features, as needed
## netSwitch.py
facilitates the quick and easy change of the Netplan network configuration file. <br/> 
Designed for switching between "Bridged Adapter" and "Internal" modes on REMnux virtual machines. <br/>
netSwitch.py edits the netplan configuration file (/etc/netplan/01-netcfg.yaml, by default) to either enable DHCP, or manually set the given IP address.<br/>
The virtual machine network settings must then be set to the corresponding configuration (Bridged Adapter or Interal). Doing this manually is cumbersome when going from "sandbox" to regular internet.
### Usage
```
./netSwitch.py [-h] [-b] [-i IP/CIDR]
(Requires sudo/root privileges)

Options:
  -h, --help            show this help message and exit
  -b, --bridged         Switch to bridged network config (DHCP)
  -i IP/CIDR, --internal IP/CIDR
                        Switch to internal network config

Examples:
./netSwitch.py -i 10.10.10.1/16
./netSwitch.py --bridged
./netSwitch.py --internal="192.168.1.1/24"
```
### Issues & TODO
- As of version 1.0, this will only work with the basic default netplan configuration file. It will destroy any other configurations.
- There may be "false negatives" when validating the given IP address, occasionally I run into mistakes in my validation regex when testing with random IPs.
- Add a way to change the name of the config file to be edited
- Add different configurations, as needed
- Fix class structure, it's currently whack
