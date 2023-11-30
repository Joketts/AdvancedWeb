#!/usr/bin/bash

cat > webtech.service << END
# /etc/systemd/system/helloapp.service
[Unit]
Description=Your App Name
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/home/$USER/YcoaGame
ExecStart=/home/$USER/YcoaGame/bin/waitress-serve --listen=127.0.0.1:5000 Server:app #change your repo with the actual name of your repo
Restart=always

[Install]
WantedBy=multi-user.target
END
