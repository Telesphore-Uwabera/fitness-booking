# Fitness Booking System

A Django-based fitness booking system with Docker, GitHub Actions, and Ansible deployment.

## Project Structure
```
fitness_booking/
├── app/                   
│   ├── Dockerfile        
│   ├── requirements.txt   
│   └── fitness_booking/   
├── docker-compose.yml     
├── .github/               
│   └── workflows/
│       ├── ci.yml       
│       └── cd.yml       
└── ansible/             
    ├── playbook.yml      
    ├── hosts            
    └── group_vars/     
```

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/telesphore-uwabera/fitness_booking.git
cd fitness_booking
```

2. Start the development environment:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:8000
- API: http://localhost:8000/api
- Admin: http://localhost:8000/admin

## Deployment

1. Production Server:
- IP: 146.190.158.14
- User: ubuntu
- Ports: 80, 443, 8000

2. Deployment Process:
```bash
# Using Ansible
ansible-playbook -i ansible/hosts ansible/playbook.yml --limit production
```

## Port Management
- 8000: Django development server
- 80: Nginx (HTTP)
- 443: Nginx (HTTPS)
- 5432: PostgreSQL
- 6379: Redis

## Environment Variables
Create a `.env` file in the app directory:
```env
DEBUG=True
SECRET_KEY=secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=fitness_booking
DB_USER=fitness_booking
DB_PASSWORD=db-password
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
```

## GitHub Workflow
- CI: Runs on every push to main branch
- CD: Deploys to production on tagged releases

## Features

- User authentication and registration
- Fitness class management
- Class scheduling and booking
- Email notifications for bookings and reminders
- Membership management
- Payment processing

## Tech Stack

- Django 4.2
- PostgreSQL
- Redis
- Celery
- Docker & Docker Compose
- Nginx
- GitHub Actions
- Ansible

## Prerequisites

- Docker and Docker Compose
- Python 3.11
- Git
- Ansible (for deployment)

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ALU-BSE/devops-challenge-Telesphore-Uwabera.git
   cd fitness-booking
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```
   DEBUG=True
   DJANGO_SECRET_KEY=secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   POSTGRES_PASSWORD=db-password
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Access the application at http://localhost:8000

## Deployment

The application is configured for automated deployment using GitHub Actions and Ansible.

### Required Secrets

Add the following secrets to the GitHub repository:

- `DJANGO_SECRET_KEY`: Django secret key
- `POSTGRES_PASSWORD`: PostgreSQL password
- `DOCKER_HUB_USERNAME`: Docker Hub username
- `DOCKER_HUB_TOKEN`: Docker Hub access token
- `SSH_PRIVATE_KEY`: SSH private key for server access

### Deployment Process

1. Push changes to the main branch
2. GitHub Actions will:
   - Run tests
   - Build Docker images
   - Push images to Docker Hub
   - Deploy to the server using Ansible

## Server Configuration

The application is deployed to: 146.190.158.14

### Port Configuration

- Nginx: 80
- Django: 8000
- PostgreSQL: 5432
- Redis: 6379
- MailHog: 1025 (SMTP), 8025 (Web UI)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit the changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
