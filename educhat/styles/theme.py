"""Theme and styling configuration for EduChat."""

import reflex as rx

# Color palette (Modern enhanced design)
COLORS = {
    "primary_green": "#10A37F",      # Modern teal green (main brand)
    "light_green": "#E6F7F1",        # Very light green background
    "dark_green": "#0E8B6A",         # Darker green for hover
    "white": "#FFFFFF",
    "background": "#F9FAFB",         # Off-white background
    "light_gray": "#F3F4F6",         # Light gray background
    "gray": "#9CA3AF",               # Medium gray text
    "dark_gray": "#374151",          # Dark gray text
    "border_gray": "#E5E7EB",        # Border color
    "border_light": "#F3F4F6",       # Lighter border
    "black": "#111827",
    # Text colors for hierarchy
    "text_primary": "#111827",       # Almost black for primary text
    "text_secondary": "#6B7280",     # Medium gray for secondary
    "text_tertiary": "#9CA3AF",      # Light gray for tertiary
    # Functional colors
    "success": "#10B981",            # Green for success
    "error": "#EF4444",              # Red for errors
    "warning": "#F59E0B",            # Orange for warnings
    "info": "#3B82F6",               # Blue for info
    # UI element colors
    "hover_bg": "#F9FAFB",           # Hover background
    "active_bg": "#F3F4F6",          # Active/selected background
    "shadow": "rgba(0, 0, 0, 0.05)", # Subtle shadow
    "shadow_md": "rgba(0, 0, 0, 0.1)", # Medium shadow
    "border": "#E5E7EB",             # Border color alias
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

# Border radius (Modern, more rounded)
RADIUS = {
    "xs": "4px",
    "sm": "6px",
    "md": "10px",
    "lg": "14px",
    "xl": "18px",
    "2xl": "24px",
    "full": "9999px",
    "pill": "28px",  # For pill-shaped buttons
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

