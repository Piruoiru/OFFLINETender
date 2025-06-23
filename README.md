<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">


# OFFLINETENDER

<em>Transform Data Into Action, Instantly and Seamlessly</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/Piruoiru/OFFLINETender?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Piruoiru/OFFLINETender?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/Piruoiru/OFFLINETender?style=flat&color=0080ff" alt="repo-language-count">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white" alt="JSON">
<img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="Markdown">
<img src="https://img.shields.io/badge/Filament-%23FDAE4B.svg?style=flat&logo=Filament&logoColor=white" alt="Filament" />
<img src="https://img.shields.io/badge/npm-CB3837.svg?style=flat&logo=npm&logoColor=white" alt="npm">
<img src="https://img.shields.io/badge/Composer-885630.svg?style=flat&logo=Composer&logoColor=white" alt="Composer">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=flat&logo=JavaScript&logoColor=black" alt="JavaScript">
<img src="https://img.shields.io/badge/Scrapy-60A839.svg?style=flat&logo=Scrapy&logoColor=white" alt="Scrapy">
<br>
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/XML-005FAD.svg?style=flat&logo=XML&logoColor=white" alt="XML">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/PHP-777BB4.svg?style=flat&logo=PHP&logoColor=white" alt="PHP">
<img src="https://img.shields.io/badge/Vite-646CFF.svg?style=flat&logo=Vite&logoColor=white" alt="Vite">
<img src="https://img.shields.io/badge/Axios-5A29E4.svg?style=flat&logo=Axios&logoColor=white" alt="Axios">
<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
<img src="https://img.shields.io/badge/Laravel-%23CB171E.svg?style=flat&logo=Laravel&logoColor=white" alt="Laravel" />

</div>
<br>

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Accessing the Application](#accessing-the-application)
- [Return to Top](#top)

## Overview

**OFFLINETENDER** is a full-stack application that ingests documents and data, applies advanced processing (**PDF parsing**, **web scraping**, **LLM-powered analysis**, **vector search**), and provides actionable output through RESTful APIs and a modern **Filament** dashboard.

---

## Getting Started

### Features

- **Document Parsing:** Extract text and metadata from PDF files.
- **Web Scraping:** Collect and normalize data from target websites using Scrapy.
- **LLM Integration:** Leverage local or hosted language models via Ollama.
- **Vector Search:** Fast similarity search with FAISS and PostgreSQL pgvector.
- **Dashboard:** Admin panel built with Laravel, Filament, and Livewire.
- **API Endpoints:** Flask-based microservice for data clients.
- **Containerization:** Docker Compose setup for consistent development and deployment.

### Tech Stack

- **Backend (Python):** Flask, Scrapy, LangChain Community, FAISS, PyJWT
- **Frontend (Laravel):** PHP 8.2+, Laravel 12, Filament 3, Livewire 3, Tailwind CSS,   Vite, Axios
- **Database:** PostgreSQL 17 with pgvector extension
- **Containerization:** Docker, Docker Compose
- **Environment:** Python 3.11, Node.js (LTS), Composer, npm

### Prerequisites

- **Python 3.11+**
- **PHP 8.2+**
- **Composer**
- **Node.js (LTS) and npm**
- **Docker & Docker Compose**
- **PostgreSQL 17 with pgvector extension**

### Installation

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/Piruoiru/OFFLINETender
    ```

2. **Using [Herd](https://herd.laravel.com/windows):**

Open the Herd app, go to **Sites** > **Add** > **Link Existing Project**, and select the **laravelProject directory**.

**Using [Docker](https://hub.docker.com/_/postgres):**
```sh
docker run --name offlinetenderdb \
  -e POSTGRES_PASSWORD=POSTGRES_PASSWORD \
  -p 5433:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:17
```
Environment variables, such as **POSTGRES_PASSWORD**, are defined in the project’s .env file.


### Configuration

1. **PHP DEPENDENCIES**
```sh
-  php ^8.2
-  laravel/framework ^12.0
-  filament/filament ^3.3
-  laravel/sanctum ^4.0
-  laravel/tinker ^2.10.1
-  livewire/livewire ^3.6
```

2. **PYTHON DEPENDENCIES**
```sh
- PyPDF2
- scrapy
- requests
- ollama
- python-dotenv
- litellm
- flask
- langchain_community
- faiss-cpu
- PyJWT
- psycopg2-binary
- pgvector[psycopg2]
```
3. **Laravel** 
- Copy laravelProject/.env.example to laravelProject/.env.

- Set database credentials (**host**: postgres, **port**: 5432, **user**: postgres, **password**: from .env).

4. **PostgreSQL**
- Ensure the pgvector extension is enabled:
```sh
CREATE EXTENSION IF NOT EXISTS vector;
```
5. **FlaskApp**
- Copy Project/.env.example to Project/.env.
- Configure any model paths or secrets.

### Usage


**Using [Flask](https://www.npmjs.com/):**

Open the project, run the command: 

```sh
python .\Project\UseCases\API.py
```

### Accessing the Application

- **Laravel Dashboard:** [http://localhost:8000](http://localhost:8000)
- **Flask API:** [http://localhost:5000](http://localhost:5000)


---

<div align="left"><a href="#top">⬆ Return</a></div>

---
