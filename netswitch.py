#!/bin/python3

"""
Netswitch - Quickly change the Netplan network configuration file
"""

_NAME = "netSwitch.py"
_VERS = "2.1"
_AUTHOR = "LLCZ00"
_DESCRIPTION = f"""Network Configuration Switch {_VERS}, by {_AUTHOR}\n
Description: Edits /etc/netplan/01-netcfg.yaml to quickily change network configurations.
(Made for debian/ubuntu VMs using netplan)\n
Requires sudo/root privileges to edit config file.
""" 

import sys
import re
import os
import argparse
import subprocess


class NetplanConfigBuilder:
    base_config = "network:\n  version: 2\n  renderer: networkd\n  ethernets:"
    default_indent = ' '*12
    def __init__(self, config_path, interface="enp0s3"):
        self.config_path = config_path
        self.config = f"{self.base_config}\n    {interface}:\n"
        self.indent = self.default_indent
        self.msg = ""

    def apply_config(self, apply=False):
        with open(self.config_path, "w") as file:
            file.write(self.config)
        if apply:    
            check = subprocess.run(["netplan", "apply"])
            if check.returncode == 0:
                print("[NS] Netplan configuration applied")
                if self.msg:
                    print(self.msg)
            else:
                print("[NS] Netplan configuration failed.")
        else:
            if self.msg:
                print(f"[NS] Netplan configuration written to {self.config_path}")
                print(self.msg)            

    def set_dhcp(self, state=False):
        dhcp_state = "no"
        if state:
            dhcp_state = "yes"
            self.msg += " - DHCP: Enabled\n"
        self.config += f"{self.indent}dhcp4: {dhcp_state}\n"

    def set_address(self, ipaddr=None):
        if ipaddr:
            self.config += f"{self.indent}addresses: [{ipaddr}]\n"
            self.msg += f" - Address set: {ipaddr}\n"

    def set_gateway(self, ipaddr=None):
        if ipaddr:
            self.config += f"{self.indent}gateway4: {ipaddr}\n"
            self.msg += f" - Gateway set: {ipaddr}\n"

    def set_dns(self, ipaddr=None):
        if ipaddr:
            self.config += f"{self.indent}nameservers:\n    {self.indent}addresses: [{ipaddr}]\n"
            self.msg += f" - DNS set: {ipaddr}\n"

    


class NetswitchParser(argparse.ArgumentParser):
    """Override argparse class for better error handler"""
    def error(self, message="Unknown error", help_flag=0):
        if help_flag:
            self.print_help()
        else:
            print("Error. {}".format(message))
            print("Try './{} --help' for more information.".format(self.prog))
        sys.exit(1)

class ValidateIPCIDR(argparse.Action):
    """argparse Action to validate ip address and CIDR"""
    def __call__(self, parser, namespace, value, option_string=None):

        if re.fullmatch(r"^(?:[1-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-5]{1,2}|)(?:\.(?:[0-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-5]{1,2})){3}/(?:[1-9]|[12][0-9]|3[012])\Z", value):
            setattr(namespace, self.dest, value)
        else:
            parser.error(f"Invalid IP Address or CIDR '{value}'")

class ValidateIP(argparse.Action):
    """argparse Action to validate ip address, CIDR optional"""
    def __call__(self, parser, namespace, value, option_string=None):

        if re.fullmatch(r"^(?:[1-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-5]{1,2}|)(?:\.(?:[0-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-5]{1,2})){3}(?:/(?:[1-9]|[12][0-9]|3[012]))?\Z", value):
            setattr(namespace, self.dest, value)
        else:
            parser.error(f"Invalid IP Address '{value}'")


def main():
    parser = NetswitchParser(
            prog=_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"Examples:\n./{_NAME} -a 10.10.10.1/16\n./{_NAME} --dhcp\n./{_NAME} --address=192.168.1.1/24 --dns 192.168.1.2 -g 192.168.1.2 --apply",
            description=_DESCRIPTION
        )

    parser.add_argument(
            '-a', '--address',
            help="Set IP address",
            metavar="IP/CIDR",
            dest="ipaddr",
            action=ValidateIPCIDR,
            type=str
        )
    parser.add_argument(
            '-d','--dhcp',
            help="Turn on DHCP",
            dest="dhcp",
            action="store_true"         
        )
    parser.add_argument(
            '-n','--dns',
            help="Set DNS nameserver address",
            metavar="IP",
            dest="dns",
            action=ValidateIP,
            type=str
        )
    parser.add_argument(
            '-g','--gateway',
            help="Set gateway address",
            metavar="IP",
            dest="gateway",
            action=ValidateIP,
            type=str
        )
    parser.add_argument(
            '-i', '--interface',
            help="Set target interface (Default: enp0s3)",
            metavar="INTERFACE",
            dest="interface",
            default="enp0s3",
            type=str
        )
    parser.add_argument(
            '-c','--config',
            help="Specify path of config file to edit/create (Default: /etc/netplan/01-netcfg.yaml)",
            metavar="FILEPATH",
            dest="configpath",
            default='/etc/netplan/01-netcfg.yaml',
            type=str
        )
    parser.add_argument(
            '--print',
            help="Print current netplan configuration",
            dest="print_config",
            default=False,
            action="store_true"
        )
    parser.add_argument(
            '--apply',
            help="Run 'netplan apply' command after writing config",
            dest="apply",
            action="store_true"
        )

    args = parser.parse_args()

    if args.print_config:
        with open(args.configpath, "r") as file:
            print(file.read())
        sys.exit()

    # Ensure root privileges
    if os.geteuid() != 0:
        parser.error("root privileges required.")


    np = NetplanConfigBuilder(config_path=args.configpath, interface=args.interface)

    np.set_dhcp(state=args.dhcp)

    np.set_address(ipaddr=args.ipaddr)

    np.set_gateway(ipaddr=args.gateway)

    np.set_dns(ipaddr=args.dns)

    np.apply_config(apply=args.apply)



if __name__ == "__main__":
    sys.exit(main())
