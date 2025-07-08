#!/usr/bin/env python3

import urllib.request
import yaml
import subprocess

from os.path import exists
from sys import exit as sys_exit, argv

systemd_flags = ["start", "stop", "restart"]

def help(code=0):
    print("\nFilelink Server (Daemon)")
    print("repository: https://github.com/medowic/filelink\n")
    print("Commands:")
    print(" * help      -   Show this page and exit")
    print(" * version   -   Show Filelink version and exit")
    print(" * update    -   Checking for new updates from Github")
    print(" * config    -   Edit Filelink configuration with preferred editor")
    print(" * setpath   -   Set new path to folder for sharing")
    print(" * start     -   Start Filelink Server")
    print(" * restart   -   Restart Filelink")
    print(" * stop      -   Stop Filelink Server\n")
    print("This is software is under the MIT License (https://github.com/medowic/filelink/LICENSE)\n")

    sys_exit(code)

def version():
    with open(f"{workdir}/version/version.data", "r", encoding="utf-8") as file:
        version_main_local = file.read()
        version_main_local = version_main_local.strip()
    with open(f"{workdir}/version/version_daemon.data", "r", encoding="utf-8") as file:
        version_daemon_local = file.read()
        version_daemon_local = version_daemon_local.strip()

    print("\nFilelink Server (Daemon)")
    print("repository: https://github.com/medowic/filelink\n")
    print("Versions:")
    print(f" * Filelink: {version_main_local}")
    print(f" * Filelink Daemon: {version_daemon_local}\n")
    print("You can check new available versions by running 'filelink update'\n")

    sys_exit(0)

def update():
    print("Checking for updates...\n")
    with urllib.request.urlopen('https://raw.githubusercontent.com/medowic/filelink-daemon/master/version/version.data') as response:
        version_daemon = response.read().decode('utf-8')
        version_daemon = version_daemon.strip()
    with urllib.request.urlopen('https://raw.githubusercontent.com/medowic/filelink/master/version/version.data') as response:
        version_main = response.read().decode('utf-8')
        version_main = version_main.strip()

    with open(f"{workdir}/version/version.data", "r", encoding="utf-8") as file:
        version_main_local = file.read()
        version_main_local = version_main_local.strip()
    with open(f"{workdir}/version/version_daemon.data", "r", encoding="utf-8") as file:
        version_daemon_local = file.read()
        version_daemon_local = version_daemon_local.strip()

    if not version_main_local == version_main:
        print(f"New version of Filelink available ({version_main}) [current: {version_main_local}]")
        print("You can download it from https://github.com/medowic/filelink\n")
    
    if not version_daemon_local == version_daemon:
        print(f"New version of Filelink-Daemon available ({version_daemon}) [current: {version_daemon_local}]")
        print("You can download it from https://github.com/medowic/filelink-daemon")
        print("Or update automatically by running these commands below:\n")
        print(f"cd {workdir}")
        print("wget -O daemon-install.sh https://raw.githubusercontent.com/medowic/filelink-daemon/master/daemon-install.sh")
        print("bash daemon-install.sh\n")

    if version_main_local == version_main and version_daemon_local == version_daemon:
        print("You're up-to-date! No updates available\n")
    
    sys_exit(0)

def config():
    if not exists(f"{workdir}/config/editor"):
        print("Choose preferred editor")
        print(f"This settings will be saved. You can change it into '{workdir}/config/editor' file\n")
        print("[1] Nano (/usr/bin/nano)")
        print("[2] Vim (/usr/bin/vim)")
        print("[3] Custom editor\n")

        choose = None
        while not choose:
            try:
                choose = str(input("Input number in range 1-3 >> "))
            except KeyboardInterrupt:
                print()
                sys_exit(0)
            if choose == "1":
                with open(f"{workdir}/config/editor", "w", encoding="utf-8") as file:
                    editor = "/usr/bin/nano"
                    file.write(editor)
            elif choose == "2":
                with open(f"{workdir}/config/editor", "w", encoding="utf-8") as file:
                    editor = "/usr/bin/vim"
                    file.write(editor)
            elif choose == "3":
                editor = None
                while not editor:
                    try:
                        editor = str(input("Set path to your editor (CTRL+C to abort) >> "))
                    except KeyboardInterrupt:
                        print()
                        sys_exit(0)
                    if editor and not exists(editor):
                        print("\nIt's looks likes path isn't exists")
                        print("Check path name and try again")
                        editor = None
                        continue
                    with open(f"{workdir}/config/editor", "w", encoding="utf-8") as file:
                        file.write(editor)
            else:
                choose = None
                continue
    else:
        with open(f"{workdir}/config/editor", "r", encoding="utf-8") as file:
            editor = file.read()
            editor = editor.strip()
    
    subprocess.run([editor, f"{workdir}/config/config.yaml"])
    sys_exit(0)

def setpath():
    new_path = None
    print("Set new folder for Filelink (CTRL+C to abort):")
    while not new_path:
        try:
            new_path = str(input(">> "))
        except KeyboardInterrupt:
            print()
            sys_exit(0)
        if new_path and not exists(new_path):
            print("\nIt's looks likes path isn't exists. It may issue HTTP 500 error")
            print("Check path name and try again (CTRL+C to abort)")
            new_path = None
            continue

    with open(f"{workdir}/config/daemon.source", "w", encoding="utf-8") as file:
        file.write(f"FILELINK_PATH={new_path}")

    sys_exit(0)

def systemd(cmd):
    try:
        subprocess.check_call(
            ["systemctl", cmd, "filelink"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if cmd == "start":
            print("Filelink Server was started")
            print("Run 'filelink' for show configuration")
        elif cmd == "stop":
            print("Filelink Server was stopped")
        sys_exit(0)
    except subprocess.CalledProcessError as Error:
        print(f"Something went wrong: Filelink couldn't {cmd}")
        print(f"Error: {Error}")
        sys_exit(1)

with open("/etc/filelink/path", "r", encoding="utf-8") as file:
    workdir = file.read()
    workdir = workdir.strip()

try:
    if argv[1] == "help": help()
    elif argv[1] == "version": version()
    elif argv[1] == "update": update()
    elif argv[1] == "config": config()
    elif argv[1] == "setpath": setpath()
    elif argv[1] in systemd_flags: systemd(argv[1])
    else:
        print(f"Couldn't find '{argv[1]}' command")
        help(2)
except IndexError:
    pass

try:
    subprocess.check_call(
        ["systemctl", "is-active", "filelink"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Filelink Server is running\n")
except:
    print("Filelink Server is disabled")
    sys_exit(1)

with open(f"{workdir}/config/config.yaml", "r", encoding="utf-8") as file:
    config_yaml = yaml.load(file, Loader=yaml.SafeLoader)

filelink_host = str(config_yaml["server"]["address"])
filelink_port = int(config_yaml["server"]["port"])

with open(f"{workdir}/config/daemon.source", "r", encoding="utf-8") as file:
    filelink_path = file.read()
    filelink_path = filelink_path.split("=")
    filelink_path = filelink_path[1].strip()

with open(f"{workdir}/tmp/daemon.yaml.tmp", "r", encoding="utf-8") as file:
    daemon_yaml_tmp = yaml.load(file, Loader=yaml.SafeLoader)

filelink_provider = str(daemon_yaml_tmp["provider"])
filelink_secure = str(daemon_yaml_tmp["secure"])

print("Debug:")
if filelink_host == "0.0.0.0":
    print(f" * Running on all addresses ({filelink_host})")
    print(f" * Running on http://127.0.0.1:{filelink_port}")
else:
    print(f" * Running on http://{filelink_host}:{filelink_port}")

print("\nConfiguration:")
print(f" * Folder: {filelink_path}")
print(f" * Host: {filelink_provider}")
print(f" * Passkey: {filelink_secure}")
print("\nFor getting info about commands, run 'filelink help'")
sys_exit(0)