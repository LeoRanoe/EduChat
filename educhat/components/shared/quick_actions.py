"""Quick action buttons for common education queries."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS


def quick_action_button(
    text: str,
    icon: str = "💬",
    on_click=None,
) -> rx.Component:
    """Quick action button for common prompts.
    
    Args:
        text: Button text/prompt
        icon: Emoji icon
        on_click: Click handler
    """
    return rx.button(
        rx.hstack(
            rx.text(
                icon,
                font_size="1.25rem",
            ),
            rx.text(
                text,
                font_size="0.875rem",
                font_weight="500",
            ),
            spacing="2",
            align="center",
        ),
        on_click=on_click,
        background="white",
        border=f"1.5px solid {COLORS['border_gray']}",
        border_radius=RADIUS["lg"],
        padding="0.75rem 1rem",
        cursor="pointer",
        _hover={
            "border_color": COLORS["primary_green"],
            "background": "#F0F9F0",
        },
        transition="all 0.2s ease",
        width="100%",
        text_align="left",
    )


def quick_actions_grid(on_action_click) -> rx.Component:
    """Grid of quick action buttons.
    
    Args:
        on_action_click: Function that takes prompt text as argument
    """
    actions = [
        {"text": "Vertel me over MINOV", "icon": "🏫"},
        {"text": "Welke opleidingen zijn er?", "icon": "📚"},
        {"text": "Hoe schrijf ik me in?", "icon": "✍️"},
        {"text": "Wat zijn de deadlines?", "icon": "📅"},
        {"text": "Welke documenten heb ik nodig?", "icon": "📄"},
        {"text": "Wat zijn de toelatingseisen?", "icon": "📋"},
    ]
    
    return rx.box(
        rx.vstack(
            rx.text(
                "Populaire vragen:",
                font_size="0.875rem",
                font_weight="600",
                color=COLORS["dark_gray"],
                margin_bottom="0.5rem",
            ),
            rx.box(
                *[
                    quick_action_button(
                        text=action["text"],
                        icon=action["icon"],
                        on_click=lambda t=action["text"]: on_action_click(t),
                    )
                    for action in actions
                ],
                display="grid",
                grid_template_columns=["1fr", "1fr", "repeat(2, 1fr)"],  # 1 col mobile, 2 cols desktop
                gap="0.75rem",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        padding="1rem",
        width="100%",
        max_width="800px",
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
        icon: Emoji icon
        on_click: Click handler
    """
    return rx.button(
        rx.vstack(
            rx.hstack(
                rx.text(
                    icon,
                    font_size="1.5rem",
                ),
                rx.text(
                    title,
                    font_size="1rem",
                    font_weight="600",
                    color=COLORS["dark_gray"],
                ),
                spacing="2",
                align="center",
                width="100%",
            ),
            rx.text(
                description,
                font_size="0.875rem",
                color=COLORS["gray"],
                line_height="1.4",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        on_click=on_click,
        background="white",
        border=f"1.5px solid {COLORS['border_gray']}",
        border_radius=RADIUS["lg"],
        padding="1rem",
        cursor="pointer",
        _hover={
            "border_color": COLORS["primary_green"],
            "box_shadow": f"0 2px 8px rgba(34, 139, 34, 0.1)",
        },
        transition="all 0.2s ease",
        width="100%",
        text_align="left",
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
            "icon": "✍️",
            "prompt": "Hoe schrijf ik me in voor een opleiding? Kun je me stap voor stap door het proces leiden?",
        },
        {
            "title": "Benodigde documenten",
            "description": "Ontdek welke documenten je nodig hebt voor je inschrijving",
            "icon": "📄",
            "prompt": "Welke documenten heb ik nodig om me in te schrijven? Kun je een volledige lijst geven?",
        },
        {
            "title": "Toelatingseisen",
            "description": "Bekijk de vereisten en voorwaarden voor toelating",
            "icon": "📋",
            "prompt": "Wat zijn de toelatingseisen voor studies in Suriname? Welke voorwaarden moet ik vervullen?",
        },
    ]
    
    return rx.vstack(
        rx.text(
            "Start een gesprek:",
            font_size="0.875rem",
            font_weight="600",
            color=COLORS["dark_gray"],
        ),
        *[
            conversation_template_button(
                title=template["title"],
                description=template["description"],
                icon=template["icon"],
                on_click=lambda p=template["prompt"]: on_template_click(p),
            )
            for template in templates
        ],
        spacing="3",
        width="100%",
        max_width="800px",
    )
