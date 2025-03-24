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
- User Authentication: Flask-JWT-Extended
- **SpaCy**for NLP tasks
- **word2number** for converting text (two) to numerals (2)
- **fuzzywuzzy** for suggestions (menu items): (diet kok -> diet coke)
- **inflect** : convert plural words to singular : (pizzas -> pizza)
- **Flask-SocketIO** (for Flask) for WebSockets
- Unit tests : pytest

## **Frontend:
- Vue.js 3 (Composition API)
- Vue Router for navigation
- Pinia for state management
- Vuetify for UI components
- Axios for API calls
- Toast for Success and Error messages
- ApexCharts for popular items, peak hours, and sales trends

- **Deployment:
- Docker Compose to containerize frontend, backend, and database
- NGINX as a reverse proxy (optional for production)

## Screenshots
1. Registration
<img src="/screenshots/1 Registration.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
2. Login
<img src="/screenshots/2 Login.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
3. Size
<img src="/screenshots/3 Size.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
4. Type
<img src="/screenshots/4 Type.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
5.Modifier
<img src="/screenshots/5 Modifier.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
6.Add Item
<img src="/screenshots/6 Add Item.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
7. Menu
<img src="/screenshots/7 Menu.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
8. Place Order with suggestion 
<img src="/screenshots/8 order .png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
<img src="/screenshots/order a.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
Live Order Display 
<img src="/screenshots/order b.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>

9. All Orders
<img src="/screenshots/10_all_orders.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>
<img src="/screenshots/10_all_orders_1.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>

10. Report with charts
<img src="/screenshots/9 report.png" alt="MarineGEO circle logo" style="height: 600px; width:800px;"/>