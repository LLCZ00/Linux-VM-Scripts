#!/bin/bash

_NAME="xbuild.sh"
_V=1.0
_AUTHOR="LLCZ00"

help()
{
echo "GCC Cross-Compiler Builder 
Version: $_V
Author: $_AUTHOR

Usage: ./$_NAME [options] TARGET

Builds a cross-compiler (CC) for a specified architecture.
Downloads and installs required dependencies, when necessary.
(Made for Debian/Ubuntu)

Required:
  TARGET                            Architecture to build CC for

Options:
  -h, --help                        Show usage (this page)
  -t, --tool-dir=DIR                CC tool destination (Default: \$HOME/opt/cross)
  -s, --src-dir=DIR                 GCC/Binutils Source Code destination (Default: \$HOME/src)

  --gcc-build=--arg,--spaces=no     Additional arguments to pass when configuring GCC
  --bin-build=--arg,--spaces=no     Additional arguments to pass when configuring Binutils

Examples:
$_NAME i386-elf
$_NAME --gcc-build=--disable-nls,--enable-languages=c --bin-build=--disable-werror x86_64-pc-linux-gnu
$_NAME --tool-dir=\$HOME/Desktop/tools --src-dir=/tmp/source arm-eabi"
	
	exit 0
}

# Target architecture
TARGET=unset

# Source code and tool directory (defaults)
SOURCE_DIR=$HOME/src
PREFIX="$HOME/opt/cross"

# Build configuration arguments ( NOT CURRENTLY IN USE )
GCC_CONFIG="--disable-nls,--enable-languages=c,--disable-libssp,--without-headers"
BIN_CONFIG="--with-sysroot,--disable-nls,--disable-werror"


### Handle Arguments ###
PARSED_ARGS=$(getopt -a -n $_NAME -o h,t:,s: --long help,tool-dir:,src-dir:,gcc-build:,bin-build: -- "$@")
VALID_ARGS=$?

# Catch invalid args
if [[ ("$VALID_ARGS" != "0") ]]; then
	echo "Try '$_NAME --help' for more information"
	exit 2
fi

eval set -- "$PARSED_ARGS"

# Parse args
while :
do
	case "$1" in
		-h | --help)
		help
		;;

		-t | --tool-dir)		
		PREFIX="$2"
		shift 2
		;;

		-s | --src-dir)
		SOURCE_DIR=$2
		shift 2
		;;

		--gcc-build)
		GCC_CONFIG=$2
		shift 2
		;;

		--bin-build)
		BIN_CONFIG=$2
		shift 2
		;;

		--)
		if [[ -z $2 ]]; then
			echo  -e "$_NAME: missing target\nTry '$_NAME --help' for more information"
			exit 2
		else
			TARGET=$2
		fi
		break
		;;
	esac
done


#######################################################################################################
# FUNCTIONAL START #
#######################################################################################################

### Install build-essentials and general CC dependencies ###
echo "[~] Installing build-essentials and CC dependencies"
sudo apt install -y \
	build-essential \
	bison \
	flex \
	libgmp3-dev \
	libmpc-dev \
	libmpfr-dev \
	texinfo
echo "[OK] Dependancies installed."


### Download/unzip GCC and Binutils source code ###

# Check for source folder, 
# if not found, check for archive. 
# if archive not found, download, then unzip into source folder.
# This avoids waiting 10 minutes for the source files to download every time we run this

# Binutils
BIN_SOURCE=$SOURCE_DIR/binutils_source.tar.gz
if [[ ! -e "$SOURCE_DIR/binutils-2.38" ]]; then

	# Download
	if [[ ! -e "$BIN_SOURCE" ]]; then
		echo -n "[~] Downloading Binutils to '$BIN_SOURCE'..."
		curl -sS -o $BIN_SOURCE https://ftp.gnu.org/gnu/binutils/binutils-2.38.tar.gz
		echo "done."
	fi

	# Unzip, with or without download
	echo -n "[~] Unzipping binutils_source.tar.gz..."
	tar -xf $BIN_SOURCE -C $SOURCE_DST
	echo "done."

else
		# If source already exists.. 
		echo "[OK] Binutils Source found, download not required."
fi

# GCC
GCC_SOURCE=$SOURCE_DIR/gcc_source.tar.gz
if [[ ! -e "$SOURCE_DIR/gcc-11.3.0" ]]; then

	# Download
	if [[ ! -e "$GCC_SOURCE" ]]; then
		echo -n "[~] Downloading GCC to '$GCC_SOURCE'..."
		curl -sS -o $GCC_SOURCE https://bigsearcher.com/mirrors/gcc/releases/gcc-11.3.0/gcc-11.3.0.tar.gz
		echo "done."
	fi
	# Unzip, with or without download
	echo -n "[~] Unzipping gcc_source.tar.gz..."
	tar -xf $GCC_SOURCE -C $SOURCE_DST
	echo "done."

else
		# If source already exists.. 
		echo "[OK] GCC Source found, download not required."
fi


### Build tools ###

# Define CC and LD (?)
CC=/usr/bin/gcc-9
LD=/usr/bin/gcc-9

# Set up directories, 
mkdir -p $SOURCE_DIR/binutils-build 
mkdir -p $SOURCE_DIR/gcc-build
mkdir -p $PREFIX

# Add tool directory to PATH
PATH="$PREFIX/bin:$PATH"

# Binutils
echo "[~] Building Binutils..."
cd $SOURCE_DIR/binutils-build 
../binutils-2.38/configure --target=$TARGET --prefix="$PREFIX" --with-sysroot --enable-multilib --disable-nls --disable-werror
make
make install
echo "[OK] Binutils built."

# GCC (TAKES FOREVER)
echo "[~] Building GCC..."
cd $SOURCE_DIR/gcc-build
../gcc-11.3.0/configure --target=$TARGET --prefix="$PREFIX" --disable-nls --enable-languages=c --disable-libssp --without-headers
make all-gcc
make all-target-libgcc
make install-gcc
make install-target-libgcc
echo "[OK] GCC built."


### Success ###

# Check if tools are actually there
if [[ ! -e "$PREFIX/bin/$TARGET-ld" || ! -e "$PREFIX/bin/$TARGET-gcc" ]]; then
	echo "[!] Something went wrong: $TARGET-ld or $TARGET-gcc not found."
	exit -1
fi

echo "[~] $TARGET Cross-Compiler successfully installed!"
echo -e "\nTool usage:\n$PREFIX/bin/$TARGET-[TOOLNAME]"
