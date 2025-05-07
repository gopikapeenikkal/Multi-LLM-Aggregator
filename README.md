# Multi-LLM Aggregator

A Python application that leverages multiple Large Language Models (LLMs) through Together.ai's platform to generate comprehensive responses by aggregating outputs from different models.

## Overview

This project implements a system that:
1. Processes user queries through multiple high-performance LLMs concurrently
2. Aggregates and synthesizes the responses using a meta-model
3. Provides a unified, high-quality response that benefits from multiple model perspectives

## Features

- Concurrent execution of multiple LLM queries using asyncio
- Utilizes three powerful models:
  - Qwen/Qwen2-72B-Instruct
  - meta-llama/Llama-3.3-70B-Instruct-Turbo
  - mistralai/Mixtral-8x22B-Instruct-v0.1
- Response aggregation using Mixtral-8x22B-Instruct-v0.1
- Streaming output support for real-time response generation

## Prerequisites

- Python 3.10 or higher
- Together.ai API key
- Required Python packages (specified in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd multi_llm