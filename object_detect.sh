#!/bin/bash
cd ComputerVisionProcessing/
python getImage.py
OUTPUT="$(python ComputerVision2.py)"
echo "${OUTPUT}"
afplay file.wav
