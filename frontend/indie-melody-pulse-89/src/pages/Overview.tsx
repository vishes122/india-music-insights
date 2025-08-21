import { useEffect, useState } from 'react';
import { Calendar, Music, TrendingUp, Users, PlayCircle, Sparkles } from 'lucide-react';
import { KPICard } from '@/components/KPICard';
import { TrackTable } from '@/components/TrackTable';
import { apiService, Track } from '@/lib/apiClient';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from '@/hooks/use-toast';
import heroBanner from '@/assets/hero-banner.jpg';

export default function Overview() {
  const [topTracks, setTopTracks] = useState<Track[]>([]);
  const [kpiData, setKpiData] = useState({
    lastSnapshotDate: '',
    totalTracks: 0,
    totalArtists: 0,
    totalGenres: 0,
    tracksGrowth: '+0%',
    artistsGrowth: '+0%',
  });
  const [genreData, setGenreData] = useState<Array<{name: string, percentage: number}>>([]);
  const [topArtists, setTopArtists] = useState<Array<{name: string, track_count: number}>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('[Overview] mounted');
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch all data in parallel
        const [tracksResponse, kpiResponse, genresResponse, artistsResponse] = await Promise.all([
          apiService.getTopToday('IN').catch((error) => {
            console.error('[Overview] Failed to fetch top tracks:', error);
            toast({
              title: "API Connection Error",
              description: `Failed to load today's top tracks: ${error.message}`,
              variant: "destructive",
            });
            return { tracks: [], total: 0, snapshot_id: '', last_updated: '' };
          }),
          apiService.getKPIStats().catch((error) => {
            console.error('[Overview] Failed to fetch KPI stats:', error);
            return {
              lastSnapshotDate: new Date().toISOString(),
              totalTracks: 0,
              totalArtists: 0,
              totalGenres: 0,
              tracksGrowth: '+0%',
              artistsGrowth: '+0%',
            };
          }),
          apiService.getGenreDistribution().catch((error) => {
            console.error('[Overview] Failed to fetch genre distribution:', error);
            return { genres: [], total_tracks: 0, fetched_at: '' };
          }),
          apiService.getTopArtistsByTracks(4).catch((error) => {
            console.error('[Overview] Failed to fetch top artists:', error);
            return { artists: [], total: 0, fetched_at: '' };
          }),
        ]);

        setTopTracks(tracksResponse.tracks?.slice(0, 50) || []);
        setKpiData({
          ...kpiResponse,
          tracksGrowth: kpiResponse.tracksGrowth ?? '+0%',
          artistsGrowth: kpiResponse.artistsGrowth ?? '+0%',
        });
        setGenreData(genresResponse.genres || []);
        setTopArtists(artistsResponse.artists || []);
      } catch (error) {
        console.error('Failed to fetch overview data:', error);
        toast({
          title: "Error loading data",
          description: "Failed to load overview data. Using demo data instead.",
          variant: "destructive",
        });
        
        // Demo data fallback
        setTopTracks([]);
        setKpiData({
          lastSnapshotDate: new Date().toISOString(),
          totalTracks: 55,
          totalArtists: 62,
          totalGenres: 8,
          tracksGrowth: '+12%',
          artistsGrowth: '+8%',
        });
        setGenreData([
          { name: 'Bollywood', percentage: 85 },
          { name: 'Pop', percentage: 70 },
          { name: 'Hip-Hop', percentage: 55 },
          { name: 'Classical', percentage: 40 }
        ]);
        setTopArtists([
          { name: 'Aditya Rikhari', track_count: 11 },
          { name: 'Anuv Jain', track_count: 5 },
          { name: 'Arijit Singh', track_count: 4 },
          { name: 'Faheem Abdullah', track_count: 3 }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      return 'Recently';
    }
  };

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl">
        <div 
          className="h-64 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${heroBanner})` }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/80 to-transparent" />
          <div className="relative h-full flex items-center justify-start p-8">
            <div className="space-y-4 max-w-2xl">
              <div className="flex items-center space-x-3">
                <div className="h-12 w-12 rounded-xl bg-gradient-primary flex items-center justify-center glow-effect">
                  <Sparkles className="h-6 w-6 text-primary-foreground animate-music-note" />
                </div>
                <div>
                  <h1 className="text-4xl font-bold text-foreground">
                    India Music Insights
                  </h1>
                  <p className="text-lg text-muted-foreground">
                    Professional Analytics Dashboard
                  </p>
                </div>
              </div>
              <p className="text-muted-foreground max-w-lg">
                Discover trends, analyze performance, and explore the dynamic landscape 
                of Indian music streaming with real-time data visualization.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="px-6 space-y-8">

      {/* KPI Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {loading ? (
          Array.from({ length: 4 }).map((_, i) => (
            <Card key={i}>
              <CardContent className="p-6">
                <Skeleton className="h-16 w-full" />
              </CardContent>
            </Card>
          ))
        ) : (
          <>
            <KPICard
              title="Last Updated"
              value={formatDate(kpiData.lastSnapshotDate)}
              subtitle="Data snapshot"
              icon={Calendar}
              gradient
            />
            <KPICard
              title="Total Tracks"
              value={kpiData.totalTracks.toLocaleString()}
              subtitle="In database"
              icon={Music}
              trend={{
                value: parseInt(kpiData.tracksGrowth?.replace(/[^0-9]/g, '') || '0'),
                label: "vs last week"
              }}
            />
            <KPICard
              title="Total Artists"
              value={kpiData.totalArtists.toLocaleString()}
              subtitle="Unique artists"
              icon={Users}
              trend={{
                value: parseInt(kpiData.artistsGrowth?.replace(/[^0-9]/g, '') || '0'),
                label: "vs last week"
              }}
            />
            <KPICard
              title="Genres Tracked"
              value={kpiData.totalGenres}
              subtitle="Music categories"
              icon={TrendingUp}
              trend={{
                value: 3,
                label: "vs last week"
              }}
            />
          </>
        )}
      </div>

      {/* Today's Top Tracks */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h2 className="text-2xl font-semibold text-foreground">
              Today's Top 50 - India
            </h2>
            <p className="text-muted-foreground">
              Most popular tracks streaming right now
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="secondary" className="bg-primary/10 text-primary border-primary/20">
              <PlayCircle className="h-3 w-3 mr-1" />
              Live Data
            </Badge>
          </div>
        </div>

        {loading ? (
          <Card>
            <CardHeader>
              <Skeleton className="h-6 w-32" />
            </CardHeader>
            <CardContent className="space-y-4">
              {Array.from({ length: 10 }).map((_, i) => (
                <div key={i} className="flex items-center space-x-4">
                  <Skeleton className="h-12 w-12 rounded-md" />
                  <div className="flex-1 space-y-2">
                    <Skeleton className="h-4 w-48" />
                    <Skeleton className="h-3 w-32" />
                  </div>
                  <Skeleton className="h-4 w-16" />
                </div>
              ))}
            </CardContent>
          </Card>
        ) : topTracks.length > 0 ? (
          <TrackTable
            tracks={topTracks}
            title="Top Tracks"
            showRank
            className="animate-fade-in"
          />
        ) : (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-16 space-y-4">
              <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
                <Music className="h-8 w-8 text-muted-foreground" />
              </div>
              <div className="text-center space-y-2">
                <h3 className="font-semibold text-foreground">No data available</h3>
                <p className="text-muted-foreground">
                  Unable to load today's top tracks. Please check your API connection.
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Quick Stats */}
      {!loading && topTracks.length > 0 && (
        <div className="grid gap-6 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Popular Genres Today</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {genreData.slice(0, 4).map((genre) => (
                  <div key={genre.name} className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">{genre.name}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-16 bg-muted rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full"
                          style={{ width: `${genre.percentage}%` }}
                        />
                      </div>
                      <span className="text-xs text-muted-foreground w-8">
                        {genre.percentage}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Top Artists</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {topArtists.map((artist, i) => (
                  <div key={artist.name} className="flex items-center space-x-3">
                    <span className="text-sm font-mono text-muted-foreground w-4">
                      {i + 1}
                    </span>
                    <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                      <Users className="h-4 w-4 text-primary" />
                    </div>
                    <div className="flex-1">
                      <div className="text-sm text-foreground truncate">
                        {artist.name}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {artist.track_count} tracks
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Trending Now</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                  <span className="text-sm text-foreground">Live streaming data</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 rounded-full bg-music-gold animate-pulse delay-100" />
                  <span className="text-sm text-foreground">Real-time analytics</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 rounded-full bg-music-purple animate-pulse delay-200" />
                  <span className="text-sm text-foreground">Market insights</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 rounded-full bg-music-blue animate-pulse delay-300" />
                  <span className="text-sm text-foreground">Trend analysis</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
      </div>
    </div>
  );
}