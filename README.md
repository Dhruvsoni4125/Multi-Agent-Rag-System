---
title: Multi-Agent RAG System
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Multi-Agent RAG System

A FastAPI-based multi-agent research assistant running on Hugging Face Spaces.

## Interactive API Docs
Once deployed, the Swagger interactive documentation is available at:
`https://dhruvsoni-multi-agent-rag-system.hf.space/docs`

## Local Setup

1. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
2. Start the FastAPI server locally:
   ```bash
   uvicorn main:app --reload
   ```
