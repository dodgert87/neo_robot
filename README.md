a# NAO Robot Backend

A modular and scalable backend system for handling user interactions with the NAO robot using OpenAI, WeatherAPI, and NewsData.io. The system processes natural language queries and generates AI-driven responses across multiple domains such as weather, news, jokes, stories, and general knowledge.

---

##  Project Structure

```
nao-robot-backend/
├── app/
│   ├── core/               # Enums, config, language, error codes
│   ├── database/           # SQLAlchemy models and DB services
│   ├── routes/             # API endpoints (chat, db)
│   ├── services/           # Core logic (AI, weather, news, sessions, etc.)
│   └── utils/              # Helper utilities (text cleaning, ID generation)
├── .env                    # Environment config (NOT tracked in Git)
├── requirements.txt        # Dependencies
└── README.md               # Project overview
```

---

##  How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/nao-robot-backend.git
   cd nao-robot-backend
   ```

2. **Create a `.env` File**
   Place this file in the project root (same level as `app/`):

   ```
   ENVIRONMENT=development
   OPENAI_API_KEY_NAO_ROBOT=your-openai-api-key
   DATABASE_URL=sqlite:///./nao_backend.db
   WEATHER_API_URL=https://api.weatherapi.com/v1/current.json
   WEATHER_API_KEY=your-weather-api-key
   NEWS_API_KEY=your-news-api-key
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**
   ```bash
   uvicorn app.main:app --reload
   ```

---

##  Environment Security

- Your `.env` file is **excluded from Git** for security reasons.
- Make sure to never commit credentials or keys to the repository.

---

##  Features

- OpenAI GPT-powered query interpretation and response
- Weather and news fetching using external APIs
- Query tagging, history tracking, and structured response generation
- Stateless and session-based chat management

---

##  License

This project is licensed under the MIT License. See `LICENSE` for details.
