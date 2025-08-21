import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: {
    value: number;
    label: string;
  };
  gradient?: boolean;
  className?: string;
}

export function KPICard({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  trend, 
  gradient = false,
  className 
}: KPICardProps) {
  return (
    <Card className={cn(
      "relative overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-elegant",
      gradient && "bg-gradient-card border-primary/20",
      className
    )}>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div className="space-y-2">
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <div className="space-y-1">
              <p className="text-2xl font-bold text-foreground">{value}</p>
              {subtitle && (
                <p className="text-xs text-muted-foreground">{subtitle}</p>
              )}
            </div>
            {trend && (
              <div className="flex items-center space-x-1">
                <span className={cn(
                  "text-xs font-medium",
                  trend.value > 0 ? "text-primary" : "text-destructive"
                )}>
                  {trend.value > 0 ? "+" : ""}{trend.value}%
                </span>
                <span className="text-xs text-muted-foreground">{trend.label}</span>
              </div>
            )}
          </div>
          
          <div className={cn(
            "relative flex h-12 w-12 items-center justify-center rounded-lg",
            gradient 
              ? "bg-primary/10 border border-primary/20" 
              : "bg-muted"
          )}>
            <Icon className={cn(
              "h-6 w-6",
              gradient ? "text-primary" : "text-muted-foreground"
            )} />
            {gradient && (
              <div className="absolute inset-0 rounded-lg bg-primary/5 animate-pulse" />
            )}
          </div>
        </div>

        {gradient && (
          <>
            <div className="absolute top-0 right-0 h-16 w-16 -translate-y-8 translate-x-8 rounded-full bg-primary/10 blur-xl" />
            <div className="absolute bottom-0 left-0 h-12 w-12 -translate-x-6 translate-y-6 rounded-full bg-primary/5 blur-lg" />
          </>
        )}
      </CardContent>
    </Card>
  );
}