# Filelink Daemon Service
Filelink Daemon Service for Linux

## Install
1. Clone [main Filelink repository](https://github.com/medowic/filelink)
```sh
git clone https://github.com/medowic/filelink.git
```
2. Move to `filelink` directory and download `daemon-install.sh` file
```sh
cd filelink
wget -O daemon-install.sh https://raw.githubusercontent.com/medowic/filelink-daemon/master/daemon-install.sh
```
3. Run `daemon-install.sh`
```sh
chmod +x daemon-install.sh
./daemon-install.sh
```
> [!IMPORTANT]
> It is not recommended to use the Filelink server as root in the daemon, so the installer will use `sudo` to install the Filelink daemon service as a non-root user with all necessary permissions
>
> **Don't run the installation like** `sudo ./daemon-install.sh`**. It will be parsed as a root installation**

## Run
To use Filelink Server in daemon run `filelink` command

For example:
```sh
filelink start/restart/stop
```

To show current working configuration run `filelink`
```sh
filelink
```

If the Filelink server is disabled, the output will be as follows
```sh
$ filelink
Filelink Server is disabled
```

There is a `filelink help` command output with available commands
```
Commands:
 * help      -   Show this page and exit
 * version   -   Show Filelink version and exit
 * update    -   Checking for new updates from Github
 * config    -   Edit Filelink configuration with preferred editor
 * setpath   -   Set new path to folder for sharing
 * start     -   Start Filelink Server
 * restart   -   Restart Filelink
 * stop      -   Stop Filelink Server
```

# License
This project is under the [MIT License](https://raw.githubusercontent.com/medowic/filelink-daemon/master/LICENSE)
