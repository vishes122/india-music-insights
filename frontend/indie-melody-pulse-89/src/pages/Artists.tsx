import { useState, useEffect } from 'react';
import { Music, ExternalLink, Users, TrendingUp, Heart } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { apiService, Artist } from '@/lib/apiClient';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from '@/hooks/use-toast';

export default function Artists() {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [selectedMarket, setSelectedMarket] = useState('IN');
  const [loading, setLoading] = useState(false);
  const [filteredArtists, setFilteredArtists] = useState<Artist[]>([]);

  const years = Array.from({ length: 26 }, (_, i) => 2025 - i);
  const markets = [
    { value: 'IN', label: 'India', flag: '🇮🇳' },
    { value: 'US', label: 'United States', flag: '🇺🇸' },
    { value: 'GB', label: 'United Kingdom', flag: '🇬🇧' },
    { value: 'CA', label: 'Canada', flag: '🇨🇦' },
    { value: 'AU', label: 'Australia', flag: '🇦🇺' },
  ];

  const fetchArtists = async () => {
    setLoading(true);
    try {
            const response = await apiService.getTopArtists(selectedYear, selectedMarket);
            let artistsData = Array.isArray(response.artists) ? response.artists : [];
      
      // If no data from API, use demo data
      const demoArtists: Artist[] = [
        {
          id: 'demo-1',
          name: 'Arijit Singh',
          images: [{ url: '/placeholder.svg', height: 640, width: 640 }],
          followers: { total: 15000000 },
          popularity: 95,
          external_urls: { spotify: '#' },
          genres: ['Bollywood', 'Playback Singing']
        },
        {
          id: 'demo-2', 
          name: 'A.R. Rahman',
          images: [{ url: '/placeholder.svg', height: 640, width: 640 }],
          followers: { total: 8500000 },
          popularity: 92,
          external_urls: { spotify: '#' },
          genres: ['Film Score', 'World Music']
        },
        {
          id: 'demo-3',
          name: 'Shreya Ghoshal',
          images: [{ url: '/placeholder.svg', height: 640, width: 640 }],
          followers: { total: 12000000 },
          popularity: 90,
          external_urls: { spotify: '#' },
          genres: ['Bollywood', 'Classical']
        },
        {
          id: 'demo-4',
          name: 'Badshah',
          images: [{ url: '/placeholder.svg', height: 640, width: 640 }],
          followers: { total: 9800000 },
          popularity: 88,
          external_urls: { spotify: '#' },
          genres: ['Hip-Hop', 'Punjabi']
        },
        {
          id: 'demo-5',
          name: 'Armaan Malik',
          images: [{ url: '/placeholder.svg', height: 640, width: 640 }],
          followers: { total: 7200000 },
          popularity: 85,
          external_urls: { spotify: '#' },
          genres: ['Pop', 'Bollywood']
        },
        {
          id: 'demo-6',
          name: 'Rahat Fateh Ali Khan',
          images: [{ url: '/placeholder.svg', height: 640, width: 640 }],
          followers: { total: 6500000 },
          popularity: 82,
          external_urls: { spotify: '#' },
          genres: ['Qawwali', 'Sufi']
        }
      ];

            setArtists(artistsData.length > 0 ? artistsData : []);
    } catch (error) {
      console.error('Failed to fetch artists:', error);
      toast({
        title: "Error loading artists",
        description: "Using demo data instead.",
        variant: "destructive",
      });
      
            setArtists([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArtists();
  }, [selectedYear, selectedMarket]);

  useEffect(() => {
    const filtered = artists.filter(artist =>
      artist.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      artist.genres.some(genre => genre.toLowerCase().includes(searchQuery.toLowerCase()))
    );
    setFilteredArtists(filtered);
  }, [artists, searchQuery]);

  const getPopularityColor = (popularity: number) => {
    if (popularity >= 90) return 'text-primary';
    if (popularity >= 80) return 'text-music-gold';
    if (popularity >= 70) return 'text-music-blue';
    return 'text-muted-foreground';
  };

  const getPopularityLabel = (popularity: number) => {
    if (popularity >= 90) return 'Superstar';
    if (popularity >= 80) return 'Popular';
    if (popularity >= 70) return 'Rising';
    return 'Emerging';
  };

  return (
    <div className="space-y-8 p-6">
      {/* Header */}
      <div className="space-y-4 animate-fade-in">
        <div className="flex items-center space-x-3">
          <div className="h-12 w-12 rounded-xl bg-gradient-primary flex items-center justify-center glow-effect">
            <Music className="h-6 w-6 text-primary-foreground animate-music-note" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-foreground">Top Artists</h1>
            <p className="text-muted-foreground">
              Discover the most popular artists and their musical journey
            </p>
          </div>
        </div>

        {/* Controls */}
        <div className="flex flex-wrap gap-4 items-end">
          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">Search Artists</label>
            <Input
              placeholder="Search by name or genre..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-64"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">Year</label>
            <Select value={selectedYear.toString()} onValueChange={(value) => setSelectedYear(parseInt(value))}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {years.map(year => (
                  <SelectItem key={year} value={year.toString()}>{year}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">Market</label>
            <Select value={selectedMarket} onValueChange={setSelectedMarket}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {markets.map(market => (
                  <SelectItem key={market.value} value={market.value}>
                    {market.flag} {market.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <Button 
            onClick={fetchArtists} 
            disabled={loading}
            className="bg-gradient-primary hover:opacity-90 transition-all duration-300"
          >
            {loading ? 'Loading...' : 'Refresh'}
          </Button>
        </div>

        {/* Results Summary */}
        <div className="flex items-center space-x-4">
          <Badge variant="secondary" className="bg-primary/10 text-primary border-primary/20">
            {filteredArtists.length} artists found
          </Badge>
          {searchQuery && (
            <Badge variant="outline">
              Filtered by "{searchQuery}"
            </Badge>
          )}
        </div>
      </div>

      {/* Artists Grid */}
      {loading ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Card key={i}>
              <CardContent className="p-6">
                <Skeleton className="h-32 w-full mb-4" />
                <Skeleton className="h-4 w-3/4 mb-2" />
                <Skeleton className="h-3 w-1/2" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : filteredArtists.length > 0 ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 animate-fade-in">
          {filteredArtists.map((artist, index) => (
            <Card 
              key={artist.id} 
              className="group hover:shadow-elegant transition-all duration-300 hover:scale-105"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <CardContent className="p-6">
                <div className="space-y-4">
                  {/* Artist Image */}
                  <div className="relative">
                    <img
                      src={artist.images[0]?.url || '/placeholder.svg'}
                      alt={artist.name}
                      className="w-full h-32 object-cover rounded-lg group-hover:scale-110 transition-transform duration-300"
                    />
                    <div className="absolute top-2 right-2">
                      <Badge 
                        variant="secondary" 
                        className={`${getPopularityColor(artist.popularity)} bg-background/80 backdrop-blur-sm`}
                      >
                        {getPopularityLabel(artist.popularity)}
                      </Badge>
                    </div>
                  </div>

                  {/* Artist Info */}
                  <div className="space-y-2">
                    <h3 className="font-semibold text-lg text-foreground group-hover:text-primary transition-colors">
                      {artist.name}
                    </h3>
                    
                    <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-1">
                        <Users className="h-4 w-4" />
                        <span>{artist.followers.total.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <TrendingUp className="h-4 w-4" />
                        <span>{artist.popularity}%</span>
                      </div>
                    </div>

                    {/* Popularity Bar */}
                    <div className="w-full bg-muted rounded-full h-2">
                      <div
                        className="bg-primary h-2 rounded-full transition-all duration-300"
                        style={{ width: `${artist.popularity}%` }}
                      />
                    </div>

                    {/* Genres */}
                    <div className="flex flex-wrap gap-1">
                      {artist.genres.slice(0, 3).map((genre) => (
                        <Badge 
                          key={genre} 
                          variant="outline" 
                          className="text-xs"
                        >
                          {genre}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center justify-between pt-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Heart className="h-4 w-4 mr-1" />
                      Follow
                    </Button>
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => window.open(artist.external_urls.spotify, '_blank')}
                      className="opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <ExternalLink className="h-4 w-4 mr-1" />
                      Spotify
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16 space-y-4">
            <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
              <Music className="h-8 w-8 text-muted-foreground" />
            </div>
            <div className="text-center space-y-2">
              <h3 className="font-semibold text-foreground">No artists found</h3>
              <p className="text-muted-foreground">
                {searchQuery 
                  ? `No artists match "${searchQuery}". Try different keywords.`
                  : "No artists available for the selected filters."
                }
              </p>
            </div>
            {searchQuery && (
              <Button 
                variant="outline" 
                onClick={() => setSearchQuery('')}
                className="mt-4"
              >
                Clear Search
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      {/* Quick Stats */}
      {!loading && filteredArtists.length > 0 && (
        <div className="grid gap-6 md:grid-cols-4">
          <Card className="animate-fade-in delay-100">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total Followers
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">
                {filteredArtists.reduce((sum, artist) => sum + artist.followers.total, 0).toLocaleString()}
              </div>
            </CardContent>
          </Card>

          <Card className="animate-fade-in delay-200">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Average Popularity
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">
                {Math.round(filteredArtists.reduce((sum, artist) => sum + artist.popularity, 0) / filteredArtists.length)}%
              </div>
            </CardContent>
          </Card>

          <Card className="animate-fade-in delay-300">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Top Genre
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">
                Bollywood
              </div>
            </CardContent>
          </Card>

          <Card className="animate-fade-in delay-400">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Superstars
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">
                {filteredArtists.filter(artist => artist.popularity >= 90).length}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}