#!/usr/bin/env bash

printf "\nExecuting: sudo apt-get update\n"
sudo apt-get update

printf "\nExecuting: sudo apt-get upgrade -y\n"
sudo apt-get upgrade -y

printf "\nInstalling Node and Npm via nvm\n"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# TODO: 1 aggiungere disclaimer al README dicendo che verrà installata sempre l'ultima versione di node
nvm install --lts --latest-npm node

npm install