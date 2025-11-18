"""Responsive design utilities for EduChat.

Defines breakpoints and responsive helper functions for mobile-first design.
"""

# Breakpoints (mobile-first)
BREAKPOINTS = {
    "mobile": "0px",      # 0-767px
    "tablet": "768px",    # 768-1023px
    "desktop": "1024px",  # 1024px+
}

# Responsive display utilities
def mobile_only() -> dict:
    """Show only on mobile devices (<768px)."""
    return {
        "display": ["flex", "flex", "none"],  # mobile, tablet, desktop
    }

def tablet_up() -> dict:
    """Show on tablet and desktop (≥768px)."""
    return {
        "display": ["none", "flex", "flex"],  # mobile, tablet, desktop
    }

def desktop_only() -> dict:
    """Show only on desktop (≥1024px)."""
    return {
        "display": ["none", "none", "flex"],  # mobile, tablet, desktop
    }

# Responsive sizing
def responsive_width(mobile: str, tablet: str, desktop: str) -> dict:
    """Responsive width across breakpoints."""
    return {
        "width": [mobile, tablet, desktop],
    }

def responsive_padding(mobile: str, tablet: str, desktop: str) -> dict:
    """Responsive padding across breakpoints."""
    return {
        "padding": [mobile, tablet, desktop],
    }

def responsive_font_size(mobile: str, tablet: str, desktop: str) -> dict:
    """Responsive font size across breakpoints."""
    return {
        "font_size": [mobile, tablet, desktop],
    }

# Layout utilities
def sidebar_responsive() -> dict:
    """Responsive styles for sidebar.
    
    Mobile: Fixed position, off-screen by default, slides in when open
    Tablet: Toggleable, 220px width when open
    Desktop: Always visible, 220px fixed width
    """
    return {
        "width": ["100%", "220px", "220px"],
        "position": ["fixed", "relative", "relative"],
        "left": ["-100%", "0", "0"],  # Off-screen on mobile
        "z_index": ["1000", "auto", "auto"],
        "transition": "left 0.3s ease",
    }

def chat_responsive() -> dict:
    """Responsive styles for chat container.
    
    Mobile: Full width
    Tablet: Flex-grow to fill space
    Desktop: Max 1200px with margins
    """
    return {
        "width": ["100%", "auto", "auto"],
        "max_width": ["100%", "100%", "1200px"],
        "flex": ["1", "1", "1"],
    }

def container_responsive() -> dict:
    """Responsive container with max width and centering."""
    return {
        "max_width": ["100%", "100%", "1200px"],
        "margin": ["0", "0", "0 auto"],
        "padding": ["1rem", "1.5rem", "2rem"],
    }

