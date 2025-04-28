# Quran/Kuran

This repository contains Quranic text in simple, accessible formats for developers and researchers.

This project generates static HTML pages  of Quran content using Python scripts.  
It processes `quran_content.json` & posts/*.md files and creates formatted HTML files like `index.html`, `index_1.html`, etc.

A simple Python-based application to manage, display verses from the Quran. The project uses **Flask** , **Jinja2 templates** , and **JSON** data files to create a lightweight and functional system for interacting with Turkish/English Quranic text.

I will be using the project files on my personal web site.

### Structure

- **Posts Folder**: Contains generated htmls and related md files.
    
- **Python Scripts**: (`generate_quran.py`, `generate_gw_v2.py`, etc.) are used to format and export Quran content into HTML.
    
- **Data**: `quran_content.json` holds the Quran title, summary, tags and location of md files used in generating htmls.
    
- **Output**: Static HTML files ready for web publishing.
    

### Usage

Simply run any of the `generate_*.py` scripts to recreate or customize the HTML output.