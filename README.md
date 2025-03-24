# smart-restaurant-management-system

# copy .env.example to .env
# copy /frontend_vue/.env.example to /frontend_vue/.env

*   docker-compose up --build -d   
*   docker-compose exec backend flask db init                                         
*   docker-compose exec backend flask db migrate -m "Initial migration"   
*   docker-compose exec backend flask db upgrade
*   docker-compose down -v

*   If issue
    docker-compose build --no-cache
    docker-compose up -d

*   http://localhost:3000     ->  front_end
*   http://localhost:5000     ->  backend

### **Tech Stack:
## **Backend:
- **Flask** (with Flask-RESTful)
- PostgreSQL with **SQLAlchemy** (Flask)
- **SpaCy**for NLP tasks
- **word2number** for converting text (two) to numerals (2)
- fuzzywuzzy for suggestions (menu items): (diet kok -> diet coke)
- inflect : convert plural words to singular : (pizzas -> pizza)
- **Flask-SocketIO** (for Flask) for WebSockets
- Unit tests : pytest

## **Frontend:
- Vue.js 3 (Composition API)
- Vue Router for navigation
- Pinia for state management
- Vuetify for UI components
- Axios for API calls

- **Deployment:
- Docker Compose to containerize frontend, backend, and database
- NGINX as a reverse proxy (optional for production)

1. Registration
<img src="/screenshots/1 Registration.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>