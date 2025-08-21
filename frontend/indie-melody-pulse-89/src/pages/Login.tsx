import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Music, Lock, Mail, ArrowLeft } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { toast } from '@/hooks/use-toast';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // SEO and accessibility
  useEffect(() => {
    document.title = 'Sign In - Music Insights Dashboard';
    document.querySelector('meta[name="description"]')?.setAttribute(
      'content', 
      'Sign in to Music Insights dashboard to access professional music analytics, streaming data, and market insights.'
    );
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      toast({
        title: "Missing fields",
        description: "Please fill in all required fields.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    
    // Simulate login API call
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Store auth state (in real app, you'd get a token)
      localStorage.setItem('isAuthenticated', 'true');
      if (rememberMe) {
        localStorage.setItem('userEmail', email);
      }
      
      toast({
        title: "Login successful!",
        description: "Welcome back to Music Insights Dashboard.",
      });
      
      navigate('/');
    } catch (error) {
      toast({
        title: "Login failed",
        description: "Invalid credentials. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-hero">
      {/* Mobile-optimized header */}
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center px-4">
          <Link to="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
            <ArrowLeft className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Back to Home</span>
          </Link>
        </div>
      </header>

      <main className="flex items-center justify-center px-4 py-8 sm:py-12">
        <div className="w-full max-w-md space-y-6 sm:space-y-8">
          {/* Brand Header */}
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center space-x-3">
              <div className="h-10 w-10 sm:h-12 sm:w-12 rounded-xl bg-gradient-primary flex items-center justify-center glow-effect">
                <Music className="h-5 w-5 sm:h-6 sm:w-6 text-primary-foreground" />
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold text-foreground">Music Insights</h1>
            </div>
            <div className="space-y-2">
              <h2 className="text-xl sm:text-2xl font-semibold text-foreground">Welcome back</h2>
              <p className="text-sm sm:text-base text-muted-foreground px-2">
                Sign in to access your professional music analytics dashboard
              </p>
            </div>
          </div>

          {/* Login Form */}
          <Card className="shadow-elegant border-border/50 bg-card/50 backdrop-blur-sm">
            <CardHeader className="space-y-1 pb-4">
              <CardTitle className="flex items-center space-x-2 text-lg">
                <Lock className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Sign In</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="px-4 sm:px-6">
              <form onSubmit={handleLogin} className="space-y-5 sm:space-y-6">
                {/* Email Field */}
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-sm font-medium text-foreground">
                    Email Address
                  </Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="email"
                      type="email"
                      placeholder="Enter your email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="pl-10 h-11 sm:h-12 text-base"
                      autoComplete="email"
                      required
                      aria-describedby="email-help"
                    />
                  </div>
                  <p id="email-help" className="sr-only">Enter your registered email address</p>
                </div>

                {/* Password Field */}
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-sm font-medium text-foreground">
                    Password
                  </Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="password"
                      type={showPassword ? 'text' : 'password'}
                      placeholder="Enter your password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="pl-10 pr-12 h-11 sm:h-12 text-base"
                      autoComplete="current-password"
                      required
                      aria-describedby="password-help"
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 hover:bg-transparent"
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <Eye className="h-4 w-4 text-muted-foreground" />
                      )}
                    </Button>
                  </div>
                  <p id="password-help" className="sr-only">Enter your account password</p>
                </div>

                {/* Remember Me & Forgot Password */}
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="remember"
                      checked={rememberMe}
                      onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                    />
                    <Label
                      htmlFor="remember"
                      className="text-sm text-muted-foreground cursor-pointer"
                    >
                      Remember me
                    </Label>
                  </div>
                  <Link
                    to="/forgot-password"
                    className="text-sm text-primary hover:text-primary/80 transition-colors"
                  >
                    Forgot password?
                  </Link>
                </div>

                {/* Login Button */}
                <Button
                  type="submit"
                  className="w-full bg-gradient-primary hover:opacity-90 transition-all duration-300 h-11 sm:h-12 text-base font-medium"
                  disabled={loading}
                >
                  {loading ? (
                    <div className="flex items-center space-x-2">
                      <div className="h-4 w-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                      <span>Signing in...</span>
                    </div>
                  ) : (
                    'Sign In'
                  )}
                </Button>

                {/* Demo Credentials */}
                <div className="p-3 sm:p-4 bg-muted/30 rounded-lg border border-border/50">
                  <p className="text-xs font-medium text-muted-foreground mb-2">Demo Credentials:</p>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground font-mono">Email: demo@musicinsights.com</p>
                    <p className="text-xs text-muted-foreground font-mono">Password: demo123</p>
                  </div>
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Sign Up Link */}
          <div className="text-center px-2">
            <p className="text-sm text-muted-foreground">
              Don't have an account?{' '}
              <Link
                to="/register"
                className="text-primary hover:text-primary/80 transition-colors font-medium"
              >
                Sign up here
              </Link>
            </p>
          </div>

          {/* Features List */}
          <Card className="bg-card/30 backdrop-blur-sm border-border/50">
            <CardContent className="p-4 sm:p-6">
              <h3 className="text-sm font-medium text-foreground mb-4">What you'll get access to:</h3>
              <div className="grid gap-3">
                <div className="flex items-start space-x-3">
                  <div className="h-2 w-2 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                  <span className="text-xs sm:text-sm text-muted-foreground">Real-time music analytics and streaming insights</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="h-2 w-2 rounded-full bg-music-gold mt-1.5 flex-shrink-0" />
                  <span className="text-xs sm:text-sm text-muted-foreground">Track trending songs and top artists</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="h-2 w-2 rounded-full bg-music-purple mt-1.5 flex-shrink-0" />
                  <span className="text-xs sm:text-sm text-muted-foreground">Market comparison and genre analysis</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="h-2 w-2 rounded-full bg-music-blue mt-1.5 flex-shrink-0" />
                  <span className="text-xs sm:text-sm text-muted-foreground">Historical data exploration and trends</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Creator Attribution */}
          <div className="text-center px-2">
            <p className="text-xs text-muted-foreground">
              Created with ❤️ by{' '}
              <a 
                href="http://visheshsanghvi.me/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-primary hover:text-primary/80 transition-colors font-medium"
              >
                Vishesh Sanghvi
              </a>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}