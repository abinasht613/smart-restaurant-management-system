# smart-restaurant-management-system
python -m backend.app

# copy .env.example to .env

*   docker-compose up --build -d   
*   docker-compose exec backend flask db init                                         
*   docker-compose exec backend flask db migrate -m "Initial migration"   
*   docker-compose exec backend flask db upgrade
*   docker-compose down -v

*   If issue
    docker-compose build --no-cache
    docker-compose up -d

*   http://localhost:81     ->  front_end
*   http://localhost:81/api ->  backend