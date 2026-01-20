"""Quiz question components for onboarding."""
import reflex as rx
from educhat.styles.theme import COLORS, FONTS, SPACING, RADIUS
from typing import List, Callable


def multi_select_button(
    label: str,
    is_selected: rx.Var[bool],
    on_click: Callable
) -> rx.Component:
    """
    Single button for multi-select groups.
    
    Args:
        label: Button text
        is_selected: Whether the button is currently selected
        on_click: Click handler function
    """
    return rx.button(
        label,
        on_click=on_click,
        background=rx.cond(is_selected, COLORS["primary_green"], "white"),
        color=rx.cond(is_selected, "white", COLORS["text_primary"]),
        border=rx.cond(
            is_selected,
            f"2px solid {COLORS['primary_green']}",
            f"1px solid {COLORS['border']}"
        ),
        border_radius="10px",
        padding="10px 18px",
        font_size="0.875rem",
        font_weight="500",
        cursor="pointer",
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
        min_height="44px",
        _hover={
            "border_color": COLORS["primary_green"],
            "background": rx.cond(is_selected, COLORS["primary_hover"], COLORS["primary_light"]),
        },
        _focus_visible={
            "outline": f"2px solid {COLORS['primary_green']}",
            "outline_offset": "2px",
        },
    )


def multi_select_group(
    options: List[str],
    selected_values: rx.Var[List[str]],
    on_toggle: Callable
) -> rx.Component:
    """
    Group of multi-select buttons.
    
    Args:
        options: List of option labels
        selected_values: List of currently selected values
        on_toggle: Function to call when an option is toggled
    """
    return rx.box(
        rx.foreach(
            options,
            lambda option: multi_select_button(
                label=option,
                is_selected=selected_values.contains(option),
                on_click=lambda: on_toggle(option),
            )
        ),
        display="flex",
        flex_wrap="wrap",
        gap="10px",
        margin_top="0.75rem",
    )


def checkbox_item(
    label: str,
    is_checked: rx.Var[bool],
    on_change: Callable
) -> rx.Component:
    """
    Single checkbox with label.
    
    Args:
        label: Checkbox label text
        is_checked: Whether checkbox is checked
        on_change: Change handler function
    """
    return rx.hstack(
        rx.checkbox(
            checked=is_checked,
            on_change=on_change,
            color_scheme="green",
            size="2",
        ),
        rx.text(
            label,
            font_size="0.9375rem",
            color=COLORS["text_primary"],
            cursor="pointer",
            on_click=on_change,
            line_height="1.4",
        ),
        spacing="3",
        align="center",
        padding="10px 12px",
        margin_left="-12px",
        border_radius="8px",
        cursor="pointer",
        transition="background 0.15s ease",
        min_height="44px",
        _hover={
            "background": COLORS["gray_100"],
        },
    )


def checkbox_list(
    options: List[str],
    selected_values: rx.Var[List[str]],
    on_toggle: Callable
) -> rx.Component:
    """
    List of checkboxes.
    
    Args:
        options: List of checkbox labels
        selected_values: List of selected values
        on_toggle: Toggle handler function
    """
    return rx.vstack(
        rx.foreach(
            options,
            lambda option: checkbox_item(
                label=option,
                is_checked=selected_values.contains(option),
                on_change=lambda: on_toggle(option),
            )
        ),
        spacing="1",
        align="stretch",
        width="100%",
        margin_top="0.5rem",
    )


def radio_button(
    label: str,
    value: str,
    selected_value: rx.Var[str],
    on_change: Callable
) -> rx.Component:
    """
    Single radio button with label.
    
    Args:
        label: Radio button label
        value: Value when selected
        selected_value: Currently selected value
        on_change: Change handler
    """
    return rx.hstack(
        rx.box(
            rx.cond(
                selected_value == value,
                rx.box(
                    width="10px",
                    height="10px",
                    border_radius="50%",
                    background=COLORS["primary_green"],
                ),
                rx.box(),
            ),
            width="20px",
            height="20px",
            border_radius="50%",
            border=rx.cond(
                selected_value == value,
                f"2px solid {COLORS['primary_green']}",
                f"2px solid {COLORS['gray_300']}"
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            cursor="pointer",
            transition="all 0.15s ease",
            on_click=lambda: on_change(value),
            flex_shrink="0",
        ),
        rx.text(
            label,
            font_size="0.9375rem",
            color=COLORS["text_primary"],
            cursor="pointer",
            on_click=lambda: on_change(value),
            line_height="1.4",
        ),
        spacing="3",
        align="center",
        padding="10px 12px",
        margin_left="-12px",
        border_radius="8px",
        cursor="pointer",
        transition="background 0.15s ease",
        min_height="44px",
        _hover={
            "background": COLORS["gray_100"],
        },
    )


def radio_group(
    options: List[str],
    selected_value: rx.Var[str],
    on_change: Callable
) -> rx.Component:
    """
    Group of radio buttons.
    
    Args:
        options: List of option labels
        selected_value: Currently selected value
        on_change: Change handler
    """
    return rx.vstack(
        rx.foreach(
            options,
            lambda option: radio_button(
                label=option,
                value=option,
                selected_value=selected_value,
                on_change=on_change,
            )
        ),
        spacing="1",
        align="stretch",
        width="100%",
        margin_top="0.5rem",
    )


def text_area_input(
    value: rx.Var[str],
    on_change: Callable,
    placeholder: str = "Type hier...",
    max_chars: int = 500
) -> rx.Component:
    """
    Multi-line text input with character counter.
    
    Args:
        value: Current text value
        on_change: Change handler
        placeholder: Placeholder text
        max_chars: Maximum character limit
    """
    return rx.vstack(
        rx.text_area(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            width="100%",
            min_height="120px",
            padding="14px 16px",
            font_size="0.9375rem",
            border=f"1px solid {COLORS['border']}",
            border_radius="12px",
            resize="vertical",
            background="white",
            transition="border-color 0.2s ease, box-shadow 0.2s ease",
            _focus={
                "border_color": COLORS["primary_green"],
                "outline": "none",
                "box_shadow": f"0 0 0 3px {COLORS['primary_light']}",
            },
            _placeholder={
                "color": COLORS["text_muted"],
            },
        ),
        rx.text(
            rx.cond(
                value,
                f"{value.length()} / {max_chars}",
                f"0 / {max_chars}"
            ),
            font_size="0.75rem",
            color=COLORS["text_secondary"],
            align_self="end",
        ),
        spacing="2",
        width="100%",
        margin_top="0.75rem",
    )


def dropdown_select(
    options: List[str],
    value: rx.Var[str],
    on_change: Callable,
    placeholder: str = "Selecteer..."
) -> rx.Component:
    """
    Dropdown select component.
    
    Args:
        options: List of dropdown options
        value: Currently selected value
        on_change: Change handler
        placeholder: Placeholder text
    """
    return rx.select(
        options,
        value=value,
        on_change=on_change,
        placeholder=placeholder,
        width="100%",
        max_width="340px",
        font_size="0.9375rem",
        margin_top="0.75rem",
    )

