# Tech Companies Israel

A platform to explore the Israeli tech ecosystem, including companies, jobs, and insights. Built with Python, PostgreSQL, and Streamlit.

## Overview

This platform helps users:
- Discover and explore Israeli tech companies
- Find job opportunities in the tech sector
- Analyze market trends and insights
- Get ML-powered recommendations

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or conda for package management

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tech-companies-israel.git
cd tech-companies-israel
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```bash
# Create .env file from template
cp .env.example .env

# Edit with your values
TCI_ENV=development
TCI_POSTGRES_USER=your_user
TCI_POSTGRES_PASSWORD=your_password
TCI_POSTGRES_HOST=localhost
TCI_POSTGRES_PORT=5432
TCI_POSTGRES_DB=tci
TCI_SECRET_KEY=your-secure-secret-key  # Change this in production!
```

5. Initialize the database:
```bash
# Create PostgreSQL database
createdb tci

# Run migrations
python scripts/init_database.py
```

6. Create an admin user (optional):
```bash
python scripts/create_admin.py
# Default credentials:
# Email: admin@example.com
# Password: admin123
```

## Running the App

1. Start the development server:
```bash
streamlit run tci/web/app.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## Project Structure

```
tech-companies-israel/
├── tci/                    # Main package
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality and config
│   ├── db/                # Database models and connections
│   ├── services/          # Business logic
│   └── web/               # Streamlit web interface
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Features

### Current
- User authentication with JWT
- Company explorer with search and filters
- Basic job board functionality
- PostgreSQL database integration

### Coming Soon
- Advanced company search with ML
- Job recommendations
- Market analytics dashboard
- Company similarity engine
- Trend analysis and insights

## Development

### Running Tests
```bash
pytest
```

### Code Style
We follow PEP 8 guidelines. Format your code using:
```bash
black .
isort .
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Israeli tech community
- Streamlit team for the amazing framework
- All contributors and supporters