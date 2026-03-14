# E-Commerce Recommendation System

A production-ready e-commerce recommendation system built using:
- Django
- Machine Learning (TF-IDF, Cosine Similarity)
- PostgreSQL
- HTML, CSS, JavaScript

## Features
- User authentication
- Product search and filtering
- Content-based recommendations
- Shopping cart and checkout
- Scalable backend architecture

## Tech Stack
- Backend: Django
- ML: Scikit-learn, Pandas
- Database: SQLite / PostgreSQL
- Frontend: HTML, CSS, JS

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-recommendation-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create a `.env` file in the project root:
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   ```

6. **Load product data**
   ```bash
   python manage.py load_products
   ```

7. **Train recommendation model**
   ```bash
   python manage.py train_recommender
   ```

8. **Run the server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `GET /api/recommend/?product=<name>&top_n=<number>` - Get product recommendations

## Status
🚧 Under active development
