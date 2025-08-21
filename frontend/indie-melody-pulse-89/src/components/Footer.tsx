import { Heart, Music, Github, ExternalLink } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-card border-t border-border mt-16">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid gap-8 md:grid-cols-3">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 rounded-lg bg-gradient-primary flex items-center justify-center">
                <Music className="h-5 w-5 text-primary-foreground" />
              </div>
              <span className="font-bold text-foreground">Music Insights</span>
            </div>
            <p className="text-muted-foreground text-sm">
              Professional analytics dashboard for Indian music streaming data with beautiful visualizations and insights.
            </p>
          </div>

          {/* Links */}
          <div className="space-y-4">
            <h3 className="font-semibold text-foreground">Quick Links</h3>
            <div className="space-y-2">
              <a href="/" className="block text-sm text-muted-foreground hover:text-primary transition-colors">
                Overview
              </a>
              <a href="/year-explorer" className="block text-sm text-muted-foreground hover:text-primary transition-colors">
                Year Explorer
              </a>
              <a href="/artists" className="block text-sm text-muted-foreground hover:text-primary transition-colors">
                Artists
              </a>
              <a href="/search" className="block text-sm text-muted-foreground hover:text-primary transition-colors">
                Search
              </a>
            </div>
          </div>

          {/* Creator */}
          <div className="space-y-4">
            <h3 className="font-semibold text-foreground">Created By</h3>
            <div className="space-y-3">
              <a 
                href="http://visheshsanghvi.me/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-sm text-muted-foreground hover:text-primary transition-colors group"
              >
                <span className="font-medium">Vishesh Sanghvi</span>
                <ExternalLink className="h-3 w-3 group-hover:translate-x-1 transition-transform" />
              </a>
              <div className="space-y-1">
                <p className="text-xs text-muted-foreground">
                  Full Stack Developer & Music Enthusiast
                </p>
                <p className="text-xs text-muted-foreground/80">
                  Passionate about building innovative music technology solutions
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-8 pt-8 border-t border-border flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <span>Made with</span>
            <Heart className="h-4 w-4 text-primary animate-pulse" />
            <span>for music lovers everywhere</span>
          </div>
          <div className="text-sm text-muted-foreground">
            © 2024 Music Insights by Vishesh Sanghvi. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
}