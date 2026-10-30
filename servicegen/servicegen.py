 #!/usr/bin/env python3

# [Unit]
# Description={description}
# After={example: network.target}
#
# [Service]
# Type={example: simple}
# User={example: root}
# WorkingDirectory={example: /opt/myapp}
# ExecStart={example: /opt/myapp/app_binary}
# Restart={example: always}
# RestartSec={example: 5}
#
# [Install]
# WantedBy={example: multi-user.target}

import os
import subprocess

version = "v0.1"

print("SERVICEGEN ", version)

name = input("What's the name of your service? [example: name.service] ")
description = input("What's the description of your service? [example: My Service] ")
after = input("What should this service start after? [example: network.target] ")
service_type = input("What type of service is this? [example: simple] ")
user = input("What user should this service run as? [example: root] ")
working_directory = input("What is the working directory for this service? [example: /opt/myapp] ")
exec_start = input("What is the command to start this service? [example: /opt/myapp/app_binary] ")
restart = input("Should this service restart on failure? [example: always] ")
restart_sec = input("How many seconds should it wait before restarting? [example: 5] ")
wanted_by = input("What target should this service be wanted by? [example: multi-user.target] ")

print(f"\nYour service configuration ({name}):")
print("---------------------------")
print("[Unit]")
print(f"Description: {description}")
print(f"After: {after}")
print(" ")
print("[Service]")
print(f"Type: {service_type}")
print(f"User: {user}")
print(f"WorkingDirectory: {working_directory}")
print(f"ExecStart: {exec_start}")
print(f"Restart: {restart}")
print(f"RestartSec: {restart_sec}")
print(" ")
print("[Install]")
print(f"WantedBy: {wanted_by}")

print("How to install this service:")
print(f"1. Save the configuration to /etc/systemd/system/{name}")
print(f"2. Run `sudo systemctl daemon-reload`")
print(f"3. Run `sudo systemctl enable {name}`")
print(f"4. Run `sudo systemctl start {name}`")

print("Have a nice day!")