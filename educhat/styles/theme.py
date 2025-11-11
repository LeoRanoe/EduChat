"""Theme and styling configuration for EduChat."""

import reflex as rx

# Color palette (based on design requirements)
COLORS = {
    "primary_green": "#228B22",      # Forest Green (main brand color)
    "light_green": "#90EE90",        # Light Green
    "dark_green": "#006400",         # Dark Green (hover states)
    "white": "#FFFFFF",
    "light_gray": "#F5F5F5",         # Background gray
    "gray": "#808080",               # Text gray
    "dark_gray": "#333333",          # Dark text
    "border_gray": "#E0E0E0",        # Border color
    "black": "#000000",
}

# Typography
FONTS = {
    "heading": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "body": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
}

# Font sizes
FONT_SIZES = {
    "xs": "0.75rem",      # 12px
    "sm": "0.875rem",     # 14px
    "base": "1rem",       # 16px
    "lg": "1.125rem",     # 18px
    "xl": "1.25rem",      # 20px
    "2xl": "1.5rem",      # 24px
    "3xl": "1.875rem",    # 30px
    "4xl": "2.25rem",     # 36px
}

# Spacing
SPACING = {
    "xs": "0.25rem",      # 4px
    "sm": "0.5rem",       # 8px
    "md": "1rem",         # 16px
    "lg": "1.5rem",       # 24px
    "xl": "2rem",         # 32px
    "2xl": "3rem",        # 48px
}

# Border radius
RADIUS = {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "9999px",
}

# Breakpoints for responsive design
BREAKPOINTS = {
    "mobile": "768px",
    "tablet": "1024px",
    "desktop": "1200px",
}

# Global styles
def get_global_styles():
    """Get global CSS styles for the app."""
    return {
        "body": {
            "margin": "0",
            "padding": "0",
            "font_family": FONTS["body"],
            "background": COLORS["light_gray"],
            "color": COLORS["dark_gray"],
        },
        "*": {
            "box-sizing": "border-box",
        },
    }
