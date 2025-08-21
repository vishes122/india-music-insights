import { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Globe } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { apiService } from '@/lib/apiClient';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from '@/hooks/use-toast';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const MARKET_COLORS = {
  IN: '#1DB954',
  US: '#1ed760', 
  GB: '#1aa34a',
  CA: '#17853a',
  AU: '#146b2e',
  DE: '#1c7a3d',
  FR: '#189644',
  BR: '#15662c',
};

export default function Compare() {
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [selectedMarkets, setSelectedMarkets] = useState<string[]>(['IN', 'US', 'GB']);
  const [compareData, setCompareData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const years = Array.from({ length: 26 }, (_, i) => 2025 - i);
  const markets = [
    { value: 'IN', label: 'India', flag: '🇮🇳' },
    { value: 'US', label: 'United States', flag: '🇺🇸' },
    { value: 'GB', label: 'United Kingdom', flag: '🇬🇧' },
    { value: 'CA', label: 'Canada', flag: '🇨🇦' },
    { value: 'AU', label: 'Australia', flag: '🇦🇺' },
    { value: 'DE', label: 'Germany', flag: '🇩🇪' },
    { value: 'FR', label: 'France', flag: '🇫🇷' },
    { value: 'BR', label: 'Brazil', flag: '🇧🇷' },
  ];

  const fetchCompareData = async () => {
    if (selectedMarkets.length === 0) return;

    setLoading(true);
    try {
      const response = await apiService.compareGenres(selectedMarkets);
      const transformedData = (response.genres || []).map((g: any) => {
        const row: any = { genre: g.name };
        selectedMarkets.forEach(m => {
          row[m] = g.markets?.[m] ?? 0;
        });
        return row;
      });
      setCompareData(transformedData);
    } catch (error) {
      console.error('Failed to fetch compare data:', error);
      toast({ title: 'Error loading data', description: 'Could not load comparison.', variant: 'destructive' });
      setCompareData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCompareData();
  }, [selectedYear, selectedMarkets]);

  const handleMarketToggle = (marketValue: string, checked: boolean) => {
    if (checked) {
      setSelectedMarkets(prev => [...prev, marketValue]);
    } else {
      setSelectedMarkets(prev => prev.filter(m => m !== marketValue));
    }
  };

  const getMarketLabel = (value: string) => {
    return markets.find(m => m.value === value)?.label || value;
  };

  const getMarketFlag = (value: string) => {
    return markets.find(m => m.value === value)?.flag || '';
  };

  return (
    <div className="space-y-8 p-6">
      {/* Header */}
      <div className="space-y-4 animate-fade-in">
        <div className="flex items-center space-x-3">
          <div className="h-12 w-12 rounded-xl bg-gradient-primary flex items-center justify-center glow-effect">
            <BarChart3 className="h-6 w-6 text-primary-foreground animate-music-note" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-foreground">Compare Markets</h1>
            <p className="text-muted-foreground">
              Analyze music trends across different global markets
            </p>
          </div>
        </div>

        {/* Controls */}
        <div className="flex flex-wrap gap-6 items-start">
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
            <label className="text-sm font-medium text-foreground">Markets to Compare</label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 bg-card border border-border rounded-lg">
              {markets.map(market => (
                <div key={market.value} className="flex items-center space-x-2">
                  <Checkbox
                    id={market.value}
                    checked={selectedMarkets.includes(market.value)}
                    onCheckedChange={(checked) => handleMarketToggle(market.value, checked as boolean)}
                  />
                  <label
                    htmlFor={market.value}
                    className="text-sm font-medium text-foreground cursor-pointer flex items-center space-x-1"
                  >
                    <span>{market.flag}</span>
                    <span>{market.label}</span>
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="flex items-end">
            <Button 
              onClick={fetchCompareData} 
              disabled={loading || selectedMarkets.length === 0}
              className="bg-gradient-primary hover:opacity-90 transition-all duration-300"
            >
              {loading ? 'Loading...' : 'Update Comparison'}
            </Button>
          </div>
        </div>

        {/* Selected Markets Summary */}
        <div className="flex flex-wrap gap-2">
          {selectedMarkets.map(market => (
            <Badge 
              key={market} 
              variant="secondary" 
              className="bg-primary/10 text-primary border-primary/20"
            >
              {getMarketFlag(market)} {getMarketLabel(market)}
            </Badge>
          ))}
        </div>
      </div>

      {/* Comparison Chart */}
      <Card className="animate-fade-in delay-100">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Globe className="h-5 w-5" />
              <span>Genre Buckets by Market</span>
            </div>
            <Badge variant="secondary">
              {selectedMarkets.length} markets
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <Skeleton className="h-96 w-full" />
          ) : selectedMarkets.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 space-y-4">
              <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
                <BarChart3 className="h-8 w-8 text-muted-foreground" />
              </div>
              <div className="text-center space-y-2">
                <h3 className="font-semibold text-foreground">Select markets to compare</h3>
                <p className="text-muted-foreground">
                  Choose at least one market from the options above to see the comparison
                </p>
              </div>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={compareData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis 
                  dataKey="genre" 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'hsl(var(--card))', 
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                  labelStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Legend />
                {selectedMarkets.map((market) => (
                  <Bar
                    key={market}
                    dataKey={market}
                    name={`${getMarketFlag(market)} ${getMarketLabel(market)}`}
                    fill={MARKET_COLORS[market as keyof typeof MARKET_COLORS] || '#1DB954'}
                    radius={[2, 2, 0, 0]}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          )}
        </CardContent>
      </Card>

      {/* Insights */}
      {!loading && selectedMarkets.length > 0 && compareData.length > 0 && (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card className="animate-fade-in delay-200">
            <CardHeader>
              <CardTitle className="text-lg">Market Insights</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="text-sm">
                  <span className="font-medium text-foreground">Dominant Genre:</span>
                  <br />
                  <span className="text-muted-foreground">
                    {compareData.reduce((prev, curr) => {
                      const prevMax = Math.max(...selectedMarkets.map(m => prev[m] || 0));
                      const currMax = Math.max(...selectedMarkets.map(m => curr[m] || 0));
                      return currMax > prevMax ? curr : prev;
                    }, compareData[0])?.genre || 'N/A'}
                  </span>
                </div>
                <div className="text-sm">
                  <span className="font-medium text-foreground">Most Diverse Market:</span>
                  <br />
                  <span className="text-muted-foreground">
                    {(() => {
                      const scores = selectedMarkets.map(m => ({
                        market: m,
                        nonZero: compareData.filter((row: any) => (row[m] || 0) > 0).length
                      }));
                      const leader = scores.reduce((a, b) => (b.nonZero > a.nonZero ? b : a), scores[0]);
                      return `${getMarketFlag(leader.market)} ${getMarketLabel(leader.market)}`;
                    })()}
                  </span>
                </div>
                <div className="text-sm">
                  <span className="font-medium text-foreground">Unique Trends:</span>
                  <br />
                  <span className="text-muted-foreground">
                    Regional preferences vary significantly
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="animate-fade-in delay-300">
            <CardHeader>
              <CardTitle className="text-lg">Market Leaders</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {compareData.slice(0, 4).map((genre, index) => {
                  const leader = selectedMarkets.reduce((prev, curr) => 
                    (genre[curr] || 0) > (genre[prev] || 0) ? curr : prev
                  );
                  return (
                    <div key={genre.genre} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-mono text-muted-foreground w-4">
                          {index + 1}
                        </span>
                        <span className="text-sm text-foreground">{genre.genre}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <span className="text-xs">{getMarketFlag(leader)}</span>
                        <span className="text-xs text-muted-foreground">{genre[leader]}%</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          <Card className="animate-fade-in delay-400">
            <CardHeader>
              <CardTitle className="text-lg">Key Observations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 text-sm text-muted-foreground">
                <div className="flex items-start space-x-2">
                  <div className="h-1.5 w-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                  <span>Cultural preferences significantly influence genre popularity</span>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="h-1.5 w-1.5 rounded-full bg-music-gold mt-2 flex-shrink-0" />
                  <span>Bollywood music dominates in Indian markets</span>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="h-1.5 w-1.5 rounded-full bg-music-purple mt-2 flex-shrink-0" />
                  <span>Western markets show similar patterns for Pop and Hip-Hop</span>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="h-1.5 w-1.5 rounded-full bg-music-blue mt-2 flex-shrink-0" />
                  <span>Electronic music gains popularity in developed markets</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}