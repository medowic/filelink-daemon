#!/usr/bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

function err() {
    echo "Error: couldn't copy main Filelink files to ${1}"
    echo "Check that you're root or 'wget' is installed at your machine and try again"
    echo "failed with exit-code 1"
    exit 1
}

function install() {
    COMMAND="${1}"
    SYSTEMD="[Unit]
Description=Filelink Server Service
After=network.target

[Service]
EnvironmentFile=${SCRIPT_DIR}/config/daemon.source 
User=$(whoami)
ExecStart=/usr/bin/python3 ${SCRIPT_DIR}/run.py -o -f \$FILELINK_PATH
WorkingDirectory=${SCRIPT_DIR}
SuccessExitStatus=0

[Install]
WantedBy=multi-user.target"

    if ! ${COMMAND} wget -O /usr/bin/filelink https://raw.githubusercontent.com/medowic/filelink-daemon/master/filelink.py > /dev/null 2>&1; then
        err "/usr/bin/filelink (by wget download)";
    fi

    if ! [ -f "${SCRIPT_DIR}"/config/daemon.source ]; then
        if [ -f "${SCRIPT_DIR}"/config/config.yaml ]; then
            ${COMMAND} rm "${SCRIPT_DIR}"/config/config.yaml
        else
            ${COMMAND} mkdir "${SCRIPT_DIR}"/config
        fi
        if ! ${COMMAND} wget -O "${SCRIPT_DIR}"/config/config.yaml https://raw.githubusercontent.com/medowic/filelink-daemon/master/config/config.yaml > /dev/null 2>&1; then
            err "${SCRIPT_DIR}/config/config.yaml (by wget download)";
        fi
    fi

    if ! ${COMMAND} wget -O "${SCRIPT_DIR}"/version/version_daemon.data https://raw.githubusercontent.com/medowic/filelink-daemon/master/version/version.data > /dev/null 2>&1; then
        err "${SCRIPT_DIR}/version/version_daemon.data (by wget download)";
    fi

    if ! ${COMMAND} wget -O /usr/bin/filelink-uninstall https://raw.githubusercontent.com/medowic/filelink-daemon/master/daemon-uninstall.sh > /dev/null 2>&1; then
        err "/usr/bin/filelink-uninstall (by wget download)";
    fi

    if ! echo "${SYSTEMD}" | ${COMMAND} tee /etc/systemd/system/filelink.service > /dev/null 2>&1; then
        err "/etc/systemd/system/filelink.service";
    fi

    if ! [ -f "${SCRIPT_DIR}"/config/daemon.source ]; then
        if ! echo "FILELINK_PATH=${SCRIPT_DIR}/files" | ${COMMAND} tee "${SCRIPT_DIR}"/config/daemon.source > /dev/null 2>&1; then
            err "${SCRIPT_DIR}/config/daemon.source";
        fi
    fi

    if ! [ -d /etc/filelink ] || ! [ -f /etc/filelink/path ]; then
        ${COMMAND} mkdir /etc/filelink > /dev/null 2>&1
        if ! echo "${SCRIPT_DIR}" | ${COMMAND} tee /etc/filelink/path > /dev/null 2>&1; then
            err "/etc/filelink/path";
        fi
    fi

    ${COMMAND} chmod +x /usr/bin/filelink
    ${COMMAND} chmod 755 /usr/bin/filelink
    
    ${COMMAND} chmod +x /usr/bin/filelink-uninstall
    ${COMMAND} chmod 755 /usr/bin/filelink-uninstall

    ${COMMAND} systemctl daemon-reload > /dev/null
    ${COMMAND} systemctl stop filelink > /dev/null
}

echo "Install Filelink Server as daemon"
echo "";
echo "Install as '$(whoami)' user"
echo "Working path was set to '${SCRIPT_DIR}'"
echo ""

if [ "${EUID}" -ne 0 ]; then
    if ! [ -f /usr/bin/sudo ]; then
        echo "You're not a root-user and it's looks like you haven't 'sudo' installed on your machine";
        echo "Script can't run without 'sudo', if you're not root";
        echo "Please install 'sudo' and try again";
        echo "failed with exit-code 2"
        exit 2;
    fi
    echo "Using 'sudo' to install Filelink...";
    echo "Enter password below, if it's required:"
    sudo echo > /dev/null;
    install "sudo";
else
    echo "WARNING: we're not recommend to install Filelink as root-user";
    echo "It's may issue secure problems";
    echo "";
    CHOOSE="";
    while [ "${CHOOSE}" == "" ]; do
        # shellcheck disable=SC2162
        read -p "Are you sure? [y/n] >> " CHOOSE
        if [ "${CHOOSE}" == "y" ]; then
            install "";
            echo "Install was successful";
            exit 0;
        elif [ "${CHOOSE}" == "n" ]; then
            echo "Aborted";
            exit 2;
        else
            CHOOSE="";
            continue;
        fi
    done
fi
