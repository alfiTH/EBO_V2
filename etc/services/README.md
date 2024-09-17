# Install service

```bash
# Services
cd /home/robocomp/robocomp/components/EBO_V2/etc/services && sudo cp ./*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable base INA226 ledStrip sensors usb_camera accessPoint
sudo systemctl start base INA226 ledStrip sensors usb_camera accessPoint
sudo systemctl status base INA226 ledStrip sensors usb_camera accessPoint

# Autostart appication
cd /home/robocomp/robocomp/components/EBO_V2/etc/services && sudo chmod +x ./*.desktop && sudo cp ./*.desktop /home/$USER/.config/autostart 
```