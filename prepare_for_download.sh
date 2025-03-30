#!/bin/bash

# This script prepares a zip file of the project for deployment

# Create a zip file of the project
cd /home/ubuntu
zip -r whatsapp-restaurant-bot.zip whatsapp-restaurant-bot

echo "Project has been zipped to /home/ubuntu/whatsapp-restaurant-bot.zip"
echo "You can download this file and deploy it using one of the methods described."
