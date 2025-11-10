#!/bin/bash
echo "🔧 Configuration du haut-parleur Bluetooth"
sudo apt install -y pulseaudio pulseaudio-module-bluetooth bluez-tools
sudo systemctl --user enable pulseaudio
sudo systemctl --user start pulseaudio
echo "👉 Lance 'bluetoothctl' puis 'pair', 'connect' et 'trust' ton haut-parleur."
