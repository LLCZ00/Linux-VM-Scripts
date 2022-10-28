# GCC Cross-Compiler Builder
### xbuild.sh
Builds a cross-compiler for a desired architecture, as well as downloading/installing required dependencies. <br/> The purpose of **xbuild** is to expedite the awkward process of downloading/configuring/building a useable cross-compiler. <br/>
Made with OS development in mind, on a Debian/Ubuntu system, so individual efficacy may vary.
## Usage
```
GCC Cross-Compiler Builder 

Usage: ./xbuild.sh [options] TARGET

Required:
  TARGET                            Architecture to build CC for

Options:
  -h, --help                        Show usage (this page)
  -t, --tool-dir=DIR                CC tool destination (Default: $HOME/opt/cross)
  -s, --src-dir=DIR                 GCC/Binutils Source Code destination (Default: $HOME/src)

Examples:
xbuild.sh i386
xbuild.sh --tool-dir=$HOME/Desktop/tools --source-dir=/tmp/source arm-eabi
```
#### After setting source and tool directories, **xbuild** performs the following actions:
1. Installs *build-essential* package (if the system doesnt already have GCC, Make, libc6-dev, etc.)
2. Installs general cross-compiler dependencies: *bison*, *flex*, *libgmp3-dev*, *libmpc-dev*, *libmpfr-dev*, and *texinfo*.
3. Downloads/unzips GCC/Binutils source code, if necessary.
4. Builds GCC and Binutils tools, installing them in the directory defined by default or *-t*,*--tool-dir*
5. Checks to ensure new tools actually exist, before returning 'Success' message.
## GCC/Binutils Configuration
Currently, the best way to add arguments to the *configure* command is to just edit the script. See link below for details.<br/>
[GCC Config Documentation](https://gcc.gnu.org/install/configure.html)<br/>
## Issues
- GCC/Binutils download URLs are currently hardcoded in, which could become an issue in the future.
- Downloading GCC/Binutils source code takes forever. Nothing I can really do about it, but it does.
- Building GCC also takes forever. See point about download time.
 ## To do
- Automatically download most recent version of GCC/Binutils. Retrieve names dynamically. (Currently hardcoded)
- Pass configure arguments via cmdline
