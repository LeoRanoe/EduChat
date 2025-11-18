"""Onboarding page with quiz interface."""
import reflex as rx
from educhat.state.onboarding_state import OnboardingState
from educhat.components.shared.logo import logo
from educhat.components.shared.progress_bar import progress_bar
from educhat.components.shared.quiz_components import (
    multi_select_group,
    checkbox_list,
    radio_group,
    text_area_input,
    dropdown_select,
)
from educhat.components.shared.buttons import primary_button, secondary_button
from educhat.styles.theme import COLORS, FONTS


def navigation_buttons(state: OnboardingState) -> rx.Component:
    """
    Navigation buttons for quiz (Back, Skip, Next) - Compact.
    
    Args:
        state: Onboarding state instance
    """
    return rx.hstack(
        # Back button (only show if not on first step)
        rx.cond(
            state.current_step > 0,
            rx.button(
                rx.hstack(
                    rx.icon("arrow-left", size=16),
                    rx.text("Terug", font_size="14px", font_weight="600"),
                    spacing="2",
                    align="center",
                ),
                on_click=state.previous_step,
                background="white",
                color=COLORS["primary_green"],
                border=f"2px solid {COLORS['primary_green']}",
                border_radius="10px",
                padding="10px 20px",
                font_size="14px",
                cursor="pointer",
                transition="all 0.3s ease",
                box_shadow="0 2px 8px rgba(0, 0, 0, 0.06)",
                _hover={
                    "background": f"rgba(16, 163, 127, 0.08)",
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 4px 16px rgba(16, 163, 127, 0.15)",
                },
            ),
            rx.box(),
        ),
        rx.spacer(),
        # Skip button (only show if not on last step)
        rx.cond(
            state.current_step < state.total_steps - 1,
            rx.button(
                rx.hstack(
                    rx.text("Overslaan", font_size="14px", font_weight="600"),
                    rx.icon("arrow-right", size=16),
                    spacing="2",
                    align="center",
                ),
                on_click=state.skip_step,
                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                color="white",
                border="none",
                border_radius="10px",
                padding="10px 24px",
                font_size="14px",
                font_weight="600",
                cursor="pointer",
                transition="all 0.3s ease",
                box_shadow=f"0 4px 16px rgba(16, 163, 127, 0.3)",
                _hover={
                    "transform": "translateY(-2px) scale(1.02)",
                    "box_shadow": f"0 6px 24px rgba(16, 163, 127, 0.4)",
                },
            ),
            # Complete button on last step
            rx.button(
                rx.hstack(
                    rx.icon("check-circle", size=18),
                    rx.text("Voltooi", font_size="15px", font_weight="700"),
                    spacing="2",
                    align="center",
                ),
                on_click=state.complete_quiz,
                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                color="white",
                border="none",
                border_radius="10px",
                padding="12px 28px",
                font_size="15px",
                font_weight="700",
                cursor="pointer",
                transition="all 0.3s ease",
                box_shadow=f"0 6px 20px rgba(16, 163, 127, 0.35)",
                _hover={
                    "transform": "translateY(-3px) scale(1.03)",
                    "box_shadow": f"0 8px 28px rgba(16, 163, 127, 0.45)",
                },
            ),
        ),
        spacing="3",
        width="100%",
        margin_top="0",
    )


def question_step_0(state: OnboardingState) -> rx.Component:
    """Question: Welk opleiding volgt je?"""
    options = ["Consectetur", "Lorem", "Ipsum", "Dolor", "Adipiscing", "Dolor", "Sit", "Consectetur", "Consectetur"]
    
    return rx.vstack(
        rx.text(
            "Welk opleiding volgt je?",
            font_size="16px",
            font_weight="500",
            color=COLORS["text_primary"],
            margin_bottom="8px",
        ),
        multi_select_group(
            options=options,
            selected_values=state.education,
            on_toggle=state.toggle_education,
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def question_step_1(state: OnboardingState) -> rx.Component:
    """Question: Wat is jouw leeftijd?"""
    age_options = ["18+", "Under 18", "25+", "30+", "40+"]
    
    return rx.vstack(
        rx.text(
            "Wat is jouw leeftijd?",
            font_size="16px",
            font_weight="500",
            color=COLORS["text_primary"],
            margin_bottom="8px",
        ),
        dropdown_select(
            options=age_options,
            value=state.age,
            on_change=state.set_age,
            placeholder="Selecteer leeftijd...",
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def question_step_2(state: OnboardingState) -> rx.Component:
    """Question: In welk district woon je?"""
    district_options = ["Paramaribo", "Wanica", "Nickerie", "Commewijne", "Saramacca", "Para", "Brokopondo", "Sipaliwini", "Coronie", "Marowijne"]
    
    return rx.vstack(
        rx.text(
            "In welk district woon je?",
            font_size="16px",
            font_weight="500",
            color=COLORS["text_primary"],
            margin_bottom="8px",
        ),
        dropdown_select(
            options=district_options,
            value=state.district,
            on_change=state.set_district,
            placeholder="Selecteer district...",
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def question_step_3(state: OnboardingState) -> rx.Component:
    """Question: Wat is je favoriete vak?"""
    subject_options = ["Consectetur", "Lorem", "Ipsum", "Dolor", "Adipiscing", "Dolor", "Sit", "Consectetur"]
    
    return rx.vstack(
        rx.text(
            "Wat is je favoriete vak?",
            font_size="16px",
            font_weight="500",
            color=COLORS["text_primary"],
            margin_bottom="8px",
        ),
        multi_select_group(
            options=subject_options,
            selected_values=state.favorite_subjects,
            on_toggle=state.toggle_subject,
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def question_step_4(state: OnboardingState) -> rx.Component:
    """Question: Heb je plannen om verder te studeren na deze opleiding?"""
    options = ["Ja", "Nee", "Weet nog niet"]
    
    return rx.vstack(
        rx.text(
            "Heb je plannen om verder te studeren na deze opleiding?",
            font_size="16px",
            font_weight="500",
            color=COLORS["text_primary"],
            margin_bottom="8px",
        ),
        radio_group(
            options=options,
            selected_value=state.future_plans,
            on_change=state.set_future_plans,
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def question_step_5(state: OnboardingState) -> rx.Component:
    """Question: Wat wil je verbeteren met EduChat?"""
    options = [
        "Betere cijfers halen",
        "Studiekeuze maken",
        "Informatie over scholen",
        "Leren plannen / studietips",
        "Anders",
    ]
    
    return rx.vstack(
        rx.text(
            "Wat wil je verbeteren met EduChat?",
            font_size="16px",
            font_weight="500",
            color=COLORS["text_primary"],
            margin_bottom="8px",
        ),
        checkbox_list(
            options=options,
            selected_values=state.improvement_areas,
            on_toggle=state.toggle_improvement_area,
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def question_step_6(state: OnboardingState) -> rx.Component:
    """Question: Hoe formeel mag EduChat met je praten?"""
    options = ["Jong & casual", "Normaal", "Zakelijk / professioneel"]
    
    return rx.vstack(
        rx.text(
            "Hoe formeel mag EduChat met je praten?",
            font_size="16px",
            font_weight="500",
            color=COLORS["text_primary"],
            margin_bottom="8px",
        ),
        radio_group(
            options=options,
            selected_value=state.formality,
            on_change=state.set_formality,
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def question_step_7(state: OnboardingState) -> rx.Component:
    """Question: Wat verwacht jij van EduChat?"""
    return rx.vstack(
        rx.text(
            "Wat verwacht jij van EduChat?",
            font_size="16px",
            font_weight="500",
            color=COLORS["text_primary"],
            margin_bottom="8px",
        ),
        text_area_input(
            value=state.expectations,
            on_change=state.set_expectations,
            placeholder="Vertel ons wat je verwacht...",
            max_chars=500,
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def quiz_content(state: OnboardingState) -> rx.Component:
    """Main quiz content with all questions - Compact non-scrollable."""
    return rx.vstack(
        # Back to chat link - compact
        rx.box(
            rx.link(
                rx.hstack(
                    rx.icon("arrow-left", size=16, color=COLORS["primary_green"]),
                    rx.text(
                        "Terug naar chat",
                        font_size="0.875rem",
                        color=COLORS["primary_green"],
                        font_weight="600",
                    ),
                    spacing="2",
                    align="center",
                    padding="8px 16px",
                    border_radius="8px",
                    transition="all 0.3s ease",
                    _hover={
                        "background": f"rgba(16, 163, 127, 0.08)",
                    },
                ),
                href="/",
                text_decoration="none",
            ),
            margin_bottom="1.5rem",
            width="100%",
        ),
        
        # Logo - smaller
        rx.box(
            logo(size="md"),
            margin_bottom="1.5rem",
        ),
        
        # Badge above title - compact
        rx.box(
            rx.icon("user-check", size=14, color=COLORS["primary_green"]),
            rx.text("Personalisatie", font_size="12px", font_weight="700", color=COLORS["primary_green"]),
            display="flex",
            align_items="center",
            gap="6px",
            padding="6px 16px",
            background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(13, 138, 107, 0.15) 100%)",
            border_radius="50px",
            border=f"2px solid {COLORS['primary_green']}",
            margin_bottom="1rem",
            width="fit-content",
        ),
        
        # Main title - smaller
        rx.heading(
            "Vertel ons een beetje over jezelf",
            font_size=["1.25rem", "1.5rem", "1.75rem"],
            font_weight="800",
            background=f"linear-gradient(135deg, {COLORS['text_primary']} 0%, {COLORS['primary_green']} 100%)",
            background_clip="text",
            color="transparent",
            margin_bottom="0.5rem",
            line_height="1.2",
        ),
        
        # Subtitle - smaller
        rx.text(
            "Beantwoord een paar vragen zodat we EduChat kunnen personaliseren.",
            font_size=["0.875rem", "0.9375rem", "1rem"],
            color=COLORS["text_secondary"],
            line_height="1.5",
            margin_bottom="1.5rem",
            font_weight="500",
        ),
        
        # Progress bar - compact
        rx.box(
            progress_bar(
                current_step=state.current_step,
                total_steps=state.total_steps,
            ),
            margin_bottom="2rem",
            padding="16px",
            background="white",
            border_radius="12px",
            box_shadow="0 2px 12px rgba(0, 0, 0, 0.06)",
            border=f"1px solid {COLORS['border']}",
        ),
        
        # Question content (conditional rendering based on current step)
        rx.box(
            rx.cond(
                state.current_step == 0,
                question_step_0(state),
                rx.cond(
                    state.current_step == 1,
                    question_step_1(state),
                    rx.cond(
                        state.current_step == 2,
                        question_step_2(state),
                        rx.cond(
                            state.current_step == 3,
                            question_step_3(state),
                            rx.cond(
                                state.current_step == 4,
                                question_step_4(state),
                                rx.cond(
                                    state.current_step == 5,
                                    question_step_5(state),
                                    rx.cond(
                                        state.current_step == 6,
                                        question_step_6(state),
                                        question_step_7(state),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            flex="1",
            width="100%",
            margin_bottom="1.5rem",
        ),
        
        # Navigation buttons
        navigation_buttons(state),
        
        spacing="0",
        align="start",
        width="100%",
        max_width="550px",
        padding=["1rem", "1.5rem", "2rem"],
        height="100%",
        justify_content="center",
    )


def welcome_panel() -> rx.Component:
    """Right panel with welcome message and illustration - Enhanced."""
    return rx.box(
        # Animated background patterns
        rx.html(
            f'''<svg width="100%" height="100%" viewBox="0 0 800 1000" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.1; pointer-events: none;">
                <circle cx="150" cy="150" r="120" fill="white">
                    <animate attributeName="r" values="120;150;120" dur="6s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0.8;1;0.8" dur="6s" repeatCount="indefinite"/>
                </circle>
                <circle cx="650" cy="800" r="150" fill="white">
                    <animate attributeName="r" values="150;180;150" dur="7s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0.7;0.95;0.7" dur="7s" repeatCount="indefinite"/>
                </circle>
                <circle cx="700" cy="300" r="100" fill="white">
                    <animate attributeName="r" values="100;130;100" dur="5s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0.75;1;0.75" dur="5s" repeatCount="indefinite"/>
                </circle>
                <path d="M0,500 Q200,400 400,500 T800,500" stroke="white" stroke-width="3" fill="none" opacity="0.2">
                    <animate attributeName="d" 
                        values="M0,500 Q200,400 400,500 T800,500;
                                M0,500 Q200,450 400,500 T800,500;
                                M0,500 Q200,400 400,500 T800,500" 
                        dur="8s" repeatCount="indefinite"/>
                </path>
            </svg>''',
            position="absolute",
            top="0",
            left="0",
            width="100%",
            height="100%",
            pointer_events="none",
        ),
        
        rx.vstack(
            # Badge at top
            rx.box(
                rx.icon("sparkles", size=16, color="white"),
                rx.text("AI-Powered Studiegids", font_size="14px", font_weight="700", color="white"),
                display="flex",
                align_items="center",
                gap="8px",
                padding="10px 24px",
                background="rgba(255, 255, 255, 0.15)",
                backdrop_filter="blur(10px)",
                border_radius="50px",
                border="2px solid rgba(255, 255, 255, 0.3)",
                margin_bottom="32px",
                box_shadow="0 8px 24px rgba(0, 0, 0, 0.15)",
                animation="fadeIn 0.8s ease-out",
            ),
            
            # Welcome heading
            rx.vstack(
                rx.heading(
                    "Welkom bij",
                    font_size=["2rem", "2.25rem", "2.5rem"],
                    font_weight="600",
                    color="rgba(255, 255, 255, 0.95)",
                    text_align="center",
                    line_height="1.2",
                    animation="fadeIn 0.8s ease-out 0.1s backwards",
                ),
                rx.heading(
                    "EduChat",
                    font_size=["3.5rem", "4rem", "4.5rem"],
                    font_weight="800",
                    color="white",
                    text_align="center",
                    line_height="1",
                    margin_top="0.5rem",
                    letter_spacing="-0.02em",
                    text_shadow="0 4px 20px rgba(0, 0, 0, 0.2)",
                    animation="fadeIn 0.8s ease-out 0.2s backwards",
                ),
                spacing="0",
                margin_bottom="3rem",
            ),
            
            # Illustration with enhanced card
            rx.box(
                rx.box(
                    rx.image(
                        src="/ai_assistant_illustration.svg",
                        width=["300px", "350px", "400px"],
                        height=["225px", "262px", "300px"],
                        alt="AI Assistant",
                        object_fit="contain",
                    ),
                    padding="3rem",
                    background="rgba(255, 255, 255, 0.1)",
                    backdrop_filter="blur(10px)",
                    border_radius="24px",
                    border="2px solid rgba(255, 255, 255, 0.2)",
                    box_shadow="0 12px 48px rgba(0, 0, 0, 0.2)",
                ),
                display="flex",
                justify_content="center",
                align_items="center",
                margin_bottom="3rem",
                animation="fadeIn 1s ease-out 0.4s backwards",
            ),
            
            # Description with enhanced card
            rx.box(
                rx.vstack(
                    rx.text(
                        "EduChat helpt je makkelijk informatie te vinden over het Ministerie van Onderwijs (MINOV) en alles wat met onderwijs in Suriname te maken heeft.",
                        font_size=["1rem", "1.0625rem", "1.125rem"],
                        color="rgba(255, 255, 255, 0.95)",
                        line_height="1.7",
                        text_align="center",
                        font_weight="500",
                    ),
                    rx.text(
                        "Of je nu studiekeuzes wilt vergelijken, schoolinfo zoekt, of gewoon nieuwsgierig bent – het is er om het jou simpel uit te leggen, op jouw manier.",
                        font_size=["0.9375rem", "1rem", "1.0625rem"],
                        color="rgba(255, 255, 255, 0.9)",
                        line_height="1.7",
                        text_align="center",
                        margin_top="1rem",
                    ),
                    spacing="0",
                ),
                max_width="520px",
                padding="32px",
                background="rgba(255, 255, 255, 0.1)",
                backdrop_filter="blur(10px)",
                border_radius="20px",
                border="1px solid rgba(255, 255, 255, 0.2)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.15)",
                animation="fadeInUp 0.8s ease-out 0.6s backwards",
            ),
            
            # Trust indicators
            rx.hstack(
                rx.box(
                    rx.icon("users", size=18, color="white"),
                    rx.text("100+ Studenten", font_size="13px", color="white", font_weight="600"),
                    display="flex",
                    align_items="center",
                    gap="8px",
                    padding="10px 20px",
                    background="rgba(255, 255, 255, 0.15)",
                    border_radius="50px",
                ),
                rx.box(
                    rx.icon("shield-check", size=18, color="white"),
                    rx.text("100% Betrouwbaar", font_size="13px", color="white", font_weight="600"),
                    display="flex",
                    align_items="center",
                    gap="8px",
                    padding="10px 20px",
                    background="rgba(255, 255, 255, 0.15)",
                    border_radius="50px",
                ),
                spacing="4",
                flex_wrap="wrap",
                justify="center",
                margin_top="3rem",
                animation="fadeIn 0.8s ease-out 0.8s backwards",
            ),
            
            spacing="0",
            align="center",
            justify="center",
            width="100%",
            height="100%",
            padding=["3rem", "3.5rem", "4rem"],
            position="relative",
            z_index="1",
        ),
        
        position="relative",
        width="100%",
        height="100%",
    )


def onboarding() -> rx.Component:
    """Main onboarding page with responsive split layout - Non-scrollable."""
    return rx.box(
        rx.hstack(
            # Left panel - Quiz (no scroll)
            rx.box(
                quiz_content(OnboardingState),
                width="100%",
                height="100vh",
                background=COLORS["white"],
                overflow="hidden",
                display="flex",
                align_items="center",
                justify_content="center",
                **{
                    "@media (min-width: 1024px)": {
                        "width": "50%",
                    }
                }
            ),
            
            # Right panel - Welcome (hidden on mobile)
            rx.box(
                welcome_panel(),
                width="0",
                height="100vh",
                background=COLORS["primary_green"],
                overflow="hidden",
                display="none",
                **{
                    "@media (min-width: 1024px)": {
                        "display": "flex",
                        "width": "50%",
                    }
                }
            ),
            
            spacing="0",
            width="100%",
            height="100vh",
            align="stretch",
        ),
        width="100vw",
        height="100vh",
        overflow="hidden",
        position="fixed",
        top="0",
        left="0",
    )

