# Technology Stack & Build System

## Backend Architecture (FastAPI + Python)

### **Core Framework & Runtime**
- **FastAPI 0.104.0+**: Modern async web framework with automatic OpenAPI documentation
- **Python 3.9+**: Required minimum version for modern async/await patterns and type hints
- **Uvicorn**: ASGI server with hot reload support and production-ready performance
- **Pydantic 2.4.0+**: Data validation and settings management with type safety

### **Database Layer**
- **SQLAlchemy 2.0+**: Modern ORM with async support and declarative base patterns
- **SQLite**: Primary database with file-based storage (`india_music_insights.db`)
- **Alembic 1.12.0+**: Database migration management and version control
- **Connection Pooling**: Managed through SQLAlchemy engine configuration

### **External Integrations**
- **Spotify Web API**: Primary data source with OAuth2 client credentials flow
- **HTTPX 0.25.0+**: Async HTTP client for Spotify API communication with retry logic
- **Rate Limiting**: Built-in handling for Spotify's 429 responses with exponential backoff
- **Token Management**: Automatic access token refresh and caching

### **Caching & Performance**
- **Redis 5.0.0+**: In-memory caching for API responses and computed results
- **Cache Strategy**: TTL-based caching with intelligent invalidation
- **Query Optimization**: Database indexes on frequently queried columns
- **Response Compression**: Automatic gzip compression for large payloads

### **Scheduling & Background Jobs**
- **APScheduler 3.10.0+**: Cron-like job scheduling for automated data ingestion
- **Timezone Support**: Market-specific scheduling with pytz integration
- **Job Persistence**: Redis-backed job store for reliability
- **Error Handling**: Automatic retry logic with exponential backoff

### **Logging & Monitoring**
- **Structlog 23.1.0+**: Structured JSON logging with request correlation IDs
- **Request Context**: Automatic request tracking and performance metrics
- **Error Tracking**: Comprehensive exception logging with stack traces
- **Performance Monitoring**: Response time tracking and slow query detection

### **Security & Authentication**
- **Admin Key Authentication**: Header-based authentication for privileged operations
- **CORS Configuration**: Environment-specific origin allowlisting
- **Input Validation**: Pydantic-based request/response validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents direct SQL injection

## Frontend Architecture (React + TypeScript)

### **Core Framework & Build System**
- **React 18.3.1**: Modern React with concurrent features and automatic batching
- **TypeScript 5.8.3+**: Full type safety with strict configuration
- **Vite 5.4.19**: Lightning-fast build tool with HMR and optimized production builds
- **SWC Plugin**: Rust-based compilation for faster development builds

### **UI Framework & Styling**
- **shadcn/ui**: Comprehensive component library built on Radix UI primitives
- **Radix UI**: Accessible, unstyled UI components with full keyboard navigation
- **Tailwind CSS 3.4.17**: Utility-first CSS framework with custom design system
- **CSS Variables**: Dynamic theming with HSL color space for consistent design
- **Custom Animations**: Tailwind-based keyframe animations for smooth interactions

### **State Management & Data Fetching**
- **TanStack Query 5.83.0**: Server state management with caching, background updates, and optimistic updates
- **React Hook Form 7.61.1**: Performant form handling with validation
- **Zod 3.25.76**: Runtime type validation and schema definition
- **Local State**: React hooks (useState, useReducer) for component-level state

### **HTTP Client & API Integration**
- **Axios 1.11.0**: Promise-based HTTP client with interceptors and automatic JSON handling
- **Request Interceptors**: Automatic error handling and retry logic
- **Response Transformation**: Consistent data shape transformation
- **Timeout Handling**: 30-second timeout with graceful error messages

### **Routing & Navigation**
- **React Router DOM 6.30.1**: Declarative routing with nested routes and lazy loading
- **Route-based Code Splitting**: Automatic bundle splitting by page
- **Navigation Guards**: Protected routes with authentication checks
- **URL State Management**: Query parameters for shareable application state

### **Development Tools & Quality**
- **ESLint 9.32.0**: Code linting with React and TypeScript rules
- **TypeScript ESLint**: Strict type checking and code quality enforcement
- **Vite Dev Server**: Hot module replacement with instant feedback
- **Source Maps**: Full debugging support in development and production

## Development Commands & Workflows

### **Backend Development (from `india-music-insights/`)**
```bash
# Environment Setup
cp .env.sample .env  # Configure environment variables
pip install -r requirements.txt

# Database Management
python create_tables.py  # Initialize database schema
alembic upgrade head     # Run migrations
alembic revision --autogenerate -m "description"  # Create migration

# Development Server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
# Alternative with environment variables
uvicorn app.main:app --reload --port 8001

# Testing & Quality
pytest                    # Run test suite
pytest --cov=app        # Run with coverage
black app/              # Format code
flake8 app/             # Lint code
isort app/              # Sort imports

# Production Deployment
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### **Frontend Development (from `frontend/indie-melody-pulse-89/`)**
```bash
# Dependency Management
npm install              # Install dependencies
npm audit fix           # Fix security vulnerabilities
npm update              # Update dependencies

# Development Server
npm run dev             # Start dev server (port 8080)
npm run dev -- --port 3000  # Custom port

# Build & Deployment
npm run build           # Production build
npm run build:dev       # Development build
npm run preview         # Preview production build
npm run lint            # ESLint checking
npm run lint -- --fix  # Auto-fix linting issues

# Component Development
npx shadcn-ui add button  # Add new shadcn component
```

## Environment Configuration

### **Backend Environment Variables (.env)**
```bash
# Required Configuration
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
DATABASE_URL=sqlite:///./india_music_insights.db
ADMIN_KEY=your_secure_admin_key

# Optional Configuration
MARKETS=IN,US,GB                    # Comma-separated market codes
ENABLE_SCHEDULER=True               # Enable automated ingestion
REDIS_URL=redis://localhost:6379    # Redis connection string
TIMEZONE=Asia/Kolkata               # Default timezone
LOG_LEVEL=INFO                      # Logging level
ENV=development                     # Environment mode

# Playlist Configuration
INDIA_TOP50_PLAYLIST_ID=37i9dQZEVXbLZ52XmnySJg
GLOBAL_TOP50_PLAYLIST_ID=37i9dQZEVXbMDoHDwVN2tF

# Performance Tuning
CACHE_TTL=300                       # Cache TTL in seconds
RATE_LIMIT_PER_MINUTE=100          # API rate limiting
```

### **Frontend Environment Variables (.env.local)**
```bash
# API Configuration
VITE_API_BASE_URL=http://127.0.0.1:8001  # Backend API URL

# Development Configuration
VITE_DEV_MODE=true                        # Enable dev features
VITE_LOG_LEVEL=debug                      # Console logging level
```

## Key Libraries & Dependencies

### **Backend Dependencies (requirements.txt)**
```python
# Core Framework
fastapi>=0.104.0                    # Web framework
uvicorn[standard]>=0.24.0          # ASGI server
python-multipart>=0.0.6           # Form data handling

# Database & ORM
sqlalchemy>=2.0.0                  # Database ORM
alembic>=1.12.0                    # Database migrations
psycopg2-binary>=2.9.7             # PostgreSQL driver (future)

# HTTP & API Clients
httpx>=0.25.0                      # Async HTTP client
requests>=2.31.0                   # Sync HTTP client

# Data Validation & Configuration
pydantic>=2.4.0                    # Data validation
pydantic-settings>=2.0.0           # Settings management
python-dotenv>=1.0.0               # Environment variables

# Caching & Performance
redis>=5.0.0                       # Redis client
python-redis-cache>=0.1.0          # Redis caching utilities

# Scheduling & Background Jobs
APScheduler>=3.10.0                # Job scheduling

# Utilities
pytz>=2023.3                       # Timezone handling
structlog>=23.1.0                  # Structured logging
colorlog>=6.7.0                    # Colored console logging

# Development & Testing
pytest>=7.4.0                      # Testing framework
pytest-asyncio>=0.21.0             # Async testing
faker>=19.6.0                      # Test data generation
black>=23.0.0                      # Code formatting
flake8>=6.0.0                      # Code linting
isort>=5.12.0                      # Import sorting
```

### **Frontend Dependencies (package.json)**
```json
{
  "dependencies": {
    // Core Framework
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "typescript": "^5.8.3",
    
    // UI Framework
    "@radix-ui/react-*": "^1.x.x",    // UI primitives
    "class-variance-authority": "^0.7.1", // Component variants
    "clsx": "^2.1.1",                 // Conditional classes
    "tailwind-merge": "^2.6.0",       // Tailwind class merging
    "tailwindcss-animate": "^1.0.7",  // Animation utilities
    
    // State Management
    "@tanstack/react-query": "^5.83.0", // Server state
    "react-hook-form": "^7.61.1",     // Form handling
    "zod": "^3.25.76",                // Schema validation
    
    // HTTP & API
    "axios": "^1.11.0",               // HTTP client
    
    // Routing
    "react-router-dom": "^6.30.1",    // Client routing
    
    // Data Visualization
    "recharts": "^3.1.2",             // Charts and graphs
    
    // Utilities
    "date-fns": "^3.6.0",             // Date manipulation
    "lodash-es": "^4.17.21",          // Utility functions
    "lucide-react": "^0.462.0"        // Icon library
  },
  
  "devDependencies": {
    // Build Tools
    "@vitejs/plugin-react-swc": "^3.11.0", // Vite React plugin
    "vite": "^5.4.19",                // Build tool
    
    // Styling
    "tailwindcss": "^3.4.17",         // CSS framework
    "autoprefixer": "^10.4.21",       // CSS prefixing
    "postcss": "^8.5.6",              // CSS processing
    
    // Linting & Quality
    "eslint": "^9.32.0",              // Code linting
    "typescript-eslint": "^8.38.0",   // TypeScript linting
    "@types/node": "^22.16.5",        // Node.js types
    "@types/react": "^18.3.23",       // React types
    "@types/react-dom": "^18.3.7"     // React DOM types
  }
}
```

## Database Schema & Architecture

### **Core Entity Models**
- **Artists**: Spotify artist data with popularity, followers, genres, and external URLs
- **Tracks**: Complete track metadata including audio features, release dates, and popularity
- **Playlists**: Market-specific playlist tracking with metadata and external references
- **PlaylistTrackSnapshots**: Time-series data capturing daily playlist states with rankings

### **Relationship Patterns**
- **Many-to-Many**: Tracks ↔ Artists via `track_artists` association table
- **One-to-Many**: Playlists → PlaylistTrackSnapshots for historical tracking
- **One-to-Many**: Tracks → PlaylistTrackSnapshots for track appearance history

### **Indexing Strategy**
- **Primary Indexes**: All tables have auto-incrementing primary keys
- **Unique Constraints**: Spotify IDs are unique across their respective tables
- **Composite Indexes**: (playlist_id, track_id, snapshot_date) for efficient snapshot queries
- **Performance Indexes**: snapshot_date, rank, market for fast chart queries

### **Data Integrity**
- **Foreign Key Constraints**: Enforce referential integrity across all relationships
- **Unique Constraints**: Prevent duplicate snapshots and maintain data consistency
- **Validation**: Pydantic models ensure data type correctness and business rule compliance