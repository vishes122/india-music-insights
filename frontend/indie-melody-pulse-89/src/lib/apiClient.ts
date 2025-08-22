import axios from 'axios';

// API Configuration - Debug logging with protocol fix
let API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Ensure protocol is included
if (API_BASE_URL && !API_BASE_URL.startsWith('http')) {
  API_BASE_URL = `https://${API_BASE_URL}`;
}

console.log('[API CLIENT] Environment variables:', {
  VITE_API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
  API_BASE_URL_ORIGINAL: import.meta.env.VITE_API_BASE_URL,
  API_BASE_URL_FIXED: API_BASE_URL,
  fullBaseURL: `${API_BASE_URL}/v1`
});

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/v1`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('[API REQUEST]', config.method?.toUpperCase(), config.url, 'Full URL:', `${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API REQUEST ERROR]', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log('[API SUCCESS]', response.config.method?.toUpperCase(), response.config.url, '→', response.status);
    return response;
  },
  (error) => {
    console.error('[API ERROR] Full error details:', {
      message: error.message,
      code: error.code,
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      method: error.config?.method,
      baseURL: error.config?.baseURL,
      data: error.response?.data,
      headers: error.response?.headers
    });
    
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout');
    } else if (error.response?.status >= 500) {
      console.error('Server error:', error.response.data);
    } else if (error.response?.status === 404) {
      console.error('Endpoint not found:', error.config.url);
    } else {
      console.error('API Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// API Types - Updated to match backend response
export interface Track {
  rank: number;
  track_name: string;
  name?: string; // Some APIs might return 'name' instead of 'track_name'
  artists: string[] | any[]; // Can be array of strings or artist objects
  album?: string;
  album_image_url?: string;
  album_image_width?: number;
  album_image_height?: number;
  release_date?: string;
  popularity: number;
  spotify_url?: string;
  preview_url?: string;
  duration_formatted?: string;
  explicit: boolean;
}

export interface Artist {
  id: string;
  name: string;
  images: Array<{
    url: string;
    height: number;
    width: number;
  }>;
  followers: {
    total: number;
  };
  popularity: number;
  // Enhanced analytics
  track_count?: number;
  avg_popularity?: number;
  external_urls: {
    spotify: string;
  };
  genres: string[];
}

export interface Genre {
  name: string;
  count: number;
  percentage: number;
}

export interface ChartResponse {
  market: string;
  snapshot_date: string;
  total_tracks: number;
  tracks: Track[];
  last_updated: string;
}

export interface SearchResponse {
  artists?: {
    items: Artist[];
    total: number;
  };
  tracks?: {
    items: Track[];
    total: number;
  };
  playlists?: {
    items: any[];
    total: number;
  };
}

// API Functions
export const apiService = {
  // Health Check
  getHealth: async (): Promise<any> => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // Charts
  getTopToday: async (market: string = 'IN'): Promise<ChartResponse> => {
    const response = await apiClient.get(`/charts/top-today?market=${market}`);
    return response.data;
  },

  getTopYear: async (year: number, market: string = 'IN'): Promise<ChartResponse> => {
    const response = await apiClient.get(`/charts/top-year?year=${year}&market=${market}`);
    return response.data;
  },

  // NEW: Historical Search Endpoints
  searchTracksByYear: async (year: number, query: string = '', limit: number = 50): Promise<{
    year: number;
    query: string;
    total: number;
    tracks: Track[];
    limit: number;
    offset: number;
    next_offset?: number;
    fetched_at: string;
  }> => {
    const response = await apiClient.get(`/search/tracks/year/${year}?query=${encodeURIComponent(query)}&limit=${limit}`);
    return response.data;
  },

  searchTracksByYearRange: async (
    startYear: number, 
    endYear: number, 
    query: string = '', 
    limit: number = 50
  ): Promise<{
    year_range: string;
    query: string;
    total: number;
    tracks: Track[];
    limit: number;
    offset: number;
    next_offset?: number;
    fetched_at: string;
  }> => {
    const response = await apiClient.get(`/search/tracks/year-range/${startYear}-${endYear}?query=${encodeURIComponent(query)}&limit=${limit}`);
    return response.data;
  },

  getTopTracksOfYear: async (year: number, genre?: string, limit: number = 50): Promise<{
    year: number;
    genre: string;
    total_found: number;
    tracks: Track[];
    limit: number;
    fetched_at: string;
    note: string;
  }> => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (genre) params.append('genre', genre);
    
    const response = await apiClient.get(`/search/top-of-year/${year}?${params}`);
    return response.data;
  },

  // Artists (Updated to work with backend)
  getTopArtists: async (year: number, market: string = 'IN'): Promise<{ artists: Artist[] }> => {
    // This endpoint might not exist yet - fallback to search
    try {
      const response = await apiClient.get(`/artists/top?year=${year}&market=${market}&include_details=true`);
      const items = response.data?.artists ?? [];
      const artists: Artist[] = items.map((a: any, index: number) => ({
        id: a.id ?? `artist_${index}`,
        name: a.name,
        images: Array.isArray(a.images)
          ? a.images.map((img: any) => ({ url: img.url, height: img.height ?? 0, width: img.width ?? 0 }))
          : [],
        followers: { total: a.followers_total ?? a.followers?.total ?? 0 },
        popularity: a.avg_popularity ?? a.popularity_score ?? a.popularity ?? 0,
        track_count: a.track_count ?? (Array.isArray(a.tracks) ? a.tracks.length : undefined),
        avg_popularity: a.avg_popularity,
        external_urls: { spotify: a.external_urls?.spotify ?? '' },
        genres: Array.isArray(a.genres) ? a.genres : [],
      }));
      return { artists };
    } catch {
      // Fallback: search for artists from that year
      const searchResponse = await apiClient.get(`/search/tracks/year/${year}?query=bollywood&limit=50`);
      const tracks = searchResponse.data.tracks || [];
      
      // Extract unique artists (artists are now strings)
      const artistsSet = new Set<string>();
      tracks.forEach((track: Track) => {
        track.artists.forEach(artistName => {
          artistsSet.add(artistName);
        });
      });
      
      // Convert to artist objects for compatibility
      const artists = Array.from(artistsSet).slice(0, 20).map((name, index) => ({
        id: `artist_${index}`,
        name,
        popularity: 75,
        followers: { total: 100000 },
        images: [],
        genres: ['Bollywood'],
        external_urls: { spotify: `https://open.spotify.com/search/${encodeURIComponent(name)}` }
      }));
      
      return { artists };
    }
  },

  getArtistTopTracks: async (id: string, market: string = 'IN'): Promise<{ tracks: Track[] }> => {
    const response = await apiClient.get(`/artists/${id}/top-tracks?market=${market}`);
    return response.data;
  },

  // Real Analytics Endpoints
  getAnalyticsOverview: async (market: string = 'IN'): Promise<{
    total_tracks: number;
    total_artists: number;
    total_snapshots: number;
    tracks_growth: string;
    artists_growth: string;
    genres_tracked: number;
    last_updated: string;
  }> => {
    const response = await apiClient.get(`/analytics/overview?market=${market}`);
    return response.data;
  },

  getTopArtistsByTracks: async (limit: number = 10): Promise<{
    artists: Array<{name: string, track_count: number}>;
    total: number;
    fetched_at: string;
  }> => {
    const response = await apiClient.get(`/analytics/top-artists?limit=${limit}`);
    return response.data;
  },

  getGenreDistribution: async (): Promise<{
    genres: Array<{name: string, percentage: number, count: number}>;
    total_tracks: number;
    fetched_at: string;
  }> => {
    const response = await apiClient.get(`/analytics/genres`);
    return response.data;
  },

  getArtistDetails: async (id: string): Promise<Artist> => {
    const response = await apiClient.get(`/artists/${id}`);
    return response.data;
  },

  // Genres (Mock data for now)
  getTopGenres: async (year: number, market: string = 'IN'): Promise<{ genres: Genre[] }> => {
    // Mock data since we don't have this endpoint yet
    return {
      genres: [
        { name: 'Bollywood', count: 45, percentage: 35.2 },
        { name: 'Hindi Pop', count: 32, percentage: 25.0 },
        { name: 'Indian Classical', count: 18, percentage: 14.1 },
        { name: 'Indie', count: 15, percentage: 11.7 },
        { name: 'Punjabi', count: 12, percentage: 9.4 },
        { name: 'Folk', count: 6, percentage: 4.7 }
      ]
    };
  },

  // Search - Updated for historical capability
  search: async (
    query: string, 
    type: 'artist' | 'track' | 'playlist' = 'track',
    limit: number = 20,
    year?: number
  ): Promise<SearchResponse> => {
    if (year && type === 'track') {
      // Use historical search for tracks with year
      const response = await apiService.searchTracksByYear(year, query, limit);
      return {
        tracks: {
          items: response.tracks,
          total: response.total
        }
      };
    }
    
    // Fallback to general search (mock for now)
    return {
      tracks: { items: [], total: 0 },
      artists: { items: [], total: 0 },
      playlists: { items: [], total: 0 }
    };
  },

  // Compare (Real)
  compareGenres: async (markets: string[] = ['IN', 'US', 'GB']): Promise<{
    year: number;
    markets: string[];
    genres: Array<{ name: string; markets: Record<string, number> }>;
    fetched_at: string;
  }> => {
    const params = new URLSearchParams();
    markets.forEach(m => params.append('markets', m));
    const response = await apiClient.get(`/analytics/compare-genres?${params.toString()}`);
    return response.data;
  },

  // Analytics
  getKPIStats: async (): Promise<{
    lastSnapshotDate: string;
    totalTracks: number;
    totalArtists: number;
    totalGenres: number;
    tracksGrowth?: string;
    artistsGrowth?: string;
  }> => {
    try {
      const analyticsResponse = await apiService.getAnalyticsOverview();
      return {
        lastSnapshotDate: analyticsResponse.last_updated,
        totalTracks: analyticsResponse.total_tracks,
        totalArtists: analyticsResponse.total_artists,
        totalGenres: analyticsResponse.genres_tracked,
        tracksGrowth: analyticsResponse.tracks_growth,
        artistsGrowth: analyticsResponse.artists_growth
      };
    } catch (error) {
      console.error('Failed to fetch real analytics:', error);
      return {
        lastSnapshotDate: new Date().toISOString(),
        totalTracks: 55,
        totalArtists: 62,
        totalGenres: 8
      };
    }
  },

  // NEW: Ingest data (for admin)
  ingestData: async (adminKey: string): Promise<any> => {
    const response = await apiClient.post('/charts/ingest', {}, {
      headers: { 'X-Admin-Key': adminKey }
    });
    return response.data;
  }
};

export default apiClient;