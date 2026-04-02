#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -m nltk.downloader punkt stopwords -d /tmp/nltk_data
export NLTK_DATA=/tmp/nltk_data

# Database will be initialized automatically on app startup

echo "Build completed successfully!" 