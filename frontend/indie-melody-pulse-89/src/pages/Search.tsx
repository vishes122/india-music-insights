import { useState, useEffect, useCallback } from 'react';
import { Search as SearchIcon, Music, User, List, ExternalLink, Play, Pause, Calendar } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { apiService, Track, Artist, SearchResponse } from '@/lib/apiClient';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from '@/hooks/use-toast';
import { debounce } from 'lodash-es';

export default function Search() {
  const [query, setQuery] = useState('');
  const [selectedYear, setSelectedYear] = useState<number | 'all'>('all');
  const [searchResults, setSearchResults] = useState<SearchResponse>({});
  const [loading, setLoading] = useState(false);
  const [currentlyPlaying, setCurrentlyPlaying] = useState<string | null>(null);
  const [audioElements, setAudioElements] = useState<{ [key: string]: HTMLAudioElement }>({});

  // Year options for historical search
  const yearOptions = [
    { value: 'all', label: 'All Years' },
    ...Array.from({ length: 46 }, (_, i) => {
      const year = 2025 - i;
      return { value: year, label: year.toString() };
    })
  ];

  const debouncedSearch = useCallback(
    debounce(async (searchQuery: string, year: number | 'all') => {
      if (!searchQuery.trim()) {
        setSearchResults({});
        return;
      }

      setLoading(true);
      try {
        if (year !== 'all') {
          // Use historical search for specific year
          const trackResults = await apiService.searchTracksByYear(year, searchQuery, 20);
          setSearchResults({
            tracks: {
              items: trackResults.tracks,
              total: trackResults.total
            }
          });
        } else {
          // General search across all years (fallback to current year for now)
          const currentYear = new Date().getFullYear();
          const trackResults = await apiService.searchTracksByYear(currentYear, searchQuery, 20);
          setSearchResults({
            tracks: {
              items: trackResults.tracks,
              total: trackResults.total
            }
          });
        }
      } catch (error) {
        console.error('Search failed:', error);
        toast({
          title: "Search failed",
          description: "Unable to search at the moment. Please try again.",
          variant: "destructive",
        });
        setSearchResults({});
      } finally {
        setLoading(false);
      }
    }, 500),
    []
  );

  useEffect(() => {
    debouncedSearch(query, selectedYear);
  }, [query, selectedYear, debouncedSearch]);

  const handlePlayPause = (track: Track) => {
    if (!track.preview_url) return;

    if (currentlyPlaying === track.id) {
      audioElements[track.id]?.pause();
      setCurrentlyPlaying(null);
    } else {
      if (currentlyPlaying && audioElements[currentlyPlaying]) {
        audioElements[currentlyPlaying].pause();
      }

      if (!audioElements[track.id]) {
        const audio = new Audio(track.preview_url);
        audio.addEventListener('ended', () => setCurrentlyPlaying(null));
        setAudioElements(prev => ({ ...prev, [track.id]: audio }));
        audio.play();
      } else {
        audioElements[track.id].play();
      }
      setCurrentlyPlaying(track.id);
    }
  };

  const getArtistNames = (artists: Track['artists']) => {
    return artists.map(artist => artist.name).join(', ');
  };

  const getTotalResults = () => {
    return (searchResults.artists?.total || 0) + (searchResults.tracks?.total || 0) + (searchResults.playlists?.total || 0);
  };

  return (
    <div className="space-y-8 p-6">
      {/* Header */}
      <div className="space-y-4 animate-fade-in">
        <div className="flex items-center space-x-3">
          <div className="h-12 w-12 rounded-xl bg-gradient-primary flex items-center justify-center glow-effect">
            <SearchIcon className="h-6 w-6 text-primary-foreground animate-music-note" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-foreground">Search</h1>
            <p className="text-muted-foreground">
              Discover artists, tracks, and playlists across all markets
            </p>
          </div>
        </div>

        {/* Search Input */}
        <div className="space-y-4 max-w-4xl">
          <div className="relative">
            <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
            <Input
              placeholder="Search for artists, tracks, or playlists..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="pl-10 h-12 text-lg border-2 focus:border-primary transition-all duration-300"
            />
            {loading && (
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <div className="h-4 w-4 border-2 border-primary border-t-transparent rounded-full animate-spin" />
              </div>
            )}
          </div>
          
          {/* Year Filter */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium text-foreground">Year:</span>
            </div>
            <Select 
              value={selectedYear.toString()} 
              onValueChange={(value) => setSelectedYear(value === 'all' ? 'all' : parseInt(value))}
            >
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {yearOptions.map(option => (
                  <SelectItem key={option.value} value={option.value.toString()}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            {selectedYear !== 'all' && (
              <Badge variant="secondary" className="text-xs">
                Historical Search
              </Badge>
            )}
          </div>
        </div>

        {/* Results Summary */}
        {query && !loading && (
          <div className="flex items-center space-x-4 animate-slide-in">
            <Badge variant="secondary" className="bg-primary/10 text-primary border-primary/20">
              {getTotalResults()} results for "{query}"
            </Badge>
            {searchResults.artists?.total && (
              <Badge variant="outline">{searchResults.artists.total} artists</Badge>
            )}
            {searchResults.tracks?.total && (
              <Badge variant="outline">{searchResults.tracks.total} tracks</Badge>
            )}
            {searchResults.playlists?.total && (
              <Badge variant="outline">{searchResults.playlists.total} playlists</Badge>
            )}
          </div>
        )}
      </div>

      {/* Search Results */}
      {query ? (
        <Tabs defaultValue="all" className="animate-fade-in delay-100">
          <TabsList className="grid w-full grid-cols-4 lg:w-96">
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="artists" className="flex items-center space-x-2">
              <User className="h-4 w-4" />
              <span>Artists</span>
            </TabsTrigger>
            <TabsTrigger value="tracks" className="flex items-center space-x-2">
              <Music className="h-4 w-4" />
              <span>Tracks</span>
            </TabsTrigger>
            <TabsTrigger value="playlists" className="flex items-center space-x-2">
              <List className="h-4 w-4" />
              <span>Playlists</span>
            </TabsTrigger>
          </TabsList>

          {/* All Results */}
          <TabsContent value="all" className="space-y-8">
            {/* Artists Section */}
            {searchResults.artists?.items && searchResults.artists.items.length > 0 && (
              <Card className="animate-fade-in delay-200">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <User className="h-5 w-5" />
                    <span>Artists</span>
                    <Badge variant="secondary">{(searchResults.artists?.items || []).length}</Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {(searchResults.artists?.items || []).slice(0, 6).map((artist: Artist) => (
                      <div
                        key={artist.id}
                        className="group p-4 rounded-lg border border-border hover:border-primary/50 hover:bg-muted/50 transition-all duration-300 cursor-pointer"
                      >
                        <div className="flex items-center space-x-3">
                          <img
                            src={artist.images[0]?.url || '/placeholder.svg'}
                            alt={artist.name}
                            className="h-12 w-12 rounded-full object-cover group-hover:scale-110 transition-transform duration-300"
                          />
                          <div className="flex-1 min-w-0">
                            <h4 className="font-medium text-foreground truncate group-hover:text-primary transition-colors">
                              {artist.name}
                            </h4>
                            <p className="text-sm text-muted-foreground">
                              {artist.followers.total.toLocaleString()} followers
                            </p>
                          </div>
                          <Button
                            size="sm"
                            variant="ghost"
                            className="opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => window.open(artist.external_urls.spotify, '_blank')}
                          >
                            <ExternalLink className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Tracks Section */}
            {searchResults.tracks?.items && searchResults.tracks.items.length > 0 && (
              <Card className="animate-fade-in delay-300">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Music className="h-5 w-5" />
                    <span>Tracks</span>
                    <Badge variant="secondary">{(searchResults.tracks?.items || []).length}</Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {(searchResults.tracks?.items || []).slice(0, 10).map((track: Track) => (
                      <div
                        key={track.id}
                        className="group flex items-center space-x-4 p-3 rounded-lg hover:bg-muted/50 transition-all duration-200"
                      >
                        <div className="relative flex-shrink-0">
                          <img
                            src={track.album.images[0]?.url || '/placeholder.svg'}
                            alt={track.album.name}
                            className="h-12 w-12 rounded-md object-cover"
                          />
                          {track.preview_url && (
                            <Button
                              size="sm"
                              variant="ghost"
                              className="absolute inset-0 h-12 w-12 rounded-md bg-black/60 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                              onClick={() => handlePlayPause(track)}
                            >
                              {currentlyPlaying === track.id ? (
                                <Pause className="h-4 w-4" />
                              ) : (
                                <Play className="h-4 w-4" />
                              )}
                            </Button>
                          )}
                        </div>

                        <div className="flex-1 min-w-0 space-y-1">
                          <div className="flex items-center space-x-2">
                            <h4 className="font-medium text-foreground truncate">
                              {track.name}
                            </h4>
                            {currentlyPlaying === track.id && (
                              <div className="flex space-x-1">
                                <div className="h-3 w-1 bg-primary animate-pulse rounded-full" />
                                <div className="h-3 w-1 bg-primary animate-pulse rounded-full delay-100" />
                                <div className="h-3 w-1 bg-primary animate-pulse rounded-full delay-200" />
                              </div>
                            )}
                          </div>
                          <p className="text-sm text-muted-foreground truncate">
                            {getArtistNames(track.artists)} • {track.album.name}
                          </p>
                        </div>

                        <div className="hidden sm:block">
                          <div className="flex items-center space-x-2">
                            <div className="w-12 bg-muted rounded-full h-2">
                              <div
                                className="bg-primary h-2 rounded-full transition-all duration-300"
                                style={{ width: `${track.popularity}%` }}
                              />
                            </div>
                            <span className="text-xs text-muted-foreground w-8">
                              {track.popularity}
                            </span>
                          </div>
                        </div>

                        <Button
                          size="sm"
                          variant="ghost"
                          className="opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={() => window.open(track.external_urls.spotify, '_blank')}
                        >
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Artists Only */}
          <TabsContent value="artists">
            {loading ? (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {Array.from({ length: 6 }).map((_, i) => (
                  <Skeleton key={i} className="h-20 w-full" />
                ))}
              </div>
            ) : searchResults.artists?.items && searchResults.artists.items.length > 0 ? (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 animate-fade-in">
                {(searchResults.artists?.items || []).map((artist: Artist) => (
                  <Card key={artist.id} className="group hover:shadow-elegant transition-all duration-300">
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-3">
                        <img
                          src={artist.images[0]?.url || '/placeholder.svg'}
                          alt={artist.name}
                          className="h-16 w-16 rounded-full object-cover group-hover:scale-110 transition-transform duration-300"
                        />
                        <div className="flex-1 min-w-0">
                          <h4 className="font-medium text-foreground truncate group-hover:text-primary transition-colors">
                            {artist.name}
                          </h4>
                          <p className="text-sm text-muted-foreground">
                            {artist.followers.total.toLocaleString()} followers
                          </p>
                          <div className="flex items-center space-x-1 mt-1">
                            <div className="w-16 bg-muted rounded-full h-1">
                              <div
                                className="bg-primary h-1 rounded-full transition-all duration-300"
                                style={{ width: `${artist.popularity}%` }}
                              />
                            </div>
                            <span className="text-xs text-muted-foreground">
                              {artist.popularity}%
                            </span>
                          </div>
                        </div>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => window.open(artist.external_urls.spotify, '_blank')}
                        >
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-16 space-y-4">
                  <User className="h-16 w-16 text-muted-foreground" />
                  <div className="text-center space-y-2">
                    <h3 className="font-semibold text-foreground">No artists found</h3>
                    <p className="text-muted-foreground">
                      Try searching with different keywords
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Tracks Only */}
          <TabsContent value="tracks">
            {loading ? (
              <Card>
                <CardContent className="p-6 space-y-4">
                  {Array.from({ length: 10 }).map((_, i) => (
                    <Skeleton key={i} className="h-16 w-full" />
                  ))}
                </CardContent>
              </Card>
            ) : searchResults.tracks?.items && searchResults.tracks.items.length > 0 ? (
              <Card className="animate-fade-in">
                <CardContent className="p-6">
                  <div className="space-y-2">
                    {(searchResults.tracks?.items || []).map((track: Track) => (
                      <div
                        key={track.id}
                        className="group flex items-center space-x-4 p-3 rounded-lg hover:bg-muted/50 transition-all duration-200"
                      >
                        <div className="relative flex-shrink-0">
                          <img
                            src={track.album.images[0]?.url || '/placeholder.svg'}
                            alt={track.album.name}
                            className="h-12 w-12 rounded-md object-cover"
                          />
                          {track.preview_url && (
                            <Button
                              size="sm"
                              variant="ghost"
                              className="absolute inset-0 h-12 w-12 rounded-md bg-black/60 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                              onClick={() => handlePlayPause(track)}
                            >
                              {currentlyPlaying === track.id ? (
                                <Pause className="h-4 w-4" />
                              ) : (
                                <Play className="h-4 w-4" />
                              )}
                            </Button>
                          )}
                        </div>

                        <div className="flex-1 min-w-0 space-y-1">
                          <div className="flex items-center space-x-2">
                            <h4 className="font-medium text-foreground truncate">
                              {track.name}
                            </h4>
                            {currentlyPlaying === track.id && (
                              <div className="flex space-x-1">
                                <div className="h-3 w-1 bg-primary animate-pulse rounded-full" />
                                <div className="h-3 w-1 bg-primary animate-pulse rounded-full delay-100" />
                                <div className="h-3 w-1 bg-primary animate-pulse rounded-full delay-200" />
                              </div>
                            )}
                          </div>
                          <p className="text-sm text-muted-foreground truncate">
                            {getArtistNames(track.artists)} • {track.album.name}
                          </p>
                        </div>

                        <div className="hidden sm:block">
                          <div className="flex items-center space-x-2">
                            <div className="w-12 bg-muted rounded-full h-2">
                              <div
                                className="bg-primary h-2 rounded-full transition-all duration-300"
                                style={{ width: `${track.popularity}%` }}
                              />
                            </div>
                            <span className="text-xs text-muted-foreground w-8">
                              {track.popularity}
                            </span>
                          </div>
                        </div>

                        <Button
                          size="sm"
                          variant="ghost"
                          className="opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={() => window.open(track.external_urls.spotify, '_blank')}
                        >
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-16 space-y-4">
                  <Music className="h-16 w-16 text-muted-foreground" />
                  <div className="text-center space-y-2">
                    <h3 className="font-semibold text-foreground">No tracks found</h3>
                    <p className="text-muted-foreground">
                      Try searching with different keywords
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Playlists Only */}
          <TabsContent value="playlists">
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-16 space-y-4">
                <List className="h-16 w-16 text-muted-foreground" />
                <div className="text-center space-y-2">
                  <h3 className="font-semibold text-foreground">Playlists Coming Soon</h3>
                  <p className="text-muted-foreground">
                    Playlist search functionality will be available in the next update
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      ) : (
        /* Empty State */
        <Card className="animate-fade-in">
          <CardContent className="flex flex-col items-center justify-center py-16 space-y-6">
            <div className="h-20 w-20 rounded-full bg-gradient-primary flex items-center justify-center glow-effect">
              <SearchIcon className="h-10 w-10 text-primary-foreground animate-music-note" />
            </div>
            <div className="text-center space-y-2 max-w-md">
              <h3 className="text-xl font-semibold text-foreground">Start your musical journey</h3>
              <p className="text-muted-foreground">
                Search for your favorite artists, discover new tracks, or explore trending playlists. 
                The world of music is at your fingertips.
              </p>
            </div>
            <div className="flex flex-wrap gap-2 justify-center">
              {['A.R. Rahman', 'Arijit Singh', 'Bollywood Hits', 'Classical Indian'].map((suggestion) => (
                <Button
                  key={suggestion}
                  variant="outline"
                  size="sm"
                  onClick={() => setQuery(suggestion)}
                  className="hover:bg-primary hover:text-primary-foreground transition-all duration-300"
                >
                  {suggestion}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}