"""Performance monitoring utilities for EduChat."""

import time
from typing import Dict, List, Optional
from datetime import datetime
import reflex as rx


class PerformanceMetrics:
    """Track performance metrics for the application."""
    
    def __init__(self):
        self.metrics: List[Dict] = []
        self.response_times: List[float] = []
        self.error_count: int = 0
        self.total_requests: int = 0
    
    def record_response_time(self, duration: float, endpoint: str = "ai_chat"):
        """Record API response time.
        
        Args:
            duration: Response time in seconds
            endpoint: API endpoint name
        """
        self.response_times.append(duration)
        self.total_requests += 1
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "type": "response_time",
            "endpoint": endpoint,
            "duration": duration,
            "status": "success" if duration < 2.0 else "slow",
        }
        self.metrics.append(metric)
    
    def record_error(self, error_type: str, message: str):
        """Record error occurrence.
        
        Args:
            error_type: Type of error (timeout, api_error, etc.)
            message: Error message
        """
        self.error_count += 1
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "type": "error",
            "error_type": error_type,
            "message": message,
        }
        self.metrics.append(metric)
    
    def get_average_response_time(self) -> float:
        """Calculate average response time.
        
        Returns:
            Average response time in seconds
        """
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def get_p95_response_time(self) -> float:
        """Calculate 95th percentile response time.
        
        Returns:
            P95 response time in seconds
        """
        if not self.response_times:
            return 0.0
        
        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * 0.95)
        return sorted_times[index] if index < len(sorted_times) else sorted_times[-1]
    
    def get_error_rate(self) -> float:
        """Calculate error rate as percentage.
        
        Returns:
            Error rate (0-100)
        """
        if self.total_requests == 0:
            return 0.0
        return (self.error_count / self.total_requests) * 100
    
    def get_summary(self) -> Dict:
        """Get performance summary.
        
        Returns:
            Dictionary with performance statistics
        """
        return {
            "total_requests": self.total_requests,
            "error_count": self.error_count,
            "error_rate": round(self.get_error_rate(), 2),
            "avg_response_time": round(self.get_average_response_time(), 3),
            "p95_response_time": round(self.get_p95_response_time(), 3),
            "total_metrics": len(self.metrics),
        }
    
    def clear_metrics(self):
        """Clear all stored metrics."""
        self.metrics.clear()
        self.response_times.clear()
        self.error_count = 0
        self.total_requests = 0


# Global performance tracker instance
_performance_tracker: Optional[PerformanceMetrics] = None


def get_performance_tracker() -> PerformanceMetrics:
    """Get or create global performance tracker instance.
    
    Returns:
        PerformanceMetrics instance
    """
    global _performance_tracker
    if _performance_tracker is None:
        _performance_tracker = PerformanceMetrics()
    return _performance_tracker


class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
        self.duration = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = time.time() - self.start_time
        
        # Record to performance tracker
        tracker = get_performance_tracker()
        if exc_type is None:
            tracker.record_response_time(self.duration, self.operation_name)
        else:
            tracker.record_error(
                error_type=exc_type.__name__ if exc_type else "unknown",
                message=str(exc_val) if exc_val else "Unknown error"
            )
        
        return False  # Don't suppress exceptions


def measure_performance(func):
    """Decorator to measure function performance.
    
    Args:
        func: Function to measure
    
    Returns:
        Wrapped function
    """
    async def async_wrapper(*args, **kwargs):
        with PerformanceTimer(func.__name__):
            return await func(*args, **kwargs)
    
    def sync_wrapper(*args, **kwargs):
        with PerformanceTimer(func.__name__):
            return func(*args, **kwargs)
    
    # Return appropriate wrapper based on function type
    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


# Client-side performance monitoring script
CLIENT_PERFORMANCE_SCRIPT = """
// Track First Contentful Paint (FCP)
const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        if (entry.name === 'first-contentful-paint') {
            console.log('FCP:', entry.startTime);
        }
    }
});
observer.observe({ entryTypes: ['paint'] });

// Track Time to Interactive (TTI)
window.addEventListener('load', () => {
    const loadTime = performance.now();
    console.log('Load time:', loadTime);
});

// Track Cumulative Layout Shift (CLS)
let clsScore = 0;
const clsObserver = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
            clsScore += entry.value;
        }
    }
    console.log('CLS:', clsScore);
});
clsObserver.observe({ entryTypes: ['layout-shift'] });
"""
