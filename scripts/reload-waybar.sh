#!/usr/bin/env bash
pkill waybar
sleep 0.2
waybar >/tmp/waybar.log 2>&1 &

