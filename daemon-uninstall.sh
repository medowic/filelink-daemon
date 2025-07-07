#!/usr/bin/bash

function err() {
    echo "Error: couldn't remove ${1} from ${2}"
    echo "failed with exit-code 1"
    exit 1
}

function uninstall() {
    FILELINK_DIR=$(cat /etc/filelink/path)

    systemctl stop filelink

    if [ -d /etc/filelink ]; then
        if ! rm -rf /etc/filelink; then
            err "filelink (folder)" "/etc/";
        fi
    fi

    if [ -f "${FILELINK_DIR}"/config/config.yaml ]; then
        if ! rm "${FILELINK_DIR}"/config/config.yaml; then
            err "config.yaml" "${SCRIPT_DIR}/config/"
        fi
    fi

    if ! wget -O "${FILELINK_DIR}"/config/config.yaml https://raw.githubusercontent.com/medowic/filelink/master/config/config.yaml > /dev/null 2>&1; then
        echo "Error: couldn't download original Filelink config.yaml from Github";
        echo "Check that 'wget' is installed on your machine and try again";
        echo "failed with exit-code 3";
        exit 3;
    fi

    if [ -f /usr/bin/filelink ]; then
        if ! rm /usr/bin/filelink; then
            err "filelink (binary)" "/usr/bin/";
        fi
    fi

    if [ -f /etc/systemd/system/filelink.service ]; then
        if ! rm /etc/systemd/system/filelink.service; then
            err "filelink.service (daemon)" "/etc/systemd/system/";
        fi
    fi

    systemctl daemon-reload
}

if [ "${EUID}" -ne 0 ]; then
    echo "Error: couldn't start uninstallation without root permissions";
    echo "failed with exit-code 2";
    exit 2;
else
    echo ""
    echo "Filelink Daemon uninstall"
    echo ""
    echo "This script will be remove only daemon - main files won't be removed"
    echo ""
    
    CHOOSE=""
    while [ "${CHOOSE}" == "" ]; do
        # shellcheck disable=SC2162
        read -p "Are you sure? [y/n] >> " CHOOSE
        if [ "${CHOOSE}" == "y" ]; then
            uninstall;
            echo "Uninstall was successful";
            echo "Main Filelink Server is still located in ${FILELINK_DIR} directory";
            echo "";
            if ! rm /usr/bin/filelink-uninstall; then
                err "filelink-uninstall (binary)" "/usr/bin/";
            fi
            exit 0;
        elif [ "${CHOOSE}" == "n" ]; then
            echo "Aborted";
            exit 3;
        else
            CHOOSE="";
            continue;
        fi
    done
fi
