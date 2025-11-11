"""Error handling test suite for EduChat."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from educhat.services.ai_service import AIService
from educhat.state.app_state import AppState


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_timeout_error(self):
        """Test timeout error handling."""
        # Mock AI service with timeout
        with patch('educhat.services.ai_service.get_ai_service') as mock_service:
            mock_service.return_value.chat = AsyncMock(side_effect=TimeoutError("Request timeout"))
            
            state = AppState()
            state.user_input = "Test question"
            
            await state.send_message()
            
            # Check error message was added
            assert len(state.messages) == 2  # User + error message
            assert "duurt te lang" in state.messages[-1]["content"]
            assert state.messages[-1]["is_error"] == True
    
    @pytest.mark.asyncio
    async def test_api_connection_error(self):
        """Test API connection error handling."""
        with patch('educhat.services.ai_service.get_ai_service') as mock_service:
            mock_service.return_value.chat = AsyncMock(side_effect=ConnectionError("No internet"))
            
            state = AppState()
            state.user_input = "Test question"
            
            await state.send_message()
            
            # Check generic error message
            assert len(state.messages) == 2
            assert "misgegaan" in state.messages[-1]["content"]
    
    @pytest.mark.asyncio
    async def test_rate_limit_error(self):
        """Test rate limit error handling."""
        from openai import RateLimitError
        
        with patch('educhat.services.ai_service.get_ai_service') as mock_service:
            mock_service.return_value.chat = AsyncMock(side_effect=RateLimitError("Rate limit exceeded"))
            
            state = AppState()
            state.user_input = "Test question"
            
            await state.send_message()
            
            # Should handle gracefully
            assert len(state.messages) == 2
            assert not state.is_loading
    
    def test_empty_input(self):
        """Test empty input handling."""
        state = AppState()
        state.user_input = ""
        
        # Should not add message
        initial_count = len(state.messages)
        asyncio.run(state.send_message())
        
        assert len(state.messages) == initial_count
    
    def test_whitespace_input(self):
        """Test whitespace-only input handling."""
        state = AppState()
        state.user_input = "   \n\t   "
        
        # Should not add message
        initial_count = len(state.messages)
        asyncio.run(state.send_message())
        
        assert len(state.messages) == initial_count
    
    @pytest.mark.asyncio
    async def test_invalid_context(self):
        """Test handling of invalid user context."""
        with patch('educhat.services.ai_service.get_ai_service') as mock_service:
            mock_service.return_value.chat = AsyncMock(return_value="Response")
            
            state = AppState()
            state.user_context = {"invalid": "data"}  # Invalid context
            state.user_input = "Test question"
            
            # Should still work
            await state.send_message()
            
            assert len(state.messages) == 2
            assert not state.is_loading
    
    def test_feedback_invalid_index(self):
        """Test feedback with invalid message index."""
        state = AppState()
        state.messages = [
            {"content": "User msg", "is_user": True},
            {"content": "Bot msg", "is_user": False},
        ]
        
        # Try invalid indices
        asyncio.run(state.handle_message_feedback(-1, "like"))  # Negative
        asyncio.run(state.handle_message_feedback(10, "like"))  # Out of range
        
        # Messages should be unchanged
        assert len(state.messages) == 2
        assert "feedback" not in state.messages[0]
        assert "feedback" not in state.messages[1]
    
    def test_regenerate_invalid_index(self):
        """Test regenerate with invalid message index."""
        state = AppState()
        state.messages = [
            {"content": "User msg", "is_user": True},
            {"content": "Bot msg", "is_user": False},
        ]
        
        initial_count = len(state.messages)
        
        # Try invalid index
        asyncio.run(state.regenerate_response(0))  # First message (user)
        
        # Should not change messages
        assert len(state.messages) == initial_count


class TestPerformanceMetrics:
    """Test performance monitoring."""
    
    def test_response_time_tracking(self):
        """Test response time is tracked."""
        from educhat.utils.performance import get_performance_tracker
        
        tracker = get_performance_tracker()
        tracker.clear_metrics()
        
        # Record some response times
        tracker.record_response_time(0.5, "test_endpoint")
        tracker.record_response_time(1.2, "test_endpoint")
        tracker.record_response_time(0.8, "test_endpoint")
        
        # Check average
        avg = tracker.get_average_response_time()
        assert 0.7 < avg < 0.9
        
        # Check summary
        summary = tracker.get_summary()
        assert summary["total_requests"] == 3
        assert summary["error_count"] == 0
    
    def test_error_rate_calculation(self):
        """Test error rate calculation."""
        from educhat.utils.performance import get_performance_tracker
        
        tracker = get_performance_tracker()
        tracker.clear_metrics()
        
        # Record mix of success and errors
        tracker.record_response_time(0.5, "test")
        tracker.record_response_time(0.6, "test")
        tracker.record_error("timeout", "Timeout error")
        tracker.record_response_time(0.7, "test")
        tracker.record_error("api_error", "API error")
        
        # Check error rate (2 errors / 5 requests = 40%)
        error_rate = tracker.get_error_rate()
        assert 35 < error_rate < 45


class TestCaching:
    """Test caching functionality."""
    
    def test_cache_hit(self):
        """Test cache hit scenario."""
        from educhat.utils.cache import get_response_cache
        
        cache = get_response_cache()
        cache.clear()
        
        # Set and get
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        
        assert value == "test_value"
        assert cache.hits == 1
        assert cache.misses == 0
    
    def test_cache_miss(self):
        """Test cache miss scenario."""
        from educhat.utils.cache import get_response_cache
        
        cache = get_response_cache()
        cache.clear()
        
        # Get non-existent key
        value = cache.get("nonexistent")
        
        assert value is None
        assert cache.misses == 1
        assert cache.hits == 0
    
    def test_cache_expiration(self):
        """Test cache expiration."""
        from educhat.utils.cache import SimpleCache
        import time
        
        cache = SimpleCache(default_ttl=1)  # 1 second TTL
        cache.set("test_key", "test_value")
        
        # Should be available immediately
        assert cache.get("test_key") == "test_value"
        
        # Wait for expiration
        time.sleep(1.5)
        
        # Should be expired
        assert cache.get("test_key") is None
    
    def test_cache_stats(self):
        """Test cache statistics."""
        from educhat.utils.cache import get_response_cache
        
        cache = get_response_cache()
        cache.clear()
        
        # Perform some operations
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.get("key1")  # Hit
        cache.get("key1")  # Hit
        cache.get("key3")  # Miss
        
        stats = cache.get_stats()
        assert stats["size"] == 2
        assert stats["hits"] == 2
        assert stats["misses"] == 1
        assert stats["hit_rate"] == pytest.approx(66.67, rel=0.1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
