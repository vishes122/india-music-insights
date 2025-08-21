import React from 'react';
import { ExternalLink } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import { Track } from '@/lib/apiClient';

interface TrackTableProps {
  tracks: Track[];
  title?: string;
  className?: string; // Add className prop
  showRank?: boolean;
}

interface TrackRowProps {
  track: Track;
  index: number;
}

const TrackRow: React.FC<TrackRowProps> = ({ track, index }) => {

  const getArtistNames = (artists: string[] | any[]): string => {
    if (!Array.isArray(artists) || artists.length === 0) {
      return "Unknown Artist";
    }
    
    // Handle both string arrays and artist objects
    const validArtists = artists.map(artist => {
      if (typeof artist === 'string') {
        return artist;
      } else if (typeof artist === 'object' && artist.name) {
        return artist.name;
      }
      return null;
    }).filter(name => name && typeof name === 'string' && name.trim() !== '');
    
    if (validArtists.length === 0) {
      return "Unknown Artist";
    }
    
    return validArtists.join(', ');
  };

  const getAlbumImage = (album: any): string => {
    // Since we don't have album images from the backend, use placeholder
    return '/placeholder.svg';
  };

  const getAlbumName = (album: any): string => {
    if (!album) return 'Unknown Album';
    if (typeof album === 'string') return album;
    if (typeof album === 'object' && typeof album.name === 'string') return album.name;
    return 'Unknown Album';
  };

  const formatDate = (dateString: string): string => {
    if (!dateString) return 'Unknown';
    try {
      return new Date(dateString).toLocaleDateString();
    } catch {
      return 'Unknown';
    }
  };

  const getPopularityBadge = (popularity: number | undefined): string => {
    const value = popularity ?? 0;
    if (value >= 70) return 'bg-green-500/15 text-green-600 dark:text-green-400';
    if (value >= 40) return 'bg-yellow-500/15 text-yellow-600 dark:text-yellow-400';
    return 'bg-red-500/15 text-red-600 dark:text-red-400';
  };

  const rowBackground = index % 2 === 1 ? 'bg-muted/20' : '';


  return (
    <div className={cn("p-3 rounded-lg transition-colors hover:bg-muted/40", rowBackground)}>
      {/* Mobile (<= md) */}
      <div className="flex md:hidden items-start gap-3">
        <span className="inline-flex items-center justify-center w-6 h-6 text-[10px] font-medium rounded-full bg-gradient-to-br from-primary/20 to-primary/10 text-primary mt-1">
          {index + 1}
        </span>
        <img
          src={getAlbumImage((track as any).album)}
          alt={getAlbumName((track as any).album) || 'Album cover'}
          className="w-12 h-12 rounded-md object-cover"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = '/placeholder.svg';
          }}
        />
        <div className="flex-1 min-w-0 space-y-1">
          <div className="flex items-center gap-2">
            <h3 className="font-medium text-foreground truncate">
              {track.track_name || track.name || 'Unknown Track'}
            </h3>
            {((track as any).external_urls?.spotify || (track as any).spotify_url) && (
              <a
                href={(track as any).external_urls?.spotify || (track as any).spotify_url}
                target="_blank"
                rel="noreferrer"
                title="Open on Spotify"
                className="text-muted-foreground hover:text-primary"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>
          <p className="text-xs text-muted-foreground truncate">
            {getArtistNames(track.artists)}
          </p>
          <div className="flex items-center justify-between">
            <span className="text-[11px] text-muted-foreground truncate max-w-[50%]">
              {getAlbumName((track as any).album)}
            </span>
            <span className="text-[11px] text-muted-foreground">
              {formatDate(((track as any).release_date) || ((track as any).album?.release_date))}
            </span>
          </div>
          <div className="pt-1">
            <div className="flex items-center gap-2">
              <span className={cn("inline-flex items-center justify-end px-2 py-0.5 rounded-full text-[10px]", getPopularityBadge(track.popularity))}>
                {track.popularity ?? 0}
              </span>
              <div className="flex-1">
                <Progress value={Math.min(Math.max(track.popularity || 0, 0), 100)} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Desktop (md+) */}
      <div className="hidden md:grid grid-cols-12 items-center gap-3">
        <div className="col-span-1 flex items-center justify-end pr-1">
          <span className="inline-flex items-center justify-center w-6 h-6 text-[10px] font-medium rounded-full bg-gradient-to-br from-primary/20 to-primary/10 text-primary">
            {index + 1}
          </span>
        </div>

        <div className="col-span-1">
          <img
            src={getAlbumImage((track as any).album)}
            alt={getAlbumName((track as any).album) || 'Album cover'}
            className="w-12 h-12 rounded-md object-cover"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.src = '/placeholder.svg';
            }}
          />
        </div>

        <div className="col-span-5 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-medium text-foreground truncate">
              {track.track_name || track.name || 'Unknown Track'}
            </h3>
            {((track as any).external_urls?.spotify || (track as any).spotify_url) && (
              <a
                href={(track as any).external_urls?.spotify || (track as any).spotify_url}
                target="_blank"
                rel="noreferrer"
                title="Open on Spotify"
                className="text-muted-foreground hover:text-primary"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>
          <p className="text-xs text-muted-foreground truncate">
            {getArtistNames(track.artists)}
          </p>
        </div>

        <div className="col-span-3 hidden md:block text-sm text-muted-foreground truncate">
          {getAlbumName((track as any).album)}
        </div>

        <div className="col-span-1 hidden lg:block text-xs text-muted-foreground">
          {formatDate(((track as any).release_date) || ((track as any).album?.release_date))}
        </div>

        <div className="col-span-1 text-right space-y-1">
          <span className={cn("inline-flex items-center justify-end px-2 py-0.5 rounded-full text-[10px]", getPopularityBadge(track.popularity))}>
            {track.popularity ?? 0}
          </span>
          <Progress value={Math.min(Math.max(track.popularity || 0, 0), 100)} />
        </div>
      </div>
    </div>
  );
};

export const TrackTable: React.FC<TrackTableProps> = ({ tracks, title = "Tracks", className }) => {
  if (!Array.isArray(tracks)) {
    return (
      <Card className={className}>
        <CardContent className="p-6">
          <p className="text-gray-500">No tracks available</p>
        </CardContent>
      </Card>
    );
  }

  if (tracks.length === 0) {
    return (
      <Card className={className}>
        <CardContent className="p-6">
          <p className="text-gray-500">No tracks found</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardContent className="p-0">
        <div className="p-4 border-b">
          <h2 className="text-lg font-semibold">{title}</h2>
        </div>
        
        {/* Header */}
        <div>
          <div className="md:hidden p-3 border-b bg-muted/30 text-xs font-medium text-muted-foreground">
            Top Tracks
          </div>
          <div className="hidden md:grid grid-cols-12 items-center p-3 border-b bg-gradient-to-r from-muted/40 to-transparent text-xs font-medium text-muted-foreground">
            <div className="col-span-1 text-right pr-2">Rank</div>
            <div className="col-span-1">Art</div>
            <div className="col-span-5">Title • Artists</div>
            <div className="col-span-3">Album</div>
            <div className="col-span-1">Release</div>
            <div className="col-span-1 text-right">Popularity</div>
          </div>
        </div>

        {/* Track rows */}
        <div>
          {tracks.map((track, index) => (
            <TrackRow key={`${track.track_name}-${track.rank}-${index}`} track={track} index={index} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default TrackTable;
