"""Follow-up suggestion components for EduChat."""

import reflex as rx
from typing import List, Optional
from educhat.styles.theme import COLORS, RADIUS


def suggestion_chip(
    text: str,
    icon: str = "",
    on_click=None,
) -> rx.Component:
    """Individual suggestion chip button.
    
    Args:
        text: Suggestion text
        icon: Icon (not used in clean design)
        on_click: Click handler
    """
    return rx.button(
        rx.text(
            text,
            font_size="0.85rem",
            color=COLORS["dark_gray"],
        ),
        background=COLORS["white"],
        border=f"1px solid {COLORS['border']}",
        border_radius=RADIUS["full"],
        padding="0.5rem 1rem",
        cursor="pointer",
        _hover={
            "background": "#FAFAFA",
            "border_color": COLORS["primary_green"],
        },
        on_click=on_click,
    )


def follow_up_suggestions(
    suggestions: List[str] = None,
    on_suggestion_click=None,
) -> rx.Component:
    """Display follow-up suggestion chips below AI messages.
    
    Args:
        suggestions: List of follow-up question texts
        on_suggestion_click: Handler for suggestion clicks
    """
    if not suggestions:
        suggestions = []
    
    return rx.cond(
        len(suggestions) > 0,
        rx.box(
            rx.vstack(
                rx.text(
                    "Misschien wil je ook weten:",
                    font_size="0.875rem",
                    color=COLORS["gray"],
                    font_weight="500",
                ),
                rx.wrap(
                    *[
                        suggestion_chip(
                            text=suggestion,
                            on_click=on_suggestion_click(suggestion) if on_suggestion_click else None,
                        )
                        for suggestion in suggestions
                    ],
                    spacing="2",
                    align="start",
                ),
                spacing="2",
                align="start",
            ),
            margin_top="0.75rem",
            padding_left="0.875rem",
            max_width="600px",
        ),
        rx.fragment(),
    )


def generate_contextual_suggestions(
    last_message: str,
    conversation_topic: Optional[str] = None,
) -> List[str]:
    """Generate contextual follow-up questions based on conversation.
    
    Args:
        last_message: The last AI response
        conversation_topic: Detected topic from conversation
    
    Returns:
        List of 2-3 follow-up question suggestions
    """
    # Default suggestions based on common topics
    default_suggestions = [
        "Wat zijn de kosten?",
        "Hoe lang duurt de opleiding?",
        "Welke documenten heb ik nodig?",
    ]
    
    # Keyword-based contextual suggestions
    suggestions = []
    
    message_lower = last_message.lower()
    
    # Enrollment process
    if any(word in message_lower for word in ["inschrijv", "aanmeld", "registr"]):
        suggestions = [
            "Wat zijn de deadlines voor inschrijving?",
            "Welke documenten moet ik meesturen?",
            "Kan ik me online inschrijven?",
        ]
    
    # Admission requirements
    elif any(word in message_lower for word in ["toelating", "vereist", "voorwaarde"]):
        suggestions = [
            "Wat is het minimum gemiddelde?",
            "Zijn er toelatingsexamens?",
            "Welke diploma's worden geaccepteerd?",
        ]
    
    # Documents
    elif any(word in message_lower for word in ["document", "papier", "bewijs"]):
        suggestions = [
            "Waar kan ik deze documenten krijgen?",
            "Moeten documenten gelegaliseerd zijn?",
            "Hoeveel kopieën heb ik nodig?",
        ]
    
    # Costs and financial aid
    elif any(word in message_lower for word in ["kost", "prijs", "betaal", "geld", "beurs"]):
        suggestions = [
            "Zijn er studiebeurzen beschikbaar?",
            "Kan ik in termijnen betalen?",
            "Wat zijn de extra kosten?",
        ]
    
    # Study programs
    elif any(word in message_lower for word in ["opleiding", "studie", "programma", "cursus"]):
        suggestions = [
            "Hoe lang duurt deze opleiding?",
            "Welke vakken krijg ik?",
            "Wat zijn de carrièremogelijkheden?",
        ]
    
    # Deadlines
    elif any(word in message_lower for word in ["deadline", "datum", "wanneer", "periode"]):
        suggestions = [
            "Wat gebeurt er als ik de deadline mis?",
            "Kan ik een verlenging aanvragen?",
            "Wanneer start het nieuwe schooljaar?",
        ]
    
    # MINOV general
    elif any(word in message_lower for word in ["minov", "ministerie", "onderwijs"]):
        suggestions = [
            "Welke opleidingen biedt MINOV aan?",
            "Waar zijn de MINOV kantoren?",
            "Hoe kan ik MINOV bereiken?",
        ]
    
    # Default if no match
    else:
        suggestions = default_suggestions
    
    # Return max 3 suggestions
    return suggestions[:3]


def contextual_follow_ups(
    last_bot_message: str = "",
    on_suggestion_click=None,
) -> rx.Component:
    """Generate and display contextual follow-up suggestions.
    
    Args:
        last_bot_message: The last AI response content
        on_suggestion_click: Handler for suggestion clicks
    """
    suggestions = generate_contextual_suggestions(last_bot_message)
    
    return follow_up_suggestions(
        suggestions=suggestions,
        on_suggestion_click=on_suggestion_click,
    )

