#!/bin/bash
#
# Configures display and audio output
#
# Usage:
#
#  call with mode (LCD or HDMI) to set the appropriate config
#  call with no parameter for autodetection and automatic rebooting
#  if necessary

# where is this script and it's configs installed?
ROOT="/home/pi/retroportable"

# print an error message and exit the script
die() {
	echo "ERROR: $1" >&2
	exit 1
}

# detect which configuration is currently active
detectConfig() {
	if grep -q 'mode:LCD' '/boot/config.txt'; then
		echo 'LCD'
	elif grep -q 'mode:HDMI' '/boot/config.txt'; then
		echo 'HDMI'
	else
		echo 'unknown'
	fi
}

# detect if a device is available on HDMI
detectDevice() {
	if tvservice -n 2>/dev/null |grep -q 'device_name='; then
		echo 'HDMI'
	else
		echo 'LCD'
	fi
}

# set the configuration for the given mode
setMode() {
	local MODE=$1
	cat "$ROOT/config.BASE" "$ROOT/config.$MODE" > /boot/config.txt \
		|| die "could not write boot configuration"

	cat "$ROOT/asound.BASE" "$ROOT/asound.$MODE" > /etc/asound.conf \
		|| die "could not write sound configuration"
	
	echo "Set output to $MODE"
}

# MAIN

CONFIGURED=$(detectConfig)
DETECTED=$(detectDevice)

echo "Current mode is $CONFIGURED"
echo "Detected mode is $DETECTED"

if [ -z "$1" ]; then
	if [ "$CONFIGURED" != "$DETECTED" ]; then
		setMode "$DETECTED"
		echo "rebooting..."
		/sbin/reboot
	else
		echo "nothing to do"
	fi
else
	setMode "$1"
fi
