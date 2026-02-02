"""Theme and styling configuration for EduChat.

A comprehensive design system providing:
- CSS variable-based theming for automatic dark mode support
- Professional color palette with WCAG 2.1 AA compliant contrast ratios
- Typography hierarchy with Inter font family
- Standardized spacing scale (4px base)
- Elevation/shadow system
- Animation and transition presets

IMPORTANT: All components should use CSS variables (var(--xxx)) for colors
to ensure automatic dark mode switching via Reflex's ColorMode system.
"""

import reflex as rx

# =============================================================================
# CSS VARIABLE TOKENS
# These are the ONLY color references components should use.
# They automatically switch between light/dark based on theme.
# =============================================================================

class ThemeTokens:
    """CSS variable tokens for theme-aware styling.
    
    Use these instead of hardcoded colors to ensure dark mode support.
    Example: background=ThemeTokens.bg_primary
    """
    # Brand Colors (same in light/dark)
    primary = "var(--color-primary)"
    primary_hover = "var(--color-primary-hover)"
    primary_active = "var(--color-primary-active)"
    primary_light = "var(--color-primary-light)"
    primary_muted = "var(--color-primary-muted)"
    
    # Backgrounds
    bg_primary = "var(--bg-primary)"
    bg_secondary = "var(--bg-secondary)"
    bg_tertiary = "var(--bg-tertiary)"
    bg_card = "var(--bg-card)"
    bg_input = "var(--bg-input)"
    bg_hover = "var(--bg-hover)"
    bg_active = "var(--bg-active)"
    
    # Text Colors
    text_primary = "var(--text-primary)"
    text_secondary = "var(--text-secondary)"
    text_tertiary = "var(--text-tertiary)"
    text_muted = "var(--text-muted)"
    text_inverse = "var(--text-inverse)"
    text_on_primary = "var(--text-on-primary)"
    
    # Border Colors
    border = "var(--border-color)"
    border_light = "var(--border-light)"
    border_dark = "var(--border-dark)"
    border_focus = "var(--border-focus)"
    
    # Shadows
    shadow_xs = "var(--shadow-xs)"
    shadow_sm = "var(--shadow-sm)"
    shadow_md = "var(--shadow-md)"
    shadow_lg = "var(--shadow-lg)"
    shadow_xl = "var(--shadow-xl)"
    shadow_primary = "var(--shadow-primary)"
    shadow_focus = "var(--shadow-focus)"
    
    # Semantic Colors
    success = "var(--color-success)"
    success_light = "var(--color-success-light)"
    error = "var(--color-error)"
    error_light = "var(--color-error-light)"
    warning = "var(--color-warning)"
    warning_light = "var(--color-warning-light)"
    info = "var(--color-info)"
    info_light = "var(--color-info-light)"
    
    # Overlay
    overlay = "var(--overlay-bg)"
    modal_bg = "var(--modal-bg)"
    
    # Message styling
    message_user_bg = "var(--message-user-bg)"
    message_bot_bg = "var(--message-bot-bg)"
    message_bot_border = "var(--message-bot-border)"
    
    # Navbar specific
    navbar_bg = "var(--navbar-bg)"
    navbar_border = "var(--navbar-border)"
    
    # Sidebar specific
    sidebar_bg = "var(--sidebar-bg)"
    sidebar_border = "var(--sidebar-border)"


# Alias for easier imports
T = ThemeTokens

# =============================================================================
# STATIC COLOR VALUES (for reference/gradients only)
# Use ThemeTokens for component styling!
# =============================================================================
COLORS = {
    # Brand Colors - These are constant regardless of theme
    "primary": "#10A37F",
    "primary_green": "#10A37F",
    "primary_hover": "#0D8F6F",
    "primary_active": "#0A7B5F",
    "primary_light": "#E6F7F1",
    "primary_muted": "rgba(16, 163, 127, 0.1)",
    
    # Legacy aliases for gradient definitions
    "light_green": "#E6F7F1",
    "dark_green": "#0D8F6F",
    
    # Static neutrals (for gradients that need actual values)
    "white": "#FFFFFF",
    "black": "#030712",
    
    # Light mode text (use ThemeTokens.text_* instead in components!)
    "text_primary": "var(--text-primary)",
    "text_secondary": "var(--text-secondary)",
    "text_tertiary": "var(--text-tertiary)",
    "text_muted": "var(--text-muted)",
    "text_on_primary": "#FFFFFF",
    
    # Light mode backgrounds (use ThemeTokens.bg_* instead!)
    "background": "var(--bg-primary)",
    "surface": "var(--bg-card)",
    "hover_bg": "var(--bg-hover)",
    "active_bg": "var(--bg-active)",
    
    # Light mode borders (use ThemeTokens.border* instead!)
    "border": "var(--border-color)",
    "border_gray": "var(--border-color)",
    "border_light": "var(--border-light)",
    "border_dark": "var(--border-dark)",
    
    # Legacy gray scale - mapped to CSS variables
    "gray_50": "var(--bg-primary)",
    "gray_100": "var(--bg-tertiary)",
    "gray_200": "var(--border-color)",
    "gray_300": "var(--border-dark)",
    "gray_400": "var(--text-muted)",
    "gray_500": "var(--text-tertiary)",
    "gray_600": "var(--text-secondary)",
    "gray_700": "var(--text-primary)",
    "gray_800": "var(--text-primary)",
    "gray_900": "var(--text-primary)",
    "light_gray": "var(--bg-tertiary)",
    "gray": "var(--text-muted)",
    "dark_gray": "var(--text-secondary)",
    
    # Semantic Colors
    "success": "var(--color-success)",
    "success_light": "var(--color-success-light)",
    "error": "var(--color-error)",
    "error_light": "var(--color-error-light)",
    "warning": "var(--color-warning)",
    "warning_light": "var(--color-warning-light)",
    "info": "var(--color-info)",
    "info_light": "var(--color-info-light)",
}

# =============================================================================
# TYPOGRAPHY
# =============================================================================
FONTS = {
    "heading": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "body": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "mono": "'JetBrains Mono', 'Fira Code', 'Monaco', 'Consolas', monospace",
}

FONT_WEIGHTS = {
    "normal": "400",
    "medium": "500",
    "semibold": "600",
    "bold": "700",
    "extrabold": "800",
}

FONT_SIZES = {
    "2xs": "0.625rem",
    "xs": "0.75rem",
    "sm": "0.875rem",
    "base": "1rem",
    "lg": "1.125rem",
    "xl": "1.25rem",
    "2xl": "1.5rem",
    "3xl": "1.875rem",
    "4xl": "2.25rem",
    "5xl": "3rem",
    "6xl": "3.75rem",
}

LINE_HEIGHTS = {
    "tight": "1.25",
    "snug": "1.375",
    "normal": "1.5",
    "relaxed": "1.625",
    "loose": "1.75",
}

# =============================================================================
# SPACING SCALE
# =============================================================================
SPACING = {
    "0": "0",
    "px": "1px",
    "0.5": "0.125rem",
    "1": "0.25rem",
    "1.5": "0.375rem",
    "2": "0.5rem",
    "2.5": "0.625rem",
    "3": "0.75rem",
    "3.5": "0.875rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "7": "1.75rem",
    "8": "2rem",
    "9": "2.25rem",
    "10": "2.5rem",
    "11": "2.75rem",
    "12": "3rem",
    "14": "3.5rem",
    "16": "4rem",
    "20": "5rem",
    "24": "6rem",
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
# SHADOWS
# =============================================================================
SHADOWS = {
    "none": "none",
    "xs": "var(--shadow-xs)",
    "sm": "var(--shadow-sm)",
    "md": "var(--shadow-md)",
    "lg": "var(--shadow-lg)",
    "xl": "var(--shadow-xl)",
    "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
    "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
    "primary_sm": "0 2px 8px rgba(16, 163, 127, 0.2)",
    "primary_md": "var(--shadow-primary)",
    "primary_lg": "0 8px 24px rgba(16, 163, 127, 0.3)",
    "focus": "var(--shadow-focus)",
    "focus_error": "0 0 0 3px rgba(220, 38, 38, 0.4)",
}

# =============================================================================
# TRANSITIONS
# =============================================================================
TRANSITIONS = {
    "fast": "150ms cubic-bezier(0.4, 0, 0.2, 1)",
    "normal": "200ms cubic-bezier(0.4, 0, 0.2, 1)",
    "slow": "300ms cubic-bezier(0.4, 0, 0.2, 1)",
    "slower": "500ms cubic-bezier(0.4, 0, 0.2, 1)",
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
# =============================================================================
BREAKPOINTS = {
    "xs": "475px",
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px",
    "mobile": "768px",
    "tablet": "1024px",
    "desktop": "1200px",
}

# =============================================================================
# COMPONENT STYLE PRESETS (using CSS variables)
# =============================================================================
BUTTON_STYLES = {
    "primary": {
        "background": "linear-gradient(135deg, #10A37F 0%, #0D8F6F 100%)",
        "color": "#FFFFFF",
        "border": "none",
        "border_radius": RADIUS["lg"],
        "padding": "0.75rem 1.5rem",
        "font_weight": FONT_WEIGHTS["semibold"],
        "transition": TRANSITIONS["normal"],
        "box_shadow": "0 2px 8px rgba(16, 163, 127, 0.2)",
        "_hover": {
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 14px rgba(16, 163, 127, 0.25)",
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
        "background": T.bg_card,
        "color": T.text_primary,
        "border": f"1px solid {T.border}",
        "border_radius": RADIUS["lg"],
        "padding": "0.75rem 1.5rem",
        "font_weight": FONT_WEIGHTS["medium"],
        "transition": TRANSITIONS["normal"],
        "box_shadow": T.shadow_xs,
        "_hover": {
            "background": T.bg_hover,
            "border_color": T.border_dark,
        },
    },
    "ghost": {
        "background": "transparent",
        "color": T.text_secondary,
        "border": "none",
        "padding": "0.5rem 1rem",
        "_hover": {
            "background": T.bg_hover,
            "color": T.text_primary,
        },
    },
}

INPUT_STYLES = {
    "default": {
        "background": T.bg_input,
        "border": f"1px solid {T.border}",
        "border_radius": RADIUS["lg"],
        "padding": "0.75rem 1rem",
        "font_size": FONT_SIZES["base"],
        "color": T.text_primary,
        "transition": TRANSITIONS["normal"],
        "_focus": {
            "outline": "none",
            "border_color": T.border_focus,
            "box_shadow": T.shadow_focus,
        },
        "_placeholder": {
            "color": T.text_muted,
        },
    },
}

CARD_STYLES = {
    "default": {
        "background": T.bg_card,
        "border": f"1px solid {T.border_light}",
        "border_radius": RADIUS["xl"],
        "padding": "1.5rem",
        "box_shadow": T.shadow_sm,
        "transition": TRANSITIONS["normal"],
    },
    "elevated": {
        "background": T.bg_card,
        "border": "none",
        "border_radius": RADIUS["xl"],
        "padding": "1.5rem",
        "box_shadow": T.shadow_lg,
    },
    "interactive": {
        "background": T.bg_card,
        "border": f"1px solid {T.border_light}",
        "border_radius": RADIUS["xl"],
        "padding": "1.5rem",
        "box_shadow": T.shadow_sm,
        "transition": TRANSITIONS["normal"],
        "cursor": "pointer",
        "_hover": {
            "border_color": T.primary,
            "box_shadow": T.shadow_md,
            "transform": "translateY(-2px)",
        },
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def get_responsive_value(mobile: str, tablet: str = None, desktop: str = None) -> list:
    """Generate responsive value array for Reflex components."""
    return [
        mobile,
        tablet or mobile,
        desktop or tablet or mobile,
    ]


def get_color_with_opacity(color_key: str, opacity: float) -> str:
    """Get a color with modified opacity (for static colors only)."""
    import re
    
    # Static color values for opacity calculations
    static_colors = {
        "primary": "#10A37F",
        "primary_green": "#10A37F",
        "primary_hover": "#0D8F6F",
        "white": "#FFFFFF",
        "black": "#030712",
    }
    
    color = static_colors.get(color_key, color_key)
    
    if color.startswith("#"):
        hex_color = color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, {opacity})"
    
    if color.startswith("rgba"):
        return re.sub(r",\s*[\d.]+\)$", f", {opacity})", color)
    
    return color

