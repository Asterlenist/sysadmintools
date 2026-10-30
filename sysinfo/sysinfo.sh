#!/bin/bash

echo "System Information"
echo "------------------"
echo "Hostname: $(hostname)"
echo "Operating System: $(uname -o)"
echo "Kernel Version: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "CPU: $(lscpu | grep 'Model name' | awk -F: '{print $2}' | xargs)"
echo "Total Memory: $(free -h | awk '/^Mem:/ {print $2}')"
echo "Available Memory: $(free -h | awk '/^Mem:/ {print $7}')"
echo "Disk Usage:"
df -h | awk 'NR==1 || /^\/dev\// {print $0}'
echo "Network Interfaces:"
ip -o link show | awk -F': ' '{print $2}'
echo "------------------"