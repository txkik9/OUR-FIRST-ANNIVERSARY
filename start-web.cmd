@echo off
cd /d "%~dp0"
echo Open http://127.0.0.1:9871/letmecheck.html in your browser.
echo Keep this window open while using the website. Press Ctrl+C to stop.
python serve_diary.py
