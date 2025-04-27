# IPL Stats API Service

This project is a **Flask-based** web application that provides a suite of RESTful APIs to fetch IPL (Indian Premier League) statistics from match and delivery datasets. You can view team records, head-to-head team statistics, batsman career and vs-team records, and bowler career and vs-team records.

## 🔗 Deployment

The application is deployed on **Render.com** and is accessible at:

> [https://ipl-flask-api.onrender.com](https://ipl-flask-api-4oxn.onrender.com)

You can use any of the API endpoints by appending the route to the base URL, for example:

- Team record: [`https://ipl-flask-api.onrender.com/api/team/Mumbai%20Indians`](https://ipl-flask-api-4oxn.onrender.com/api/team/Mumbai%20Indians)
- Batsman record: [`https://ipl-flask-api.onrender.com/api/batsman/MS%20Dhoni`](https://ipl-flask-api-4oxn.onrender.com/api/batsman/MS%20Dhoni)

## 📂 Project Structure

```
ipl-flask-api/
├── app.py               # Main Flask application
├── data/
│   ├── matches.csv      # IPL match-level data
│   └── deliveries.csv   # Delivery-level data
├── templates/
│   └── index.html       # Frontend homepage with API documentation & forms
├── requirements.txt     # Python dependencies
└── runtime.txt          # Python version declaration for Render
```

## 🚀 Getting Started (Local Development)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vishal1230/ipl-flask-api.git
   cd ipl-flask-api
   ```

2. **Create & activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   # Development server
   python app.py
   # Production simulation
   gunicorn app:app
   ```

5. **View in browser**:
   - Homepage & interactive API docs: `http://127.0.0.1:5000/`
   - Swagger-style endpoints: append `/api/...` routes.

## 📖 API Endpoints

| Endpoint                                    | Description                                         |
|---------------------------------------------|-----------------------------------------------------|
| `GET /api/team/<team_name>`                  | Team record
| `GET /api/team_vs/<team1>/<team2>`           | Head-to-head team record                            |
| `GET /api/batsman/<player>`                  | Batsman career record                               |
| `GET /api/batsman_vs/<player>/<team>`        | Batsman vs-team record                              |
| `GET /api/bowler/<player>`                   | Bowler career record                                |
| `GET /api/bowler_vs/<player>/<team>`         | Bowler vs-team record                               |

*(Replace `<…>` with URL-encoded values; e.g. spaces → `%20`)*

## ⚙️ Configuration for Deployment

- **Python version** is specified in `runtime.txt` (e.g., `python-3.10.12`).
- **Start command** on Render: `gunicorn app:app`

## 📋 License

This project is open-source and available under the MIT License. Feel free to clone, modify, and deploy.

---

*Powered by Flask & Render.*

