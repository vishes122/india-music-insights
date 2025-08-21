# Project Structure & Organization

## Root Directory Layout
```
untitled folder/                           # Project container
├── india-music-insights/                  # Backend FastAPI application
│   ├── app/                              # Core application code
│   ├── alembic/                          # Database migrations
│   ├── tests/                            # Test suite
│   ├── requirements.txt                  # Python dependencies
│   ├── .env                             # Environment configuration
│   ├── docker-compose.yml               # Container orchestration
│   └── india_music_insights.db          # SQLite database file
├── frontend/indie-melody-pulse-89/        # Frontend React application
│   ├── src/                             # Source code
│   ├── public/                          # Static assets
│   ├── dist/                            # Build output
│   ├── node_modules/                    # Node dependencies
│   └── package.json                     # Node.js configuration
└── .kiro/                               # Kiro steering configuration
    └── steering/                        # AI assistant guidance
```

## Backend Architecture (`india-music-insights/`)

### **Core Application Layer (`app/`)**

#### **Application Bootstrap (`main.py`)**
- **FastAPI App Factory**: Creates configured FastAPI instance with middleware stack
- **Lifespan Management**: Handles startup/shutdown with database initialization and scheduler management
- **Middleware Stack**: CORS, request context, trusted host (production), and global exception handling
- **Router Registration**: Modular endpoint organization with versioned API structure
- **Documentation**: Automatic OpenAPI/Swagger documentation at `/docs` and `/redoc`
- **Health Monitoring**: Root endpoint with API information and health check integration

#### **Configuration Management (`config.py`)**
- **Pydantic Settings**: Type-safe environment variable loading with validation
- **Market Configuration**: Multi-market support with timezone and currency mapping
- **Playlist Management**: Market-specific playlist ID configuration and retrieval
- **Environment Detection**: Development/production mode detection with appropriate defaults
- **Security Settings**: Admin key management and CORS origin configuration

#### **Database Layer (`db.py`)**
- **SQLAlchemy Engine**: Async-capable database engine with connection pooling
- **Session Management**: Context-managed database sessions with automatic cleanup
- **Initialization**: Database table creation and schema setup
- **Connection Lifecycle**: Proper connection opening/closing with error handling

#### **Dependency Injection (`deps.py`)**
- **Database Sessions**: Scoped session management for request lifecycle
- **External Clients**: Spotify API client provisioning with authentication
- **Validation Dependencies**: Market, year, limit, and search type validation
- **Security Dependencies**: Admin key verification for privileged operations
- **Common Dependency Groups**: Pre-configured dependency combinations for different endpoint types

### **API Layer (`app/routers/`)**

#### **Health Monitoring (`health.py`)**
- **Basic Health Check**: Simple endpoint for service availability monitoring
- **Database Connectivity**: Validates database connection and query capability
- **External Service Status**: Checks Spotify API connectivity and authentication

#### **Core Music API (`charts.py`)**
- **Today's Charts**: Latest playlist snapshots with caching and market filtering
- **Historical Charts**: Yearly aggregated statistics with fallback computation
- **Search Endpoints**: Multi-year track search with Spotify API integration
- **Analytics Endpoints**: Real-time KPIs, artist rankings, genre distribution, and cross-market comparisons
- **Admin Operations**: Manual data ingestion triggers with authentication
- **Response Models**: Pydantic schemas for consistent API responses
- **Error Handling**: Comprehensive exception handling with structured error responses
- **Performance Optimization**: Intelligent caching and query optimization

### **Data Layer (`app/models/`)**

#### **Base Model (`base.py`)**
- **Declarative Base**: SQLAlchemy base class with shared functionality
- **Common Fields**: Automatic ID, created_at, and updated_at fields
- **Timestamp Management**: Automatic timestamp handling for audit trails

#### **Core Entities (`track.py`)**
- **Artist Model**: Complete artist metadata with Spotify integration
  - Spotify ID, name, popularity, followers, genres (JSON), external URLs, image URLs
  - Relationships to tracks via many-to-many association
  - Property methods for genre list access and data transformation
- **Track Model**: Comprehensive track information with audio features
  - Spotify ID, name, album, release date, duration, explicit flag, popularity
  - Audio features (danceability, energy, valence, tempo) for future analysis
  - Relationships to artists and playlist snapshots
  - Property methods for artist names and release year extraction
- **Playlist Model**: Market-specific playlist tracking
  - Spotify ID, name, market, description, external URLs, image URLs
  - Relationship to snapshots for historical tracking
- **PlaylistTrackSnapshot Model**: Time-series playlist state capture
  - Playlist/track relationships with snapshot date and rank
  - Metadata including fetch time and track addition time
  - Unique constraints preventing duplicate snapshots
  - Indexes for efficient querying by date and rank

#### **Association Tables**
- **track_artists**: Many-to-many relationship between tracks and artists
- **Composite Keys**: Efficient relationship management with proper indexing

### **Business Logic Layer (`app/services/`)**

#### **Data Ingestion Service (`ingest.py`)**
- **Playlist Processing**: Complete workflow for Spotify playlist data ingestion
- **Artist/Track Upserts**: Intelligent data merging with conflict resolution
- **Relationship Management**: Many-to-many relationship synchronization
- **Snapshot Creation**: Daily playlist state capture with metadata
- **Error Recovery**: Robust error handling with partial success reporting
- **Performance Metrics**: Detailed ingestion statistics and timing
- **Transaction Management**: Atomic operations with rollback capability

### **External Integration Layer (`app/clients/`)**

#### **Spotify API Client (`spotify.py`)**
- **Authentication Management**: OAuth2 client credentials flow with token refresh
- **HTTP Client**: Async HTTP client with connection pooling and timeout handling
- **Rate Limiting**: Automatic 429 response handling with exponential backoff
- **Retry Logic**: Configurable retry attempts with circuit breaker patterns
- **Request/Response Logging**: Comprehensive API interaction logging
- **Error Classification**: Structured exception handling with status code mapping
- **Search Capabilities**: Advanced search with year filtering and market specification
- **Playlist Operations**: Efficient playlist track retrieval with field selection

### **Utility Layer (`app/utils/`)**

#### **Logging Infrastructure (`logging.py`)**
- **Structured Logging**: JSON-formatted logs with request correlation
- **Request Context**: Automatic request ID generation and propagation
- **Performance Tracking**: Response time measurement and slow query detection
- **Error Correlation**: Exception tracking with full context preservation
- **Log Levels**: Environment-appropriate logging configuration

#### **Caching System (`caching.py`)**
- **Redis Integration**: High-performance caching with TTL management
- **Cache Key Generation**: Consistent key naming with parameter hashing
- **Invalidation Strategies**: Smart cache invalidation based on data changes
- **Fallback Handling**: Graceful degradation when cache is unavailable

#### **Time Management (`time.py`)**
- **Timezone Handling**: Market-specific timezone conversion and management
- **Date Utilities**: Consistent date formatting and parsing across the application

### **Infrastructure & Configuration**

#### **Database Migrations (`alembic/`)**
- **Version Control**: Database schema versioning with migration scripts
- **Environment Management**: Separate migration configurations for different environments
- **Rollback Capability**: Safe schema changes with rollback procedures

#### **Testing Framework (`tests/`)**
- **Unit Tests**: Comprehensive test coverage for business logic
- **Integration Tests**: End-to-end API testing with database fixtures
- **Mock Services**: External service mocking for reliable testing

## Frontend Architecture (`frontend/indie-melody-pulse-89/`)

### **Application Entry Points**

#### **HTML Entry (`index.html`)**
- **SEO Optimization**: Complete meta tag configuration for search engines
- **Social Media**: Open Graph and Twitter Card meta tags
- **PWA Support**: Web app manifest and service worker registration
- **Performance**: Preload hints and resource optimization
- **Accessibility**: Proper semantic HTML structure and ARIA labels

#### **React Bootstrap (`src/main.tsx`)**
- **React 18 Features**: Concurrent rendering with createRoot
- **Global Styles**: Tailwind CSS and custom CSS variable imports
- **Router Setup**: Browser router configuration with error boundaries
- **Provider Wrapping**: Context providers for theme, query client, and global state

### **Page Components (`src/pages/`)**

#### **Overview Dashboard (`Overview.tsx`)**
- **Data Fetching**: Parallel API calls with TanStack Query for optimal performance
- **KPI Display**: Real-time metrics with trend indicators and growth calculations
- **Chart Visualization**: Today's Top 50 with interactive track table
- **Genre Analytics**: Distribution charts with percentage breakdowns
- **Artist Rankings**: Top artists by track count with visual indicators
- **Error Handling**: Graceful fallbacks with demo data when API unavailable
- **Loading States**: Skeleton components for smooth user experience

#### **Market Comparison (`Compare.tsx`)**
- **Cross-Market Analysis**: Side-by-side genre comparison across markets
- **Interactive Charts**: Multi-series bar charts with hover states and tooltips
- **Market Selection**: Dynamic market filtering with real-time updates
- **Data Insights**: Automated insight generation based on comparison results

### **Component Library (`src/components/`)**

#### **Data Display Components**
- **TrackTable (`TrackTable.tsx`)**: Sophisticated track listing with ranking, play controls, and metadata
  - Responsive design with mobile-optimized layouts
  - Audio preview integration with play/pause controls
  - Artist name handling with proper fallbacks
  - Album artwork with error handling and placeholders
  - Popularity indicators and release date formatting
- **KPICard (`KPICard.tsx`)**: Metric display with trend visualization
  - Gradient backgrounds and icon integration
  - Trend arrows with color-coded indicators
  - Responsive typography and spacing

#### **Layout Components**
- **Layout (`Layout.tsx`)**: Application shell with navigation and responsive design
- **Footer (`Footer.tsx`)**: Site footer with links and branding
- **AudioPreview (`AudioPreview.tsx`)**: Spotify audio preview integration with controls

#### **UI Primitives (`src/components/ui/`)**
- **shadcn/ui Components**: Complete set of accessible, customizable UI components
- **Card System**: Flexible card layouts with headers, content, and footers
- **Form Controls**: Input fields, buttons, selects with validation states
- **Navigation**: Menus, tabs, breadcrumbs with keyboard navigation
- **Feedback**: Toasts, alerts, loading states with animation
- **Data Display**: Tables, lists, badges with sorting and filtering

### **API Integration Layer (`src/lib/`)**

#### **HTTP Client (`apiClient.ts`)**
- **Axios Configuration**: Centralized HTTP client with interceptors and timeout handling
- **TypeScript Integration**: Full type safety with interface definitions matching backend schemas
- **Error Handling**: Comprehensive error classification and user-friendly messages
- **Request/Response Transformation**: Consistent data shape handling
- **Caching Strategy**: HTTP-level caching with cache-control headers
- **Retry Logic**: Automatic retry for transient failures
- **API Methods**: Complete coverage of backend endpoints with proper typing
  - Chart endpoints (today, yearly, historical search)
  - Analytics endpoints (overview, artists, genres, comparisons)
  - Search functionality with year filtering
  - Admin operations with authentication

#### **Utility Functions (`utils.ts`)**
- **Class Name Utilities**: Tailwind class merging and conditional styling
- **Date Formatting**: Consistent date/time formatting across components
- **Data Transformation**: Helper functions for API response processing

### **Custom Hooks (`src/hooks/`)**

#### **UI Interaction Hooks**
- **Toast Management (`use-toast.ts`)**: Centralized notification system with queuing
- **Responsive Design (`use-mobile.ts`)**: Breakpoint detection and responsive behavior
- **Form Handling**: Custom hooks for form validation and submission

### **Configuration & Build System**

#### **Build Configuration (`vite.config.ts`)**
- **Development Server**: Hot module replacement with proxy configuration
- **Build Optimization**: Code splitting, tree shaking, and asset optimization
- **Plugin Configuration**: React SWC for fast compilation
- **Path Resolution**: Absolute imports with @ alias for clean imports

#### **Styling Configuration (`tailwind.config.ts`)**
- **Design System**: Custom color palette with CSS variables for theming
- **Typography**: Font family configuration with web font optimization
- **Animations**: Custom keyframes for smooth interactions and loading states
- **Responsive Design**: Mobile-first breakpoint system
- **Component Variants**: Class variance authority for component styling
- **Dark Mode**: CSS variable-based theming with system preference detection

#### **TypeScript Configuration**
- **Strict Mode**: Full type checking with strict compiler options
- **Path Mapping**: Absolute imports with proper IDE support
- **Environment Types**: Vite environment variable typing
- **Component Types**: React component prop typing with generic support

### **Static Assets (`public/`)**
- **Favicon Suite**: Multiple favicon formats for cross-platform support
- **PWA Manifest**: Web app manifest for mobile installation
- **SEO Files**: Robots.txt and sitemap.xml for search engine optimization
- **Social Media**: Open Graph images and Twitter Card assets

## Architectural Patterns & Best Practices

### **Backend Design Patterns**

#### **Repository Pattern**
- **Data Access Layer**: SQLAlchemy models serve as repositories with query methods
- **Business Logic Separation**: Services layer handles complex operations
- **Transaction Management**: Proper session handling with rollback capabilities

#### **Dependency Injection**
- **FastAPI Dependencies**: Leverages FastAPI's dependency injection for clean architecture
- **Service Composition**: Services receive dependencies through constructor injection
- **Testing Support**: Easy mocking and testing through dependency substitution

#### **Service Layer Pattern**
- **Business Logic Encapsulation**: Complex operations isolated in service classes
- **External Integration**: API clients abstracted behind service interfaces
- **Error Handling**: Centralized error handling with proper exception propagation

#### **Client Abstraction Pattern**
- **External API Wrapper**: Spotify client provides clean interface to external services
- **Retry Logic**: Built-in resilience patterns for external service failures
- **Authentication Management**: Automatic token handling and refresh

### **Frontend Design Patterns**

#### **Component Composition**
- **Atomic Design**: Components built from small, reusable primitives
- **Prop Drilling Avoidance**: Context and custom hooks for state management
- **Render Props**: Flexible component composition with render functions

#### **Custom Hook Pattern**
- **Logic Encapsulation**: Business logic extracted into reusable hooks
- **State Management**: Local state management with proper cleanup
- **Side Effect Management**: useEffect patterns for API calls and subscriptions

#### **API Client Pattern**
- **Centralized HTTP Logic**: Single source of truth for API communication
- **Type Safety**: Full TypeScript integration with backend schema matching
- **Error Boundary Integration**: Proper error propagation to UI error boundaries

#### **Route-based Code Splitting**
- **Lazy Loading**: Pages loaded on-demand for optimal bundle size
- **Suspense Integration**: Loading states handled through React Suspense
- **Error Boundaries**: Route-level error handling with fallback UI

### **Data Flow Architecture**

#### **Ingestion Pipeline**
1. **Scheduler Trigger**: APScheduler initiates daily ingestion jobs
2. **Spotify API Fetch**: Client retrieves playlist data with retry logic
3. **Data Processing**: Service layer processes and normalizes data
4. **Database Storage**: Atomic transactions store normalized entities
5. **Cache Invalidation**: Relevant caches cleared for fresh data

#### **API Request Flow**
1. **Request Validation**: FastAPI validates request parameters and headers
2. **Dependency Injection**: Database sessions and clients provided
3. **Business Logic**: Service layer processes request with caching
4. **Response Serialization**: Pydantic models ensure consistent response format
5. **Error Handling**: Structured error responses with proper HTTP status codes

#### **Frontend Data Flow**
1. **User Interaction**: UI events trigger API calls through event handlers
2. **API Client**: Centralized client handles HTTP communication with error handling
3. **State Management**: TanStack Query manages server state with caching
4. **Component Updates**: React re-renders components based on state changes
5. **Error Display**: Error boundaries and toast notifications handle failures

### **File Naming & Organization Conventions**

#### **Backend Conventions**
- **Python Files**: snake_case for modules and functions (`user_service.py`)
- **Class Names**: PascalCase for classes (`UserService`, `TrackModel`)
- **Constants**: UPPER_SNAKE_CASE for constants (`API_BASE_URL`)
- **Database Tables**: lowercase with underscores (`playlist_track_snapshots`)
- **API Endpoints**: kebab-case with versioning (`/v1/charts/top-today`)

#### **Frontend Conventions**
- **Components**: PascalCase for React components (`TrackTable.tsx`)
- **Hooks**: camelCase with 'use' prefix (`useTrackData.ts`)
- **Utilities**: camelCase for utility functions (`formatDuration.ts`)
- **Constants**: UPPER_SNAKE_CASE for constants (`API_BASE_URL`)
- **CSS Classes**: kebab-case following Tailwind conventions

#### **Configuration Files**
- **Environment**: lowercase with dots (`.env`, `.env.local`)
- **Config Files**: lowercase with extensions (`vite.config.ts`, `tailwind.config.ts`)
- **Package Files**: lowercase (`package.json`, `requirements.txt`)

### **Security & Performance Considerations**

#### **Backend Security**
- **Input Validation**: Pydantic models validate all input data
- **SQL Injection Prevention**: SQLAlchemy ORM prevents direct SQL injection
- **Authentication**: Admin key-based authentication for privileged operations
- **CORS Configuration**: Environment-specific origin allowlisting

#### **Frontend Security**
- **XSS Prevention**: React's built-in XSS protection through JSX
- **Content Security Policy**: Proper CSP headers for production deployment
- **Environment Variables**: Sensitive data kept in environment variables
- **API Key Protection**: No sensitive keys exposed in client-side code

#### **Performance Optimization**
- **Database Indexing**: Strategic indexes on frequently queried columns
- **Caching Strategy**: Multi-layer caching with Redis and HTTP caches
- **Code Splitting**: Route-based and component-based code splitting
- **Asset Optimization**: Image optimization and lazy loading
- **Bundle Analysis**: Regular bundle size monitoring and optimization