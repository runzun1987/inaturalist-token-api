# 🐛 iNaturalist Token Retriever API

This FastAPI project allows users to authenticate with [iNaturalist](https://www.inaturalist.org/) using their email and password, and retrieve an API token that can be used for authenticated requests such as uploading images for species identification.

## 🚀 Features

- CSRF-protected login to iNaturalist
- Session-based authentication handling
- API endpoint to retrieve `Authorization` token
- Fully written in Python with FastAPI

## 📦 Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`
- `fastapi`
- `uvicorn`

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/runzun1987/inaturalist-token-api.git
   cd inaturalist-token-api
