"""Button components for EduChat.

Professional button system with:
- Multiple variants (primary, secondary, ghost, danger)
- Loading states with spinners
- Disabled states with proper visual feedback
- Smooth hover animations and micro-interactions
- Touch-friendly sizing (44px minimum)
- Accessibility compliant focus states
"""

import reflex as rx
from typing import Optional, Callable, Literal
from educhat.styles.theme import COLORS, RADIUS, SHADOWS, TRANSITIONS


ButtonVariant = Literal["primary", "secondary", "ghost", "danger", "outline"]
ButtonSize = Literal["sm", "md", "lg"]


def primary_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    icon_right: Optional[str] = None,
    is_loading: bool = False,
    is_disabled: bool = False,
    width: str = "auto",
    size: ButtonSize = "md",
    class_name: str = "",
) -> rx.Component:
    """Modern primary button with gradient background and shadow.
    
    Args:
        text: Button text
        on_click: Click handler function
        icon: Optional icon name (left side)
        icon_right: Optional icon name (right side)
        is_loading: Loading state - shows spinner
        is_disabled: Disabled state
        width: Button width
        size: Button size - sm, md, lg
        class_name: Additional CSS class
    """
    # Size configurations
    sizes = {
        "sm": {
            "padding": "0.5rem 1rem",
            "font_size": "0.8125rem",
            "min_height": "36px",
            "icon_size": 14,
        },
        "md": {
            "padding": "0.75rem 1.5rem",
            "font_size": "0.9375rem",
            "min_height": "44px",
            "icon_size": 18,
        },
        "lg": {
            "padding": "1rem 2rem",
            "font_size": "1rem",
            "min_height": "52px",
            "icon_size": 20,
        },
    }
    
    config = sizes.get(size, sizes["md"])
    
    return rx.button(
        rx.hstack(
            # Loading spinner
            rx.cond(
                is_loading,
                rx.box(
                    rx.spinner(size="1", color="white"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.cond(
                    icon,
                    rx.icon(icon, size=config["icon_size"], flex_shrink="0"),
                    rx.fragment(),
                ),
            ),
            rx.text(
                text, 
                font_size=config["font_size"],
                white_space="nowrap",
                opacity=rx.cond(is_loading, "0.7", "1"),
            ),
            rx.cond(
                icon_right,
                rx.icon(icon_right, size=config["icon_size"], flex_shrink="0"),
                rx.fragment(),
            ),
            spacing="2",
            align="center",
            justify="center",
            width="100%",
        ),
        on_click=rx.cond(is_disabled | is_loading, None, on_click),
        background=f"linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_hover']} 100%)",
        color=COLORS["text_on_primary"],
        border="none",
        border_radius=RADIUS["lg"],
        padding=config["padding"],
        cursor=rx.cond(is_disabled | is_loading, "not-allowed", "pointer"),
        font_weight="600",
        width=width,
        min_height=config["min_height"],
        opacity=rx.cond(is_disabled, "0.5", "1"),
        box_shadow=SHADOWS["primary_sm"],
        position="relative",
        overflow="hidden",
        _before={
            "content": "''",
            "position": "absolute",
            "inset": "-2px",
            "background": f"linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_hover']} 100%)",
            "border_radius": "inherit",
            "opacity": "0",
            "z_index": "-1",
            "filter": "blur(12px)",
            "transition": TRANSITIONS["normal"],
        },
        _hover={
            "transform": rx.cond(is_disabled | is_loading, "none", "translateY(-2px)"),
            "box_shadow": rx.cond(is_disabled | is_loading, SHADOWS["primary_sm"], SHADOWS["primary_md"]),
            "_before": {"opacity": "0.4"},
        },
        _active={
            "transform": rx.cond(is_disabled | is_loading, "none", "translateY(0)"),
            "box_shadow": SHADOWS["primary_sm"],
        },
        _focus_visible={
            "box_shadow": SHADOWS["focus"],
        },
        transition=TRANSITIONS["normal"],
        class_name=f"btn-primary btn-ripple {class_name}",
    )


def secondary_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    icon_right: Optional[str] = None,
    is_loading: bool = False,
    is_disabled: bool = False,
    width: str = "auto",
    size: ButtonSize = "md",
) -> rx.Component:
    """Modern secondary button with subtle shadow and hover effect.
    
    Args:
        text: Button text
        on_click: Click handler function
        icon: Optional icon name (left side)
        icon_right: Optional icon name (right side)
        is_loading: Loading state
        is_disabled: Disabled state
        width: Button width
        size: Button size - sm, md, lg
    """
    sizes = {
        "sm": {"padding": "0.5rem 1rem", "font_size": "0.8125rem", "min_height": "36px", "icon_size": 14},
        "md": {"padding": "0.75rem 1.5rem", "font_size": "0.875rem", "min_height": "44px", "icon_size": 16},
        "lg": {"padding": "1rem 2rem", "font_size": "0.9375rem", "min_height": "52px", "icon_size": 18},
    }
    config = sizes.get(size, sizes["md"])
    
    return rx.button(
        rx.hstack(
            rx.cond(
                is_loading,
                rx.spinner(size="1", color=COLORS["primary"]),
                rx.cond(
                    icon,
                    rx.icon(icon, size=config["icon_size"], flex_shrink="0", color=COLORS["primary"]),
                    rx.fragment(),
                ),
            ),
            rx.text(
                text,
                font_size=config["font_size"],
                white_space="nowrap",
            ),
            rx.cond(
                icon_right,
                rx.icon(icon_right, size=config["icon_size"], flex_shrink="0", color=COLORS["text_secondary"]),
                rx.fragment(),
            ),
            spacing="2",
            align="center",
            justify="center",
            width="100%",
        ),
        on_click=rx.cond(is_disabled | is_loading, None, on_click),
        background=COLORS["white"],
        color=COLORS["text_primary"],
        border=f"1px solid {COLORS['border']}",
        border_radius=RADIUS["lg"],
        padding=config["padding"],
        cursor=rx.cond(is_disabled | is_loading, "not-allowed", "pointer"),
        font_weight="500",
        width=width,
        min_height=config["min_height"],
        opacity=rx.cond(is_disabled, "0.5", "1"),
        box_shadow=SHADOWS["xs"],
        _hover={
            "background": COLORS["gray_50"],
            "border_color": COLORS["gray_300"],
            "box_shadow": SHADOWS["sm"],
            "transform": rx.cond(is_disabled | is_loading, "none", "translateY(-1px)"),
        },
        _active={
            "background": COLORS["gray_100"],
            "transform": "translateY(0)",
        },
        _focus_visible={
            "box_shadow": SHADOWS["focus"],
            "border_color": COLORS["primary"],
        },
        transition=TRANSITIONS["normal"],
        class_name="btn-secondary btn-ripple",
    )


def ghost_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    is_disabled: bool = False,
    color: str = "secondary",
) -> rx.Component:
    """Ghost button with no background - just text and hover effect.
    
    Args:
        text: Button text
        on_click: Click handler
        icon: Optional icon
        is_disabled: Disabled state
        color: Text color - "primary", "secondary", "danger"
    """
    color_map = {
        "primary": COLORS["primary"],
        "secondary": COLORS["text_secondary"],
        "danger": COLORS["error"],
    }
    text_color = color_map.get(color, COLORS["text_secondary"])
    
    return rx.button(
        rx.hstack(
            rx.cond(
                icon,
                rx.icon(icon, size=16, color=text_color),
                rx.fragment(),
            ),
            rx.text(text, font_size="0.875rem"),
            spacing="2",
            align="center",
        ),
        on_click=rx.cond(is_disabled, None, on_click),
        background="transparent",
        color=text_color,
        border="none",
        border_radius=RADIUS["md"],
        padding="0.5rem 1rem",
        cursor=rx.cond(is_disabled, "not-allowed", "pointer"),
        font_weight="500",
        opacity=rx.cond(is_disabled, "0.5", "1"),
        min_height="36px",
        _hover={
            "background": COLORS["gray_100"],
            "color": COLORS["text_primary"] if color == "secondary" else text_color,
        },
        _active={
            "background": COLORS["gray_200"],
        },
        transition=TRANSITIONS["fast"],
    )


def danger_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    is_loading: bool = False,
    is_disabled: bool = False,
    width: str = "auto",
) -> rx.Component:
    """Danger/destructive action button.
    
    Args:
        text: Button text
        on_click: Click handler
        icon: Optional icon
        is_loading: Loading state
        is_disabled: Disabled state
        width: Button width
    """
    return rx.button(
        rx.hstack(
            rx.cond(
                is_loading,
                rx.spinner(size="1", color="white"),
                rx.cond(
                    icon,
                    rx.icon(icon, size=16, flex_shrink="0"),
                    rx.fragment(),
                ),
            ),
            rx.text(text, font_size="0.875rem", font_weight="600"),
            spacing="2",
            align="center",
            justify="center",
        ),
        on_click=rx.cond(is_disabled | is_loading, None, on_click),
        background=COLORS["error"],
        color="white",
        border="none",
        border_radius=RADIUS["lg"],
        padding="0.75rem 1.5rem",
        cursor=rx.cond(is_disabled | is_loading, "not-allowed", "pointer"),
        width=width,
        min_height="44px",
        opacity=rx.cond(is_disabled, "0.5", "1"),
        box_shadow="0 2px 8px rgba(220, 38, 38, 0.25)",
        _hover={
            "background": COLORS["error_dark"],
            "box_shadow": "0 4px 14px rgba(220, 38, 38, 0.35)",
            "transform": rx.cond(is_disabled | is_loading, "none", "translateY(-1px)"),
        },
        _active={
            "transform": "translateY(0)",
        },
        _focus_visible={
            "box_shadow": SHADOWS["focus_error"],
        },
        transition=TRANSITIONS["normal"],
    )


def icon_button(
    icon: str,
    on_click: Optional[Callable] = None,
    tooltip: Optional[str] = None,
    color: str = "text_tertiary",
    size: str = "md",
    is_active: bool = False,
    variant: str = "ghost",
) -> rx.Component:
    """Icon-only button with hover effects and optional tooltip.
    
    Args:
        icon: Icon name from lucide-react icon set
        on_click: Click handler function
        tooltip: Optional tooltip text
        color: Icon color key from COLORS
        size: Button size - "sm", "md", "lg"
        is_active: Active/selected state
        variant: Style variant - "ghost" or "filled"
    """
    size_config = {
        "sm": {"padding": "0.375rem", "icon_size": 14, "min_size": "28px"},
        "md": {"padding": "0.5rem", "icon_size": 16, "min_size": "36px"},
        "lg": {"padding": "0.625rem", "icon_size": 20, "min_size": "44px"},
    }
    config = size_config.get(size, size_config["md"])
    icon_color = COLORS.get(color, color)
    
    button = rx.button(
        rx.icon(icon, size=config["icon_size"]),
        on_click=on_click,
        background=rx.cond(is_active, COLORS["primary_muted"], "transparent") if variant == "ghost" else COLORS["gray_100"],
        color=rx.cond(is_active, COLORS["primary"], icon_color),
        border="none",
        border_radius=RADIUS["md"],
        padding=config["padding"],
        cursor="pointer",
        width="auto",
        height="auto",
        min_width=config["min_size"],
        min_height=config["min_size"],
        display="flex",
        align_items="center",
        justify_content="center",
        _hover={
            "background": COLORS["gray_100"],
            "color": COLORS["text_primary"],
            "transform": "scale(1.05)",
        },
        _active={
            "background": COLORS["gray_200"],
            "transform": "scale(0.95)",
        },
        _focus_visible={
            "box_shadow": SHADOWS["focus"],
        },
        transition=TRANSITIONS["fast"],
        class_name="icon-btn",
    )
    
    if tooltip:
        return rx.tooltip(
            button, 
            content=tooltip,
            delay_duration=300,
        )
    return button


def circular_button(
    icon: str,
    on_click: Optional[Callable] = None,
    size: str = "md",
    variant: str = "primary",
    is_disabled: bool = False,
    is_loading: bool = False,
    id: Optional[str] = None,
) -> rx.Component:
    """Modern circular button with gradient - perfect for send/action buttons.
    
    Args:
        icon: Icon name from lucide-react icon set
        on_click: Click handler function
        size: Button size - "sm", "md", "lg"
        variant: Color variant - "primary", "secondary", "ghost"
        is_disabled: Disabled state
        is_loading: Loading state (shows spinner)
        id: Optional HTML id attribute
    """
    size_config = {
        "sm": {"size": "32px", "icon_size": 14},
        "md": {"size": "40px", "icon_size": 18},
        "lg": {"size": "48px", "icon_size": 22},
    }
    config = size_config.get(size, size_config["md"])
    
    variant_styles = {
        "primary": {
            "background": f"linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_hover']} 100%)",
            "color": "white",
            "box_shadow": SHADOWS["primary_sm"],
            "hover_shadow": SHADOWS["primary_md"],
        },
        "secondary": {
            "background": COLORS["white"],
            "color": COLORS["primary"],
            "box_shadow": SHADOWS["sm"],
            "hover_shadow": SHADOWS["md"],
        },
        "ghost": {
            "background": "transparent",
            "color": COLORS["text_secondary"],
            "box_shadow": "none",
            "hover_shadow": SHADOWS["sm"],
        },
    }
    styles = variant_styles.get(variant, variant_styles["primary"])
    
    return rx.button(
        rx.cond(
            is_loading,
            rx.spinner(size="1", color=styles["color"]),
            rx.icon(icon, size=config["icon_size"]),
        ),
        on_click=rx.cond(is_disabled | is_loading, None, on_click),
        id=id,
        background=styles["background"],
        color=styles["color"],
        border="1px solid transparent" if variant != "secondary" else f"1px solid {COLORS['border']}",
        border_radius=RADIUS["full"],
        width=config["size"],
        height=config["size"],
        min_width=config["size"],
        min_height=config["size"],
        padding="0",
        cursor=rx.cond(is_disabled | is_loading, "not-allowed", "pointer"),
        display="flex",
        align_items="center",
        justify_content="center",
        flex_shrink="0",
        opacity=rx.cond(is_disabled, "0.5", "1"),
        box_shadow=styles["box_shadow"],
        _hover={
            "transform": rx.cond(is_disabled | is_loading, "none", "scale(1.08)"),
            "box_shadow": rx.cond(is_disabled | is_loading, styles["box_shadow"], styles["hover_shadow"]),
        },
        _active={
            "transform": rx.cond(is_disabled | is_loading, "none", "scale(0.95)"),
        },
        _focus_visible={
            "box_shadow": SHADOWS["focus"],
        },
        transition=TRANSITIONS["normal"],
    )


def link_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    color: str = "primary",
) -> rx.Component:
    """Text link styled as a button.
    
    Args:
        text: Link text
        on_click: Click handler
        icon: Optional icon
        color: Text color - "primary", "secondary"
    """
    text_color = COLORS["primary"] if color == "primary" else COLORS["text_secondary"]
    
    return rx.box(
        rx.hstack(
            rx.cond(
                icon,
                rx.icon(icon, size=14, color=text_color),
                rx.fragment(),
            ),
            rx.text(
                text,
                font_size="0.875rem",
                font_weight="500",
                color=text_color,
                text_decoration="underline",
                text_decoration_color="transparent",
                text_underline_offset="2px",
            ),
            spacing="1",
            align="center",
        ),
        on_click=on_click,
        cursor="pointer",
        _hover={
            "color": COLORS["primary_hover"] if color == "primary" else COLORS["text_primary"],
            "text_decoration_color": text_color,
        },
        transition=TRANSITIONS["fast"],
    )

