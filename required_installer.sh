#!/bin/bash

required_libraries=("pillow" "pytesseract" "pyautogui")
required_packages=("tesseract-ocr")

echo "[!] Goose installer started."
echo "[!] Installing python libraries..."

for library in "${required_libraries[@]}";
do
    echo "[!] Installing $library..."
    pip install $library --break-system-packages
done

echo "[!] Installing packages..."

for package in "${required_packages[@]}";
do
    echo "[!] Installing $package..."
    sudo apt install $package -y
done