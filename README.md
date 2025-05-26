# 🎬 Movie Watchlist

A simple Python application to manage your personal movie watchlist using [`psycopg2-binary`](https://pypi.org/project/psycopg2-binary/) to interact with a PostgreSQL database.

## 🚀 Features

- Add new movie to the list
- View upcoming movies
- View all movies
- Mark a movie as watched
- View watched movies
- Add user to the app
- Search for a movie

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/lucianomap/movie-watchlist.git
cd movie-watchlist
```

2. Create a virtual environment (optional) 

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies with:

```bash
pip install -r requirements.txt
```

4. Configure the environment variables:

Rename the `.env.example` file to `.env`.
Edit the `.env` file with the appropriate configuration (e.g., PostgreSQL connection settings).

5. Run the application:

```bash
python app.py
```

## 📄 License
This project is open source and available under the MIT License.
