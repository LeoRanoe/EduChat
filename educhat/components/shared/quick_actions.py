"""Quick action buttons for common education queries."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS


def quick_action_button(
    text: str,
    icon: str = "",
    on_click=None,
) -> rx.Component:
    """Modern quick action button with subtle shadow and hover effect.
    
    Args:
        text: Button text/prompt
        icon: Icon (not used in clean design)
        on_click: Click handler
    """
    return rx.button(
        rx.hstack(
            rx.box(
                width="4px",
                height="100%",
                background=f"linear-gradient(180deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                border_radius="2px",
                opacity="0",
                transition="opacity 0.2s ease",
                class_name="action-indicator",
            ),
            rx.text(
                text,
                font_size=["0.875rem", "0.875rem", "0.9375rem"],
                font_weight="500",
                color=COLORS["dark_gray"],
                line_height="1.5",
                text_align="left",
                white_space="normal",
                word_wrap="break-word",
                overflow="hidden",
                flex="1",
            ),
            rx.icon(
                "arrow-right",
                size=16,
                color=COLORS["text_tertiary"],
                opacity="0",
                class_name="action-arrow",
                transition="all 0.2s ease",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        on_click=on_click,
        background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_gray']}50 100%)",
        border=f"1.5px solid {COLORS['border_gray']}",
        border_radius=RADIUS["xl"],
        padding=["0.875rem 1.125rem", "0.875rem 1.125rem", "1rem 1.25rem"],
        cursor="pointer",
        box_shadow="0 2px 8px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.02)",
        position="relative",
        overflow="hidden",
        _hover={
            "border_color": COLORS["primary_green"],
            "background": f"linear-gradient(135deg, {COLORS['light_green']}40 0%, {COLORS['white']} 100%)",
            "transform": "translateY(-2px) scale(1.01)",
            "box_shadow": "0 8px 24px rgba(16, 163, 127, 0.15), 0 4px 8px rgba(0,0,0,0.08)",
            ".action-indicator": {"opacity": "1"},
            ".action-arrow": {"opacity": "1", "transform": "translateX(4px)"},
        },
        _active={
            "transform": "translateY(0) scale(0.99)",
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        width="100%",
        text_align="left",
        min_height=["50px", "50px", "54px"],
        height="auto",
        display="flex",
        align_items="center",
    )


def quick_actions_grid(on_action_click) -> rx.Component:
    """Grid of quick action buttons.
    
    Args:
        on_action_click: Function that takes prompt text as argument
    """
    actions = [
        "Vertel me over MINOV",
        "Welke opleidingen zijn er?",
        "Hoe schrijf ik me in?",
        "Wat zijn de deadlines?",
        "Welke documenten heb ik nodig?",
        "Wat zijn de toelatingseisen?",
    ]
    
    # Create buttons with proper event handlers
    buttons = []
    for action_text in actions:
        button = quick_action_button(
            text=action_text,
            on_click=on_action_click(action_text),
        )
        buttons.append(button)
    
    return rx.vstack(
        rx.text(
            "Populaire vragen:",
            font_size=["0.875rem", "0.9375rem", "1rem"],
            font_weight="600",
            color=COLORS["text_primary"],
            margin_bottom="0.75rem",
            text_align="left",
            width="100%",
        ),
        rx.box(
            *buttons,
            display="grid",
            grid_template_columns=["1fr", "1fr", "repeat(2, 1fr)"],
            gap="0.75rem",
            width="100%",
        ),
        spacing="2",
        width="100%",
        align_items="start",
    )


def conversation_template_button(
    title: str,
    description: str,
    icon: str,
    on_click=None,
) -> rx.Component:
    """Button for conversation templates.
    
    Args:
        title: Template title
        description: Template description
        icon: Icon (not used in clean design)
        on_click: Click handler
    """
    return rx.button(
        rx.hstack(
            # Icon circle
            rx.box(
                rx.icon(
                    "sparkles",
                    size=18,
                    color=COLORS["primary_green"],
                ),
                background=f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['light_green']}80 100%)",
                border_radius="12px",
                padding="0.75rem",
                flex_shrink="0",
                box_shadow="0 2px 8px rgba(16, 163, 127, 0.15)",
            ),
            # Text content
            rx.vstack(
                rx.text(
                    title,
                    font_size=["0.875rem", "0.875rem", "0.9375rem"],
                    font_weight="600",
                    color=COLORS["text_primary"],
                    white_space="normal",
                    word_wrap="break-word",
                ),
                rx.text(
                    description,
                    font_size=["0.75rem", "0.75rem", "0.8125rem"],
                    color=COLORS["text_secondary"],
                    line_height="1.5",
                    white_space="normal",
                    word_wrap="break-word",
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            # Arrow indicator
            rx.icon(
                "chevron-right",
                size=18,
                color=COLORS["text_tertiary"],
                flex_shrink="0",
                class_name="template-arrow",
                transition="transform 0.2s ease",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        on_click=on_click,
        background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_gray']}30 100%)",
        border=f"1.5px solid {COLORS['border_gray']}",
        border_radius=RADIUS["lg"],
        padding=["1rem", "1rem", "1.125rem"],
        cursor="pointer",
        box_shadow="0 2px 8px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.02)",
        _hover={
            "border_color": COLORS["primary_green"],
            "background": f"linear-gradient(135deg, {COLORS['light_green']}20 0%, {COLORS['white']} 100%)",
            "transform": "translateY(-2px)",
            "box_shadow": "0 8px 24px rgba(16, 163, 127, 0.12), 0 4px 8px rgba(0,0,0,0.06)",
            ".template-arrow": {"transform": "translateX(4px)"},
        },
        _active={
            "transform": "translateY(0)",
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        width="100%",
        text_align="left",
        min_height=["70px", "70px", "auto"],
        height="auto",
    )


def conversation_templates(on_template_click) -> rx.Component:
    """Display conversation template options.
    
    Args:
        on_template_click: Function that takes template text as argument
    """
    templates = [
        {
            "title": "Inschrijvingsproces",
            "description": "Leer stap voor stap hoe je je inschrijft voor een opleiding",
            "prompt": "Hoe schrijf ik me in voor een opleiding? Kun je me stap voor stap door het proces leiden?",
        },
        {
            "title": "Benodigde documenten",
            "description": "Ontdek welke documenten je nodig hebt voor je inschrijving",
            "prompt": "Welke documenten heb ik nodig om me in te schrijven? Kun je een volledige lijst geven?",
        },
        {
            "title": "Toelatingseisen",
            "description": "Bekijk de vereisten en voorwaarden voor toelating",
            "prompt": "Wat zijn de toelatingseisen voor studies in Suriname? Welke voorwaarden moet ik vervullen?",
        },
    ]
    
    # Create buttons with proper event handlers
    buttons = []
    for template in templates:
        prompt_text = template["prompt"]
        button = conversation_template_button(
            title=template["title"],
            description=template["description"],
            icon="",
            on_click=on_template_click(prompt_text),
        )
        buttons.append(button)
    
    return rx.vstack(
        *buttons,
        spacing="3",
        width="100%",
        align_items="stretch",
    )

