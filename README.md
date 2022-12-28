# Setup/QoL Scripts for GNU/Linux Virutal Machines
Operating system-specific scripts that haven't been fleshed out enough for their own repo.

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
