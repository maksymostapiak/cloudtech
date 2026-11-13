#!/bin/bash

echo "Встановлюємо AWS CLI..."
curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -q awscliv2.zip
sudo ./aws/install

echo "Прибираємо сміття..."
rm -rf aws awscliv2.zip

echo "Налаштовуємо тестові ключі..."
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set default.region us-east-1
aws configure set default.output json

echo "Готово! AWS CLI встановлено та налаштовано."