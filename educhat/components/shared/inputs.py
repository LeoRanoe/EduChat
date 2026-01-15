"""Input components for EduChat.

Professional form inputs with:
- Labels and helper text
- Error states with validation messages
- Focus ring animations
- Icon support
- Password visibility toggle
- Proper accessibility attributes
"""

import reflex as rx
from typing import Optional, Callable, Literal
from educhat.styles.theme import COLORS, RADIUS, SHADOWS, TRANSITIONS


InputSize = Literal["sm", "md", "lg"]


def form_field(
    label: str,
    value: str = "",
    placeholder: str = "",
    on_change: Optional[Callable] = None,
    on_blur: Optional[Callable] = None,
    input_type: str = "text",
    error: str = "",
    helper_text: str = "",
    required: bool = False,
    disabled: bool = False,
    icon_left: Optional[str] = None,
    icon_right: Optional[str] = None,
    size: InputSize = "md",
    width: str = "100%",
    id: Optional[str] = None,
) -> rx.Component:
    """Complete form field with label, input, error, and helper text.
    
    Args:
        label: Field label text
        value: Input value
        placeholder: Placeholder text
        on_change: Change handler
        on_blur: Blur handler
        input_type: Input type (text, email, password, etc.)
        error: Error message (shows red state if present)
        helper_text: Helper text below input
        required: Show required indicator
        disabled: Disabled state
        icon_left: Icon on left side of input
        icon_right: Icon on right side of input
        size: Input size
        width: Field width
        id: HTML id attribute
    """
    size_config = {
        "sm": {"padding": "0.5rem 0.75rem", "font_size": "0.8125rem", "min_height": "36px", "icon_padding": "2rem"},
        "md": {"padding": "0.75rem 1rem", "font_size": "0.9375rem", "min_height": "44px", "icon_padding": "2.5rem"},
        "lg": {"padding": "1rem 1.25rem", "font_size": "1rem", "min_height": "52px", "icon_padding": "3rem"},
    }
    config = size_config.get(size, size_config["md"])
    has_error = error != ""
    
    return rx.box(
        # Label
        rx.cond(
            label,
            rx.box(
                rx.text(
                    label,
                    font_size="0.875rem",
                    font_weight="500",
                    color=COLORS["text_primary"],
                ),
                rx.cond(
                    required,
                    rx.text(" *", color=COLORS["error"], font_weight="500"),
                    rx.fragment(),
                ),
                display="flex",
                margin_bottom="0.5rem",
            ),
            rx.fragment(),
        ),
        
        # Input container
        rx.box(
            # Left icon
            rx.cond(
                icon_left,
                rx.box(
                    rx.icon(icon_left, size=18, color=COLORS["text_muted"]),
                    position="absolute",
                    left="12px",
                    top="50%",
                    transform="translateY(-50%)",
                    z_index="1",
                    class_name="input-icon-left",
                ),
                rx.fragment(),
            ),
            
            # Input
            rx.input(
                id=id,
                type=input_type,
                placeholder=placeholder,
                value=value,
                on_change=on_change,
                on_blur=on_blur,
                disabled=disabled,
                background=COLORS["white"],
                border=f"1px solid {COLORS['error'] if has_error else COLORS['border']}",
                border_radius=RADIUS["lg"],
                padding=config["padding"],
                padding_left=config["icon_padding"] if icon_left else config["padding"].split()[1],
                padding_right=config["icon_padding"] if icon_right else config["padding"].split()[1],
                width="100%",
                font_size=config["font_size"],
                min_height=config["min_height"],
                color=COLORS["text_primary"],
                _focus={
                    "outline": "none",
                    "border_color": COLORS["error"] if has_error else COLORS["primary"],
                    "box_shadow": SHADOWS["focus_error"] if has_error else SHADOWS["focus"],
                },
                _placeholder={
                    "color": COLORS["text_muted"],
                },
                _disabled={
                    "background": COLORS["gray_50"],
                    "cursor": "not-allowed",
                    "opacity": "0.6",
                },
                transition=TRANSITIONS["normal"],
                class_name="input-error" if has_error else "",
            ),
            
            # Right icon
            rx.cond(
                icon_right,
                rx.box(
                    rx.icon(icon_right, size=18, color=COLORS["text_muted"]),
                    position="absolute",
                    right="12px",
                    top="50%",
                    transform="translateY(-50%)",
                    z_index="1",
                ),
                rx.fragment(),
            ),
            
            position="relative",
            width="100%",
        ),
        
        # Error message
        rx.cond(
            has_error,
            rx.box(
                rx.icon("alert-circle", size=14, color=COLORS["error"]),
                rx.text(
                    error,
                    font_size="0.75rem",
                    color=COLORS["error"],
                    margin_left="0.25rem",
                ),
                display="flex",
                align_items="center",
                margin_top="0.375rem",
                animation="fadeIn 0.2s ease-out",
            ),
            rx.cond(
                helper_text,
                rx.text(
                    helper_text,
                    font_size="0.75rem",
                    color=COLORS["text_tertiary"],
                    margin_top="0.375rem",
                ),
                rx.fragment(),
            ),
        ),
        
        width=width,
    )


def password_input(
    label: str = "Password",
    value: str = "",
    placeholder: str = "Enter password",
    on_change: Optional[Callable] = None,
    error: str = "",
    show_password: bool = False,
    on_toggle_visibility: Optional[Callable] = None,
    required: bool = False,
    width: str = "100%",
) -> rx.Component:
    """Password input with visibility toggle.
    
    Args:
        label: Field label
        value: Password value
        placeholder: Placeholder text
        on_change: Change handler
        error: Error message
        show_password: Whether password is visible
        on_toggle_visibility: Handler to toggle visibility
        required: Required indicator
        width: Field width
    """
    has_error = error != ""
    
    return rx.box(
        # Label
        rx.box(
            rx.text(
                label,
                font_size="0.875rem",
                font_weight="500",
                color=COLORS["text_primary"],
            ),
            rx.cond(
                required,
                rx.text(" *", color=COLORS["error"]),
                rx.fragment(),
            ),
            display="flex",
            margin_bottom="0.5rem",
        ),
        
        # Input container
        rx.box(
            rx.icon(
                "lock",
                size=18,
                color=COLORS["text_muted"],
                position="absolute",
                left="12px",
                top="50%",
                transform="translateY(-50%)",
                z_index="1",
            ),
            rx.input(
                type=rx.cond(show_password, "text", "password"),
                placeholder=placeholder,
                value=value,
                on_change=on_change,
                background=COLORS["white"],
                border=f"1px solid {COLORS['error'] if has_error else COLORS['border']}",
                border_radius=RADIUS["lg"],
                padding="0.75rem 2.75rem 0.75rem 2.5rem",
                width="100%",
                font_size="0.9375rem",
                min_height="44px",
                color=COLORS["text_primary"],
                _focus={
                    "outline": "none",
                    "border_color": COLORS["error"] if has_error else COLORS["primary"],
                    "box_shadow": SHADOWS["focus_error"] if has_error else SHADOWS["focus"],
                },
                _placeholder={
                    "color": COLORS["text_muted"],
                },
                transition=TRANSITIONS["normal"],
            ),
            # Visibility toggle
            rx.box(
                rx.icon(
                    rx.cond(show_password, "eye-off", "eye"),
                    size=18,
                    color=COLORS["text_muted"],
                ),
                on_click=on_toggle_visibility,
                position="absolute",
                right="12px",
                top="50%",
                transform="translateY(-50%)",
                cursor="pointer",
                padding="0.25rem",
                border_radius=RADIUS["sm"],
                _hover={
                    "background": COLORS["gray_100"],
                },
                transition=TRANSITIONS["fast"],
            ),
            position="relative",
            width="100%",
        ),
        
        # Error message
        rx.cond(
            has_error,
            rx.box(
                rx.icon("alert-circle", size=14, color=COLORS["error"]),
                rx.text(
                    error,
                    font_size="0.75rem",
                    color=COLORS["error"],
                    margin_left="0.25rem",
                ),
                display="flex",
                align_items="center",
                margin_top="0.375rem",
            ),
            rx.fragment(),
        ),
        
        width=width,
    )


def text_input(
    placeholder: str = "",
    value: str = "",
    on_change: Optional[Callable] = None,
    on_blur: Optional[Callable] = None,
    width: str = "100%",
    multiline: bool = False,
    rows: int = 3,
) -> rx.Component:
    """Simple text input component (backward compatible).
    
    Args:
        placeholder: Placeholder text
        value: Input value
        on_change: Change handler function
        on_blur: Blur handler function
        width: Input width
        multiline: Whether to use textarea
        rows: Number of rows for textarea
    """
    common_style = {
        "background": COLORS["white"],
        "border": f"1px solid {COLORS['border']}",
        "border_radius": RADIUS["lg"],
        "padding": "0.75rem 1rem",
        "width": width,
        "font_size": "0.9375rem",
        "line_height": "1.5",
        "min_height": "44px",
        "color": COLORS["text_primary"],
        "_focus": {
            "outline": "none",
            "border_color": COLORS["primary"],
            "box_shadow": SHADOWS["focus"],
        },
        "_placeholder": {
            "color": COLORS["text_muted"],
        },
        "transition": TRANSITIONS["normal"],
    }
    
    if multiline:
        return rx.text_area(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            on_blur=on_blur,
            rows=str(rows),
            resize="vertical",
            **common_style,
        )
    else:
        return rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            on_blur=on_blur,
            **common_style,
        )


def search_input(
    placeholder: str = "Zoeken...",
    value: str = "",
    on_change: Optional[Callable] = None,
    on_submit: Optional[Callable] = None,
    width: str = "100%",
    size: InputSize = "md",
) -> rx.Component:
    """Search input with search icon and optional submit.
    
    Args:
        placeholder: Placeholder text
        value: Input value
        on_change: Change handler function
        on_submit: Submit handler (on enter)
        width: Input width
        size: Input size
    """
    size_config = {
        "sm": {"padding": "0.375rem 0.75rem 0.375rem 2rem", "icon_size": 14, "font_size": "0.8125rem"},
        "md": {"padding": "0.5rem 1rem 0.5rem 2.5rem", "icon_size": 16, "font_size": "0.875rem"},
        "lg": {"padding": "0.75rem 1.25rem 0.75rem 3rem", "icon_size": 18, "font_size": "0.9375rem"},
    }
    config = size_config.get(size, size_config["md"])
    
    return rx.box(
        rx.icon(
            "search",
            size=config["icon_size"],
            color=COLORS["text_muted"],
            position="absolute",
            left="10px",
            top="50%",
            transform="translateY(-50%)",
            z_index="1",
        ),
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            background=COLORS["gray_50"],
            border=f"1px solid {COLORS['border_light']}",
            border_radius=RADIUS["lg"],
            padding=config["padding"],
            width="100%",
            font_size=config["font_size"],
            color=COLORS["text_primary"],
            _focus={
                "outline": "none",
                "background": COLORS["white"],
                "border_color": COLORS["primary"],
                "box_shadow": SHADOWS["focus"],
            },
            _placeholder={
                "color": COLORS["text_muted"],
            },
            transition=TRANSITIONS["normal"],
        ),
        # Clear button (when value exists)
        rx.cond(
            value != "",
            rx.box(
                rx.icon("x", size=14, color=COLORS["text_muted"]),
                on_click=lambda: on_change("") if on_change else None,
                position="absolute",
                right="10px",
                top="50%",
                transform="translateY(-50%)",
                cursor="pointer",
                padding="0.25rem",
                border_radius=RADIUS["sm"],
                _hover={
                    "background": COLORS["gray_200"],
                },
            ),
            rx.fragment(),
        ),
        position="relative",
        width=width,
    )


def textarea_field(
    label: str = "",
    value: str = "",
    placeholder: str = "",
    on_change: Optional[Callable] = None,
    error: str = "",
    helper_text: str = "",
    required: bool = False,
    disabled: bool = False,
    rows: int = 4,
    max_length: Optional[int] = None,
    show_count: bool = False,
    width: str = "100%",
) -> rx.Component:
    """Textarea field with optional character count.
    
    Args:
        label: Field label
        value: Textarea value
        placeholder: Placeholder text
        on_change: Change handler
        error: Error message
        helper_text: Helper text
        required: Required indicator
        disabled: Disabled state
        rows: Number of rows
        max_length: Maximum character length
        show_count: Show character count
        width: Field width
    """
    has_error = error != ""
    char_count = len(value) if value else 0
    
    return rx.box(
        # Label
        rx.cond(
            label,
            rx.box(
                rx.text(
                    label,
                    font_size="0.875rem",
                    font_weight="500",
                    color=COLORS["text_primary"],
                ),
                rx.cond(
                    required,
                    rx.text(" *", color=COLORS["error"]),
                    rx.fragment(),
                ),
                display="flex",
                margin_bottom="0.5rem",
            ),
            rx.fragment(),
        ),
        
        # Textarea
        rx.text_area(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            rows=str(rows),
            disabled=disabled,
            background=COLORS["white"],
            border=f"1px solid {COLORS['error'] if has_error else COLORS['border']}",
            border_radius=RADIUS["lg"],
            padding="0.75rem 1rem",
            width="100%",
            font_size="0.9375rem",
            line_height="1.6",
            color=COLORS["text_primary"],
            resize="vertical",
            min_height="100px",
            _focus={
                "outline": "none",
                "border_color": COLORS["error"] if has_error else COLORS["primary"],
                "box_shadow": SHADOWS["focus_error"] if has_error else SHADOWS["focus"],
            },
            _placeholder={
                "color": COLORS["text_muted"],
            },
            _disabled={
                "background": COLORS["gray_50"],
                "cursor": "not-allowed",
            },
            transition=TRANSITIONS["normal"],
        ),
        
        # Footer: error/helper and character count
        rx.box(
            rx.cond(
                has_error,
                rx.box(
                    rx.icon("alert-circle", size=14, color=COLORS["error"]),
                    rx.text(error, font_size="0.75rem", color=COLORS["error"], margin_left="0.25rem"),
                    display="flex",
                    align_items="center",
                ),
                rx.cond(
                    helper_text,
                    rx.text(helper_text, font_size="0.75rem", color=COLORS["text_tertiary"]),
                    rx.fragment(),
                ),
            ),
            rx.cond(
                show_count,
                rx.text(
                    f"{char_count}" + (f"/{max_length}" if max_length else ""),
                    font_size="0.75rem",
                    color=COLORS["text_muted"],
                ),
                rx.fragment(),
            ),
            display="flex",
            justify_content="space-between",
            align_items="center",
            margin_top="0.375rem",
        ),
        
        width=width,
    )

