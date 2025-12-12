#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive
export CI=true

# Install wget
sudo apt-get update
sudo apt-get install -y wget

# Install Yarn
npm install -g yarn
corepack enable

# Configure Yarn and Zsh in user home
(
    cd ~
    yarn set version berry
    mkdir -p ~/.oh-my-zsh/custom/themes
    wget https://raw.githubusercontent.com/Riverscapes/environment/master/nar-ys.zsh-theme -O ~/.oh-my-zsh/custom/themes/nar-ys.zsh-theme
    wget https://raw.githubusercontent.com/Riverscapes/environment/master/.aliases -O ~/.aliases
    wget https://raw.githubusercontent.com/Riverscapes/environment/master/.zshrc -O ~/.zshrc
)

# Install Python dependencies
sudo pip install uv
sudo uv pip install --system -e .[dev]
