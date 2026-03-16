# Smart Notes Generator

An NLP-based system that converts PDF, Word, and PowerPoint documents into structured study notes and exam-oriented questions.

## Features

- Multi-format document ingestion (Supported formats: PDF, DOCX, PPTX)
- Automatic concept extraction
- Structured notes generation
- Exam question generation
- Chat with notes using RAG

## Tech Stack

Python, PyMuPDF, spaCy, HuggingFace Transformers, FAISS, Streamlit

## Project Architecture

Document → Text Extraction → NLP Processing → Notes Generation → Question Generation → RAG Chat

## Installation

Clone the repository

git clone https://github.com/YOUR_USERNAME/smart-notes-generator.git

Create virtual environment

python -m venv venv

Activate environment

Windows:
venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

## Run

python extraction/pdf_parser.py