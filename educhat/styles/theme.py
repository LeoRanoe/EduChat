"""Theme and styling configuration for EduChat.

A comprehensive design system providing:
- Professional color palette with proper contrast ratios
- Typography hierarchy with Inter font family
- Standardized spacing scale (4px base)
- Elevation/shadow system
- Animation and transition presets
"""

import reflex as rx

# =============================================================================
# COLOR SYSTEM
# Professional palette with WCAG 2.1 AA compliant contrast ratios
# =============================================================================
COLORS = {
    # Brand Colors
    "primary": "#10A37F",            # Primary brand green
    "primary_green": "#10A37F",      # Alias for compatibility
    "primary_hover": "#0D8F6F",      # Primary hover state
    "primary_active": "#0A7B5F",     # Primary active/pressed state
    "primary_light": "#E6F7F1",      # Light green tint for backgrounds
    "primary_muted": "rgba(16, 163, 127, 0.1)",  # Muted primary for subtle bg
    
    # Legacy aliases for compatibility
    "light_green": "#E6F7F1",
    "dark_green": "#0D8F6F",
    
    # Neutral Colors (Gray Scale)
    "white": "#FFFFFF",
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",
    "black": "#030712",
    
    # Background Colors
    "background": "#F9FAFB",
    "background_secondary": "#FFFFFF",
    "background_tertiary": "#F3F4F6",
    "surface": "#FFFFFF",
    "surface_hover": "#F9FAFB",
    "surface_active": "#F3F4F6",
    
    # Legacy aliases
    "light_gray": "#F3F4F6",
    "gray": "#9CA3AF",
    "dark_gray": "#374151",
    
    # Text Colors (with proper contrast)
    "text_primary": "#111827",       # 15.8:1 contrast on white
    "text_secondary": "#4B5563",     # 7.5:1 contrast on white
    "text_tertiary": "#6B7280",      # 5.4:1 contrast on white
    "text_muted": "#9CA3AF",         # 3.0:1 (decorative only)
    "text_on_primary": "#FFFFFF",    # For text on primary color
    
    # Border Colors
    "border": "#E5E7EB",
    "border_gray": "#E5E7EB",
    "border_light": "#F3F4F6",
    "border_dark": "#D1D5DB",
    "border_focus": "#10A37F",
    
    # Semantic/Functional Colors
    "success": "#059669",            # Darker green for better contrast
    "success_light": "#D1FAE5",
    "success_dark": "#047857",
    
    "error": "#DC2626",              # Red for errors
    "error_light": "#FEE2E2",
    "error_dark": "#B91C1C",
    
    "warning": "#D97706",            # Orange for warnings
    "warning_light": "#FEF3C7",
    "warning_dark": "#B45309",
    
    "info": "#2563EB",               # Blue for info
    "info_light": "#DBEAFE",
    "info_dark": "#1D4ED8",
    
    # Interactive States
    "hover_bg": "#F9FAFB",
    "active_bg": "#F3F4F6",
    "focus_ring": "rgba(16, 163, 127, 0.4)",
    "disabled_bg": "#F3F4F6",
    "disabled_text": "#9CA3AF",
    
    # Shadow Colors
    "shadow_xs": "rgba(0, 0, 0, 0.03)",
    "shadow_sm": "rgba(0, 0, 0, 0.05)",
    "shadow": "rgba(0, 0, 0, 0.05)",
    "shadow_md": "rgba(0, 0, 0, 0.1)",
    "shadow_lg": "rgba(0, 0, 0, 0.15)",
    "shadow_primary": "rgba(16, 163, 127, 0.25)",
    
    # Overlay Colors
    "overlay": "rgba(0, 0, 0, 0.5)",
    "overlay_light": "rgba(0, 0, 0, 0.3)",
}

# =============================================================================
# DARK MODE COLORS
# =============================================================================
DARK_COLORS = {
    # Brand Colors (keep consistent)
    "primary": "#10A37F",
    "primary_green": "#10A37F",
    "primary_hover": "#34D399",
    "primary_active": "#6EE7B7",
    "primary_light": "#1A3D33",
    "primary_muted": "rgba(16, 163, 127, 0.15)",
    "light_green": "#1A3D33",
    "dark_green": "#34D399",
    
    # Neutral Colors (inverted)
    "white": "#1F2937",
    "gray_50": "#1F2937",
    "gray_100": "#374151",
    "gray_200": "#4B5563",
    "gray_300": "#6B7280",
    "gray_400": "#9CA3AF",
    "gray_500": "#D1D5DB",
    "gray_600": "#E5E7EB",
    "gray_700": "#F3F4F6",
    "gray_800": "#F9FAFB",
    "gray_900": "#FFFFFF",
    "black": "#FFFFFF",
    
    # Background Colors
    "background": "#0F172A",
    "background_secondary": "#1E293B",
    "background_tertiary": "#334155",
    "surface": "#1E293B",
    "surface_hover": "#334155",
    "surface_active": "#475569",
    "light_gray": "#1F2937",
    "gray": "#9CA3AF",
    "dark_gray": "#D1D5DB",
    
    # Text Colors
    "text_primary": "#F9FAFB",
    "text_secondary": "#D1D5DB",
    "text_tertiary": "#9CA3AF",
    "text_muted": "#6B7280",
    "text_on_primary": "#FFFFFF",
    
    # Border Colors
    "border": "#374151",
    "border_gray": "#374151",
    "border_light": "#1F2937",
    "border_dark": "#4B5563",
    "border_focus": "#10A37F",
    
    # Semantic Colors (slightly adjusted for dark bg)
    "success": "#34D399",
    "success_light": "#064E3B",
    "success_dark": "#6EE7B7",
    "error": "#F87171",
    "error_light": "#7F1D1D",
    "error_dark": "#FCA5A5",
    "warning": "#FBBF24",
    "warning_light": "#78350F",
    "warning_dark": "#FCD34D",
    "info": "#60A5FA",
    "info_light": "#1E3A8A",
    "info_dark": "#93C5FD",
    
    # Interactive States
    "hover_bg": "#374151",
    "active_bg": "#4B5563",
    "focus_ring": "rgba(16, 163, 127, 0.5)",
    "disabled_bg": "#1F2937",
    "disabled_text": "#4B5563",
    
    # Shadow Colors
    "shadow_xs": "rgba(0, 0, 0, 0.2)",
    "shadow_sm": "rgba(0, 0, 0, 0.3)",
    "shadow": "rgba(0, 0, 0, 0.3)",
    "shadow_md": "rgba(0, 0, 0, 0.4)",
    "shadow_lg": "rgba(0, 0, 0, 0.5)",
    "shadow_primary": "rgba(16, 163, 127, 0.3)",
    
    # Overlay Colors
    "overlay": "rgba(0, 0, 0, 0.7)",
    "overlay_light": "rgba(0, 0, 0, 0.5)",
}

# =============================================================================
# TYPOGRAPHY
# Professional font stack with Inter as primary
# =============================================================================
FONTS = {
    "heading": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "body": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "mono": "'JetBrains Mono', 'Fira Code', 'Monaco', 'Consolas', monospace",
}

# Font Weights
FONT_WEIGHTS = {
    "normal": "400",
    "medium": "500",
    "semibold": "600",
    "bold": "700",
    "extrabold": "800",
}

# Font Sizes - Based on 16px base (rem units)
FONT_SIZES = {
    "2xs": "0.625rem",    # 10px
    "xs": "0.75rem",      # 12px
    "sm": "0.875rem",     # 14px
    "base": "1rem",       # 16px
    "lg": "1.125rem",     # 18px
    "xl": "1.25rem",      # 20px
    "2xl": "1.5rem",      # 24px
    "3xl": "1.875rem",    # 30px
    "4xl": "2.25rem",     # 36px
    "5xl": "3rem",        # 48px
    "6xl": "3.75rem",     # 60px
}

# Line Heights
LINE_HEIGHTS = {
    "tight": "1.25",
    "snug": "1.375",
    "normal": "1.5",
    "relaxed": "1.625",
    "loose": "1.75",
}

# =============================================================================
# SPACING SCALE
# Based on 4px unit (0.25rem)
# =============================================================================
SPACING = {
    "0": "0",
    "px": "1px",
    "0.5": "0.125rem",    # 2px
    "1": "0.25rem",       # 4px
    "1.5": "0.375rem",    # 6px
    "2": "0.5rem",        # 8px
    "2.5": "0.625rem",    # 10px
    "3": "0.75rem",       # 12px
    "3.5": "0.875rem",    # 14px
    "4": "1rem",          # 16px
    "5": "1.25rem",       # 20px
    "6": "1.5rem",        # 24px
    "7": "1.75rem",       # 28px
    "8": "2rem",          # 32px
    "9": "2.25rem",       # 36px
    "10": "2.5rem",       # 40px
    "11": "2.75rem",      # 44px
    "12": "3rem",         # 48px
    "14": "3.5rem",       # 56px
    "16": "4rem",         # 64px
    "20": "5rem",         # 80px
    "24": "6rem",         # 96px
    # Aliases for backward compatibility
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem",
}

# =============================================================================
# BORDER RADIUS
# =============================================================================
RADIUS = {
    "none": "0",
    "xs": "2px",
    "sm": "4px",
    "md": "6px",
    "lg": "8px",
    "xl": "12px",
    "2xl": "16px",
    "3xl": "24px",
    "full": "9999px",
    "pill": "9999px",
}

# =============================================================================
# SHADOWS (Elevation System)
# =============================================================================
SHADOWS = {
    "none": "none",
    "xs": "0 1px 2px rgba(0, 0, 0, 0.05)",
    "sm": "0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
    "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
    # Colored shadows for branded elements
    "primary_sm": "0 2px 8px rgba(16, 163, 127, 0.2)",
    "primary_md": "0 4px 14px rgba(16, 163, 127, 0.25)",
    "primary_lg": "0 8px 24px rgba(16, 163, 127, 0.3)",
    # Focus ring shadows
    "focus": "0 0 0 3px rgba(16, 163, 127, 0.4)",
    "focus_error": "0 0 0 3px rgba(220, 38, 38, 0.4)",
}

# =============================================================================
# TRANSITIONS & ANIMATIONS
# =============================================================================
TRANSITIONS = {
    "fast": "150ms cubic-bezier(0.4, 0, 0.2, 1)",
    "normal": "200ms cubic-bezier(0.4, 0, 0.2, 1)",
    "slow": "300ms cubic-bezier(0.4, 0, 0.2, 1)",
    "slower": "500ms cubic-bezier(0.4, 0, 0.2, 1)",
    # Specific transitions
    "colors": "color 200ms, background-color 200ms, border-color 200ms",
    "transform": "transform 200ms cubic-bezier(0.4, 0, 0.2, 1)",
    "all": "all 200ms cubic-bezier(0.4, 0, 0.2, 1)",
    "bounce": "300ms cubic-bezier(0.68, -0.55, 0.265, 1.55)",
}

# =============================================================================
# Z-INDEX SCALE
# =============================================================================
Z_INDEX = {
    "dropdown": "100",
    "sticky": "200",
    "fixed": "300",
    "modal_backdrop": "400",
    "modal": "500",
    "popover": "600",
    "tooltip": "700",
    "toast": "800",
}

# =============================================================================
# BREAKPOINTS
# Mobile-first responsive design
# =============================================================================
BREAKPOINTS = {
    "xs": "475px",
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px",
    # Legacy aliases
    "mobile": "768px",
    "tablet": "1024px",
    "desktop": "1200px",
}

# =============================================================================
# COMPONENT PRESETS
# Reusable style combinations for common patterns
# =============================================================================
BUTTON_STYLES = {
    "primary": {
        "background": f"linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_hover']} 100%)",
        "color": COLORS["text_on_primary"],
        "border": "none",
        "border_radius": RADIUS["lg"],
        "padding": "0.75rem 1.5rem",
        "font_weight": FONT_WEIGHTS["semibold"],
        "transition": TRANSITIONS["normal"],
        "box_shadow": SHADOWS["primary_sm"],
        "_hover": {
            "transform": "translateY(-2px)",
            "box_shadow": SHADOWS["primary_md"],
        },
        "_active": {
            "transform": "translateY(0)",
        },
        "_disabled": {
            "opacity": "0.5",
            "cursor": "not-allowed",
        },
    },
    "secondary": {
        "background": COLORS["white"],
        "color": COLORS["text_primary"],
        "border": f"1px solid {COLORS['border']}",
        "border_radius": RADIUS["lg"],
        "padding": "0.75rem 1.5rem",
        "font_weight": FONT_WEIGHTS["medium"],
        "transition": TRANSITIONS["normal"],
        "box_shadow": SHADOWS["xs"],
        "_hover": {
            "background": COLORS["gray_50"],
            "border_color": COLORS["gray_300"],
        },
    },
    "ghost": {
        "background": "transparent",
        "color": COLORS["text_secondary"],
        "border": "none",
        "padding": "0.5rem 1rem",
        "_hover": {
            "background": COLORS["gray_100"],
            "color": COLORS["text_primary"],
        },
    },
}

INPUT_STYLES = {
    "default": {
        "background": COLORS["white"],
        "border": f"1px solid {COLORS['border']}",
        "border_radius": RADIUS["lg"],
        "padding": "0.75rem 1rem",
        "font_size": FONT_SIZES["base"],
        "transition": TRANSITIONS["normal"],
        "_focus": {
            "outline": "none",
            "border_color": COLORS["primary"],
            "box_shadow": SHADOWS["focus"],
        },
        "_placeholder": {
            "color": COLORS["text_muted"],
        },
    },
    "error": {
        "border_color": COLORS["error"],
        "_focus": {
            "border_color": COLORS["error"],
            "box_shadow": SHADOWS["focus_error"],
        },
    },
}

CARD_STYLES = {
    "default": {
        "background": COLORS["white"],
        "border": f"1px solid {COLORS['border_light']}",
        "border_radius": RADIUS["xl"],
        "padding": "1.5rem",
        "box_shadow": SHADOWS["sm"],
        "transition": TRANSITIONS["normal"],
    },
    "elevated": {
        "background": COLORS["white"],
        "border": "none",
        "border_radius": RADIUS["xl"],
        "padding": "1.5rem",
        "box_shadow": SHADOWS["lg"],
    },
    "interactive": {
        "background": COLORS["white"],
        "border": f"1px solid {COLORS['border_light']}",
        "border_radius": RADIUS["xl"],
        "padding": "1.5rem",
        "box_shadow": SHADOWS["sm"],
        "transition": TRANSITIONS["normal"],
        "cursor": "pointer",
        "_hover": {
            "border_color": COLORS["primary"],
            "box_shadow": SHADOWS["md"],
            "transform": "translateY(-2px)",
        },
    },
}


# =============================================================================
# GLOBAL STYLES
# =============================================================================
def get_global_styles():
    """Get global CSS styles for the app."""
    return {
        "html": {
            "scroll-behavior": "smooth",
        },
        "body": {
            "margin": "0",
            "padding": "0",
            "font_family": FONTS["body"],
            "font_size": FONT_SIZES["base"],
            "line_height": LINE_HEIGHTS["normal"],
            "background": COLORS["background"],
            "color": COLORS["text_primary"],
            "-webkit-font-smoothing": "antialiased",
            "-moz-osx-font-smoothing": "grayscale",
        },
        "*": {
            "box-sizing": "border-box",
        },
        "*::before, *::after": {
            "box-sizing": "border-box",
        },
        "::selection": {
            "background": COLORS["primary_light"],
            "color": COLORS["primary"],
        },
    }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def get_responsive_value(mobile: str, tablet: str = None, desktop: str = None) -> list:
    """Generate responsive value array for Reflex components.
    
    Args:
        mobile: Value for mobile screens (default)
        tablet: Value for tablet screens (optional, uses mobile if not provided)
        desktop: Value for desktop screens (optional, uses tablet if not provided)
    
    Returns:
        List of values in format [mobile, tablet, desktop]
    """
    return [
        mobile,
        tablet or mobile,
        desktop or tablet or mobile,
    ]


def get_color_with_opacity(color_key: str, opacity: float) -> str:
    """Get a color with modified opacity.
    
    Args:
        color_key: Key from COLORS dict
        opacity: Opacity value between 0 and 1
    
    Returns:
        Color string with opacity (rgba format)
    """
    import re
    color = COLORS.get(color_key, color_key)
    
    # Handle hex colors
    if color.startswith("#"):
        hex_color = color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, {opacity})"
    
    # Handle rgba colors - replace opacity
    if color.startswith("rgba"):
        return re.sub(r",\s*[\d.]+\)$", f", {opacity})", color)
    
    return color

