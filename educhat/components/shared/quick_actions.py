"""Quick action buttons for common education queries."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, T, SHADOWS
from educhat.state.auth_state import AuthState
from educhat.utils.translations import t


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
            # Animated indicator bar
            rx.box(
                width="3px",
                height="20px",
                background=f"linear-gradient(180deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                border_radius="3px",
                opacity="0",
                transition="all 0.3s ease",
                class_name="action-indicator",
                box_shadow=f"0 0 8px {COLORS['primary_green']}",
            ),
            
            # Icon circle
            rx.box(
                rx.icon(
                    "sparkles",
                    size=14,
                    color=COLORS["primary_green"],
                ),
                width="24px",
                height="24px",
                display="flex",
                align_items="center",
                justify_content="center",
                background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(13, 138, 107, 0.15) 100%)",
                border_radius="6px",
                transition="all 0.3s ease",
                class_name="action-icon",
            ),
            
            # Text content
            rx.text(
                text,
                font_size=["0.8125rem", "0.8125rem", "0.875rem"],
                font_weight="600",
                color=rx.cond(rx.color_mode == "dark", "#FFFFFF", "#111827"),
                line_height="1.4",
                text_align="left",
                white_space="normal",
                overflow_wrap="break-word",
                min_width="0",
                width="100%",
                flex="1",
            ),
            
            # Arrow icon
            rx.icon(
                "arrow-right",
                size=16,
                color=COLORS["primary_green"],
                opacity="0",
                class_name="action-arrow",
                transition="all 0.3s ease",
            ),
            
            spacing="2",
            align="center",
            width="100%",
            min_width="0",
        ),
        on_click=on_click,
        background=T.bg_card,
        border=f"2px solid {T.border}",
        border_radius=RADIUS["xl"],
        padding=["0.5rem 0.75rem", "0.5rem 0.75rem", "0.625rem 0.875rem"],
        cursor="pointer",
        box_shadow=SHADOWS["sm"],
        position="relative",
        overflow="hidden",
        _hover={
            "border_color": COLORS["primary_green"],
            "background": T.bg_hover,
            "transform": "translateY(-3px) scale(1.01)",
            "box_shadow": SHADOWS["primary_md"],
            ".action-indicator": {"opacity": "1"},
            ".action-icon": {
                "background": T.gradient_primary,
                "transform": "scale(1.1) rotate(-5deg)",
                "box_shadow": SHADOWS["primary_lg"],
            },
            ".action-arrow": {"opacity": "1", "transform": "translateX(6px)"},
        },
        _active={
            "transform": "translateY(-1px) scale(0.98)",
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        width="100%",
        text_align="left",
        min_height=["44px", "44px", "48px"],
        height="auto",
        display="flex",
        align_items="center",
    )


def quick_actions_grid(on_action_click) -> rx.Component:
    """Grid of quick action buttons.
    
    Args:
        on_action_click: Function that takes prompt text as argument
    """
    # Language-aware action buttons
    actions_nl = [
        "Vertel me over MINOV",
        "Welke opleidingen zijn er?",
        "Hoe schrijf ik me in?",
        "Wat zijn de deadlines?",
        "Welke documenten heb ik nodig?",
        "Wat zijn de toelatingseisen?",
    ]
    
    actions_en = [
        "Tell me about MINOV",
        "What programs are available?",
        "How do I enroll?",
        "What are the deadlines?",
        "What documents do I need?",
        "What are the admission requirements?",
    ]
    
    # Use rx.cond to switch between languages
    def create_action_button(nl_text: str, en_text: str):
        return quick_action_button(
            text=rx.cond(AuthState.is_dutch, nl_text, en_text),
            on_click=on_action_click(rx.cond(AuthState.is_dutch, nl_text, en_text)),
        )
    
    # Create buttons with proper event handlers
    buttons = [
        create_action_button(nl, en) 
        for nl, en in zip(actions_nl, actions_en)
    ]
    
    return rx.vstack(
        rx.text(
            t("popular_questions"),
            font_size=["0.8125rem", "0.875rem", "0.9375rem"],
            font_weight="600",
            color=T.text_primary,
            margin_bottom="0.375rem",
            text_align="left",
            width="100%",
        ),
        rx.box(
            *buttons,
            display="grid",
            grid_template_columns=["1fr", "1fr", "repeat(2, 1fr)"],
            gap="0.375rem",
            width="100%",
        ),
        spacing="1",
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
                box_shadow=SHADOWS["primary_sm"],
            ),
            # Text content
            rx.vstack(
                rx.text(
                    title,
                    font_size=["0.875rem", "0.875rem", "0.9375rem"],
                    font_weight="600",
                    color=rx.cond(rx.color_mode == "dark", "#FFFFFF", "#111827"),
                    white_space="normal",
                    overflow_wrap="break-word",
                    width="100%",
                    min_width="0",
                ),
                rx.text(
                    description,
                    font_size=["0.75rem", "0.75rem", "0.8125rem"],
                    color=rx.cond(rx.color_mode == "dark", "#FFFFFF", "#4B5563"),
                    line_height="1.5",
                    white_space="normal",
                    overflow_wrap="break-word",
                    width="100%",
                    min_width="0",
                ),
                spacing="1",
                align_items="start",
                flex="1",
                width="100%",
                min_width="0",
            ),
            # Arrow indicator
            rx.icon(
                "chevron-right",
                size=18,
                color=T.text_tertiary,
                flex_shrink="0",
                class_name="template-arrow",
                transition="transform 0.2s ease",
            ),
            spacing="3",
            align="center",
            width="100%",
            min_width="0",
        ),
        on_click=on_click,
        background=T.bg_card,
        border=f"1.5px solid {T.border}",
        border_radius=RADIUS["lg"],
        padding=["1rem", "1rem", "1.125rem"],
        cursor="pointer",
        box_shadow=SHADOWS["xs"],
        _hover={
            "border_color": COLORS["primary_green"],
            "background": T.bg_hover,
            "transform": "translateY(-2px)",
            "box_shadow": SHADOWS["md"],
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
    templates_nl = [
        {
            "title": t("enrollment_process_title", "nl"),
            "description": t("enrollment_process_desc", "nl"),
            "prompt": t("enrollment_process_prompt", "nl"),
        },
        {
            "title": t("required_documents_title", "nl"),
            "description": t("required_documents_desc", "nl"),
            "prompt": t("required_documents_prompt", "nl"),
        },
        {
            "title": t("admission_requirements_title", "nl"),
            "description": t("admission_requirements_desc", "nl"),
            "prompt": t("admission_requirements_prompt", "nl"),
        },
    ]
    
    templates_en = [
        {
            "title": t("enrollment_process_title", "en"),
            "description": t("enrollment_process_desc", "en"),
            "prompt": t("enrollment_process_prompt", "en"),
        },
        {
            "title": t("required_documents_title", "en"),
            "description": t("required_documents_desc", "en"),
            "prompt": t("required_documents_prompt", "en"),
        },
        {
            "title": t("admission_requirements_title", "en"),
            "description": t("admission_requirements_desc", "en"),
            "prompt": t("admission_requirements_prompt", "en"),
        },
    ]
    
    # Helper function to create a single template button with conditional content
    def create_template_button(idx: int) -> rx.Component:
        nl_template = templates_nl[idx]
        en_template = templates_en[idx]
        
        return conversation_template_button(
            title=rx.cond(AuthState.is_dutch, nl_template["title"], en_template["title"]),
            description=rx.cond(AuthState.is_dutch, nl_template["description"], en_template["description"]),
            icon="",
            on_click=on_template_click(
                rx.cond(AuthState.is_dutch, nl_template["prompt"], en_template["prompt"])
            ),
        )
    
    # Create buttons for all templates
    buttons = [create_template_button(i) for i in range(len(templates_nl))]
    
    return rx.vstack(
        *buttons,
        spacing="3",
        width="100%",
        align_items="stretch",
    )

