#!/bin/bash

echo "Package Information"
echo "------------------"
echo "Installed Packages:"
dpkg -l | awk '{print $2, $3}' | column -t
echo "------------------"
echo "Package Updates:"
if [ -x "$(command -v apt)" ]; then
    apt list --upgradable 2>/dev/null | awk 'NR>1 {print $1, $2}' | column -t
else
    echo "Package manager not supported for update check."
fi
echo "------------------"
echo "Package Sources:"
if [ -f /etc/apt/sources.list ]; then
    echo "APT Sources:"
    cat /etc/apt/sources.list | grep -v '^#' | awk '{print $1, $2, $3}' | column -t
else
    echo "APT sources list not found."
fi
echo "------------------"
echo "Package Dependencies:"
if [ -x "$(command -v apt)" ]; then
    echo "Enter package name to check dependencies:"
    read package_name
    apt-cache depends "$package_name" 2>/dev/null | awk '/Depends:/ {print $2}' | column -t
else
    echo "Package manager not supported for dependency check."
fi
echo "------------------"
echo "Package Conflicts:"
if [ -x "$(command -v apt)" ]; then
    echo "Enter package name to check conflicts:"
    read package_name
    apt-cache show "$package_name" 2>/dev/null | grep -i 'Conflicts' | awk -F: '{print $2}' | xargs
else
    echo "Package manager not supported for conflict check."
fi
echo "------------------"
echo "Package Vulnerabilities:"
if [ -x "$(command -v apt)" ]; then
    echo "Enter package name to check vulnerabilities:"
    read package_name
    apt-cache show "$package_name" 2>/dev/null | grep -i 'Vulnerabilities' | awk -F: '{print $2}' | xargs
else
    echo "Package manager not supported for vulnerability check."
fi
echo "------------------"