echo "User Information"
echo "------------------"
echo "Current User: $(whoami)"
echo "User ID: $(id -u)"
echo "Group ID: $(id -g)"
echo "Home Directory: $HOME"
echo "Shell: $SHELL"
echo "------------------"
echo "User Groups:"
groups $(whoami) | awk -F: '{print $2}' | tr ' '
echo "------------------"
echo "Last Login:"
last -n 1 $(whoami) | awk '{print $4, $5, $6, $7}'
echo "------------------"
echo "User Processes:"
ps -u $(whoami) -o pid,ppid,cmd,%mem,%cpu
echo "------------------"
echo "Environment Variables:"
printenv | sort
echo "------------------"
echo "User Permissions:"
if [ -r "$HOME" ]; then
    echo "Read permission on home directory: Yes"
else
    echo "Read permission on home directory: No"
fi
if [ -w "$HOME" ]; then
    echo "Write permission on home directory: Yes"
else
    echo "Write permission on home directory: No"
fi
if [ -x "$HOME" ]; then
    echo "Execute permission on home directory: Yes"
else
    echo "Execute permission on home directory: No"
fi
echo "------------------"
echo "User Disk Usage:"
du -sh $HOME 2>/dev/null || echo "Unable to determine disk usage for home directory."
echo "------------------"
echo "User Login History:"
last -n 5 $(whoami) | awk '{print $4, $5, $6, $7}'
echo "------------------"
echo "User Account Expiration:"
chage -l $(whoami) | grep "Account expires" | awk -F: '{print $2}' | xargs
echo "------------------"