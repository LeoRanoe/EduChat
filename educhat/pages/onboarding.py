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
    Navigation buttons for quiz (Back, Skip, Next).
    
    Args:
        state: Onboarding state instance
    """
    return rx.hstack(
        # Back button (only show if not on first step)
        rx.cond(
            state.current_step > 0,
            rx.button(
                rx.icon("arrow-left", size=16),
                " Terug",
                on_click=state.previous_step,
                background="transparent",
                color=COLORS["primary_green"],
                border=f"1px solid {COLORS['primary_green']}",
                border_radius="24px",
                padding="10px 20px",
                font_size="14px",
                cursor="pointer",
                _hover={
                    "background": "#F0F9F0",
                },
            ),
            rx.box(),
        ),
        rx.spacer(),
        # Skip button (only show if not on last step)
        rx.cond(
            state.current_step < state.total_steps - 1,
            rx.button(
                "Overslaan ",
                rx.icon("arrow-right", size=16),
                on_click=state.skip_step,
                background="transparent",
                color=COLORS["primary_green"],
                border=f"1px solid {COLORS['primary_green']}",
                border_radius="24px",
                padding="10px 20px",
                font_size="14px",
                cursor="pointer",
                _hover={
                    "background": "#F0F9F0",
                },
            ),
            # Complete button on last step
            rx.button(
                "Voltooi",
                on_click=state.complete_quiz,
                background=COLORS["primary_green"],
                color="#FFFFFF",
                border="none",
                border_radius="24px",
                padding="10px 24px",
                font_size="14px",
                font_weight="500",
                cursor="pointer",
                _hover={
                    "background": "#1A6B1A",
                },
            ),
        ),
        spacing="4",
        width="100%",
        margin_top="32px",
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
    """Main quiz content with all questions."""
    return rx.vstack(
        # Logo at top
        logo(size="md"),
        
        # Main title
        rx.heading(
            "Vertel ons een beetje over jouw",
            font_size="28px",
            font_weight="700",
            color=COLORS["text_primary"],
            margin_top="32px",
        ),
        
        # Subtitle
        rx.text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            font_size="14px",
            color=COLORS["text_secondary"],
            line_height="1.6",
            margin_top="8px",
        ),
        
        # Progress bar
        progress_bar(
            current_step=state.current_step,
            total_steps=state.total_steps,
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
            min_height="300px",
            width="100%",
        ),
        
        # Navigation buttons
        navigation_buttons(state),
        
        spacing="0",
        align="start",
        width="100%",
        padding="40px",
    )


def welcome_panel() -> rx.Component:
    """Right panel with welcome message and illustration."""
    return rx.vstack(
        rx.vstack(
            rx.heading(
                "Welkom bij",
                font_size="32px",
                font_weight="700",
                color="#FFFFFF",
                text_align="center",
            ),
            rx.heading(
                "EduChat",
                font_size="64px",
                font_weight="700",
                color="#FFFFFF",
                text_align="center",
                margin_top="-8px",
            ),
            spacing="0",
            margin_bottom="32px",
        ),
        
        # Illustration placeholder (you can add an actual image here)
        rx.box(
            rx.text(
                "🎓",
                font_size="120px",
                text_align="center",
            ),
            padding="40px",
        ),
        
        rx.text(
            "EduChat helpt je makkelijk informatie te vinden over het Ministerie van Onderwijs (MINOV) en alles wat met onderwijs in Suriname te maken heeft.",
            font_size="16px",
            color="#FFFFFF",
            line_height="1.8",
            text_align="center",
            max_width="400px",
            margin_top="24px",
        ),
        
        rx.text(
            "Of je nu studiekeuzes wilt vergelijken, schoolinfo zoekt, of gewoon nieuwsgierig bent het is er om het jou simpel uit te leggen, op jouw manier.",
            font_size="16px",
            color="#FFFFFF",
            line_height="1.8",
            text_align="center",
            max_width="400px",
            margin_top="16px",
        ),
        
        spacing="0",
        align="center",
        justify="center",
        width="100%",
        height="100%",
        padding="60px",
    )


def onboarding() -> rx.Component:
    """Main onboarding page with responsive split layout."""
    return rx.box(
        # Mobile: Stack vertically
        # Desktop: Side by side
        rx.hstack(
            # Left panel - Quiz
            rx.box(
                quiz_content(OnboardingState),
                width="100%",  # Full width on mobile
                height="100vh",
                background="#FFFFFF",
                overflow_y="auto",
                **{
                    "@media (min-width: 1024px)": {
                        "width": "50%",
                    }
                }
            ),
            
            # Right panel - Welcome (hidden on mobile)
            rx.box(
                welcome_panel(),
                width="0",  # Hidden on mobile
                height="100vh",
                background=COLORS["primary_green"],
                overflow_y="auto",
                display="none",  # Hidden on mobile/tablet
                **{
                    "@media (min-width: 1024px)": {
                        "display": "block",
                        "width": "50%",
                    }
                }
            ),
            
            spacing="0",
            width="100%",
            height="100vh",
        ),
        width="100%",
        height="100vh",
    )
