#!/bin/python3

_NAME = "netSwitch.py"
_VERS = "1.0"
_AUTHOR = "LLCZ00"

import sys, os
import re, argparse


class ArgumentHandler:
	def __init__(self):
		self.parser = self.LLCZ00Parser(
			prog=_NAME,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog="Examples:\n./{0} -i 10.10.10.1/16\n./{0} --bridged\n./{0} --internal=\"192.168.1.1/24\"".format(_NAME),
			description=\
"""Network Configuration Switch {0}, by {1}\n
Description: Edits /etc/netplan/01-netcfg.yaml to quickily 
switch between bridged and internal network configurations.
(Made for debian/ubuntu VMs using netplan)\n
Requires sudo/root privileges to edit config file.
""".format(_VERS, _AUTHOR)		
		)
		self.parser.add_argument(
			'-b', '--bridged',
			help="Switch to bridged network config (DHCP)",
			action="store_true",
			dest="bridge"
		)

		self.parser.add_argument(
			'-i', '--internal',
			help="Switch to internal network config",
			nargs=1,
			dest="ipaddr",
			type=str,
			metavar="IP/CIDR",
			action=self.ValidateIP
		)

		self.args = self.parser.parse_args()

		# Make sure one (and only 1) configuration is given
		if self.args.ipaddr and self.args.bridge: 
			self.parser.error("More than 1 configuration given.")
		elif not (self.args.ipaddr or self.args.bridge):
			self.parser.error(help_flag=1) 

		# Ensure root privileges
		if os.geteuid() != 0:
			self.parser.error("root privileges required.")


	class LLCZ00Parser(argparse.ArgumentParser): # Override argparse's error method
		def error(self, message="Unknown error", help_flag=0):
			if help_flag:
				self.print_help()
			else:
				print("Error. {}".format(message))
				print("Try './{} --help' for more information.".format(self.prog))
			sys.exit(1)


	class ValidateIP(argparse.Action): # argparse Action to validate ip address
		def __call__(self, parser, namespace, values, option_string=None):

			if re.fullmatch(r"^(?:[1-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-5]{1,2}|)(?:\.(?:[0-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-5]{1,2})){3}/(?:[1-9]|[12][0-9]|3[012])\Z", values[0]):
				setattr(namespace, self.dest, values[0])
			else:
				parser.error("Invalid IP Address '{}'".format(values[0]))


class NetworkSwitch(ArgumentHandler):
	def __init__(self):	
		super().__init__() # Parses arguments

		self.config_file = "/etc/netplan/01-netcfg.yaml" # Netplan configuration file

		with open(self.config_file, "r") as file: # Save copy of config file for alterations
			self.config = file.read()


	def bridged(self): 
		self.config = re.sub(r"dhcp4:\s*(?:yes|no)\n\s*addresses:\s*\[.*\]", "dhcp4: yes", self.config, 1, flags=re.IGNORECASE)

		self.applyConfiguration()
		print("Bridged network configuration (DHCP) set.")
		print("(Change VM settings to 'Bridged Adapter' for this to take effect)")


	def internal(self): 
		indent = " "*12 # Indentation of dhcp: no and addresses [] has to be identical (12, arbitrary)
		dhcp = "\n{0}dhcp4: no".format(indent)
		addr = "{0}addresses: [{1}]".format(indent, self.args.ipaddr)

		self.config = re.sub(r"\s*dhcp4:\s*(?:yes|no)", dhcp, self.config, 1, flags=re.IGNORECASE)

		if re.search(r"addresses:\s*\[.*\]", self.config, flags=re.IGNORECASE):
			self.config = re.sub(r"\s*addresses:\s*\[.*\]", "\n"+addr, self.config, 1, flags=re.IGNORECASE) # Replaces the previous adderess, if one is already defined
		else:
			self.config = "{0}{1}\n".format(self.config, addr)

		self.applyConfiguration()
		print("Internal network configuration set.\nIP Address: {}".format(self.args.ipaddr))
		print("(Change VM settings to 'Internal Network' for this to take effect)")


	def applyConfiguration(self): # Write new configuration to config file and apply changes
		with open(self.config_file, "w") as file:
			file.write(self.config)
		os.system("sudo netplan apply")


	def main(self):
		if self.args.ipaddr:
			self.internal()
		elif self.args.bridge:
			self.bridged()
		else:
			self.parser.error("Unknown error.")



if __name__ == "__main__":
	ns = NetworkSwitch()
	ns.main()
