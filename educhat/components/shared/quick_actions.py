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
        rx.text(
            text,
            font_size=["0.875rem", "0.875rem", "0.9375rem"],
            font_weight="450",
            color=COLORS["dark_gray"],
            line_height="1.5",
            text_align="left",
        ),
        on_click=on_click,
        background="white",
        border=f"1.5px solid {COLORS['border_gray']}",
        border_radius=RADIUS["xl"],
        padding=["0.875rem 1.125rem", "0.875rem 1.125rem", "1rem 1.25rem"],
        cursor="pointer",
        box_shadow="0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02)",
        _hover={
            "border_color": COLORS["primary_green"],
            "background": "linear-gradient(135deg, #FAFAFA 0%, #F9FAFB 100%)",
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 12px rgba(34, 139, 34, 0.12), 0 2px 4px rgba(0,0,0,0.06)",
        },
        _active={
            "transform": "translateY(0)",
        },
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
        width="100%",
        text_align="left",
        min_height=["50px", "50px", "54px"],
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
            on_click=lambda text=action_text: on_action_click(text),
        )
        buttons.append(button)
    
    return rx.box(
        rx.vstack(
            rx.text(
                "Populaire vragen:",
                font_size="0.875rem",
                font_weight="500",
                color=COLORS["dark_gray"],
                margin_bottom="0.75rem",
            ),
            rx.box(
                *buttons,
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
        icon: Icon (not used in clean design)
        on_click: Click handler
    """
    return rx.button(
        rx.vstack(
            rx.text(
                title,
                font_size=["0.875rem", "0.875rem", "0.9375rem"],
                font_weight="600",
                color=COLORS["dark_gray"],
            ),
            rx.text(
                description,
                font_size=["0.75rem", "0.75rem", "0.8125rem"],
                color=COLORS["gray"],
                line_height="1.5",
            ),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        on_click=on_click,
        background="white",
        border=f"1px solid {COLORS['border_gray']}",
        border_radius=RADIUS["lg"],
        padding=["0.875rem", "0.875rem", "1rem"],
        cursor="pointer",
        _hover={
            "border_color": COLORS["primary_green"],
            "background": "#FAFAFA",
            "transform": "translateY(-1px)",
            "box_shadow": "0 2px 4px rgba(0,0,0,0.05)",
        },
        transition="all 0.2s ease",
        width="100%",
        text_align="left",
        min_height=["60px", "60px", "auto"],  # Adequate touch target
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
            on_click=lambda p=prompt_text: on_template_click(p),
        )
        buttons.append(button)
    
    return rx.vstack(
        rx.text(
            "Start een gesprek:",
            font_size="0.875rem",
            font_weight="500",
            color=COLORS["dark_gray"],
        ),
        *buttons,
        spacing="3",
        width="100%",
        max_width="800px",
    )
