#!/bin/bash

_NAME="remnux_setup.sh"
_V="1.0"
_AUTHOR="LLCZ00"

# Colors for success/error messages
NC='\033[0m' # No color
GREEN='\033[0;32m'
RED='\033[1;31m'

# Help Menu
help() 
{
echo "REMnux Inital Setup Automation Script
Version: $_V
Author: $_AUTHOR
Usage: ./$_NAME [options]
Description: Automates the setup of new REMnux virtual machines. 
This includes:
Inital Setup - remnux upgrade, apt update/upgrade
Sublime Text - Install general purpose code/text editor
Aliases - Add given aliases to ~/.bash_aliases
By default, only Inital Setup is performed.
Options:
  -h, --help                          Show usage (this page)
  -d, --no-setup                      DISABLE Initial Setup
  -s, --sublime                       Install Sublime Text
  -a  --alias=\"COMMAND='ALIAS'\",      Create aliases (enclosed in double-quotes, comma seperated)
  Examples:
  	./$_NAME 
  	./$_NAME -s -a \"ls='ls -li --color=auto'\",\"c='clear'\"
  	./$_NAME -alias=\"ls='ls -lia --color=auto'\" -d" 
	exit 0
}

# Error Handler
fail() 
{
	echo -e "${RED}[!!]${NC} Error: $1"
	exit 1
}

INIT=1
SUBL=0
ALIAS=0

### Handle Arguments ###
PARSED_ARGS=$(getopt -a -n $_NAME -o h,d,s,a: --long help,no-setup,sublime,alias: -- "$@")
VALID_ARGS=$?

# Catch invalid args
if [[ ("$VALID_ARGS" != "0") ]]; then
	echo "Try '$_NAME --help' for more information"
	exit 1
fi

eval set -- "$PARSED_ARGS"

# Parse args
while :
do
	case "$1" in
		-h | --help)
		help
		;;

		-d | --no-setup)		
		INIT=0
		shift 1;
		;;

		-s | --sublime)
		SUBL=1
		shift 1;
		;;

		-a | --alias)
		ALIAS=1
		echo -e "These aliases will be appended to ~/.bash_aliases, \nmake sure they're not duplicates, or misspelled."
		read -p "Continue?[y/n]" -n 1 -r
		if [[ $REPLY =~ ^[Nn]$ ]]; then
			echo ""
			exit 0;
		fi
		echo ""

		IFS=',' read -a Alist <<< $2 # Create list of aliases given via command line
		shift 2;
		;;

		--)
		break
		;;
	esac
done


######################################
# Initial Setup (Upgrade and Update) #
######################################

if [[ $INIT -eq 1 ]]; then
	echo -e "${GREEN}[~]${NC} Performing Initial Setup..."

	remnux upgrade || sudo remnux upgrade || fail "Initial Setup - 'remnux upgrade' failed."
	sudo apt update || fail "Initial Setup - 'apt update' failed."
	sudo apt upgrade || fail "Initial Setup - 'apt upgrade' failed."
	sudo apt install cmake || fail "Initial Setup - cmake install failed." 

	echo -e "${GREEN}[OK]${NC} Initial Setup complete.\n"
fi

########################
# Install Sublime Text #
########################

if [[ $SUBL -eq 1 ]]; then
	echo -e "${GREEN}[~]${NC} Installing Sublime Text..."

	sudo apt install dirmngr gnupg apt-transport-https ca-certificates software-properties-common || fail "Sublime Text - Repo dependancies failed."
	sudo add-apt-repository "deb https://download.sublimetext.com/ apt/stable/" || fail "Sublime Text - Repo import failed."
	curl -fsSL https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add - || fail "Sublime Text - key download failed."
	sudo apt install sublime-text || fail "Sublime Text - install failed."

	echo -e "${GREEN}[OK]${NC} Sublime Text installed.\n"
fi

##################
# Create Aliases #
##################

if [[ $ALIAS -eq 1 ]]; then
	echo -e "${GREEN}[~]${NC} Creating Aliases...\n"

	for alias in "${Alist[@]}"; do
		echo "alias $alias" | tee -a ~/.bash_aliases
	done

	echo -e "\n${GREEN}[OK]${NC} Aliases added to ./~bash_aliases.\n(Open new shell for alias changes to take effect)\n"
fi


echo -e "${GREEN}[DONE]${NC} REMnux setup script complete."
