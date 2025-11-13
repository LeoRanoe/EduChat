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
        # Back to chat link
        rx.box(
            rx.link(
                rx.hstack(
                    rx.icon("arrow-left", size=18, color=COLORS["primary_green"]),
                    rx.text(
                        "Terug naar chat",
                        font_size="0.875rem",
                        color=COLORS["primary_green"],
                        font_weight="500",
                    ),
                    spacing="2",
                    align="center",
                ),
                href="/",
                text_decoration="none",
            ),
            margin_bottom="2rem",
            width="100%",
        ),
        
        # Logo at top
        rx.box(
            logo(size="lg"),
            margin_bottom="3rem",
        ),
        
        # Main title
        rx.heading(
            "Vertel ons een beetje over jouw",
            font_size=["1.5rem", "1.75rem", "2rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            margin_bottom="0.75rem",
            line_height="1.2",
        ),
        
        # Subtitle
        rx.text(
            "Beantwoord een paar vragen zodat we EduChat kunnen personaliseren voor jouw behoeften.",
            font_size=["0.875rem", "0.9375rem", "1rem"],
            color=COLORS["text_secondary"],
            line_height="1.6",
            margin_bottom="2rem",
        ),
        
        # Progress bar
        rx.box(
            progress_bar(
                current_step=state.current_step,
                total_steps=state.total_steps,
            ),
            margin_bottom="2.5rem",
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
            margin_bottom="2rem",
        ),
        
        # Navigation buttons
        navigation_buttons(state),
        
        spacing="0",
        align="start",
        width="100%",
        max_width="600px",
        padding=["1.5rem", "2rem", "3rem"],
    )


def welcome_panel() -> rx.Component:
    """Right panel with welcome message and illustration."""
    return rx.vstack(
        # Welcome heading
        rx.vstack(
            rx.heading(
                "Welkom bij",
                font_size=["1.75rem", "2rem", "2.25rem"],
                font_weight="600",
                color="rgba(255, 255, 255, 0.95)",
                text_align="center",
                line_height="1.2",
            ),
            rx.heading(
                "EduChat",
                font_size=["3rem", "3.5rem", "4rem"],
                font_weight="700",
                color="#FFFFFF",
                text_align="center",
                line_height="1",
                margin_top="0.25rem",
            ),
            spacing="0",
            margin_bottom="3rem",
        ),
        
        # AI Assistant Illustration
        rx.box(
            rx.image(
                src="/ai_assistant_illustration.svg",
                width=["300px", "350px", "400px"],
                height=["225px", "262px", "300px"],
                alt="AI Assistant",
                object_fit="contain",
            ),
            display="flex",
            justify_content="center",
            align_items="center",
            margin_bottom="2.5rem",
        ),
        
        # Description text
        rx.vstack(
            rx.text(
                "EduChat helpt je makkelijk informatie te vinden over het Ministerie van Onderwijs (MINOV) en alles wat met onderwijs in Suriname te maken heeft.",
                font_size=["0.9375rem", "1rem", "1.0625rem"],
                color="rgba(255, 255, 255, 0.92)",
                line_height="1.7",
                text_align="center",
            ),
            rx.text(
                "Of je nu studiekeuzes wilt vergelijken, schoolinfo zoekt, of gewoon nieuwsgierig bent – het is er om het jou simpel uit te leggen, op jouw manier.",
                font_size=["0.9375rem", "1rem", "1.0625rem"],
                color="rgba(255, 255, 255, 0.88)",
                line_height="1.7",
                text_align="center",
                margin_top="1.25rem",
            ),
            max_width="480px",
            spacing="0",
        ),
        
        spacing="0",
        align="center",
        justify="center",
        width="100%",
        height="100%",
        padding=["2.5rem", "3rem", "4rem"],
    )


def onboarding() -> rx.Component:
    """Main onboarding page with responsive split layout."""
    return rx.box(
        rx.hstack(
            # Left panel - Quiz
            rx.box(
                rx.box(
                    quiz_content(OnboardingState),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    min_height="100vh",
                    width="100%",
                ),
                width="100%",
                height="100vh",
                background=COLORS["white"],
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
                width="0",
                height="100vh",
                background=COLORS["primary_green"],
                overflow_y="auto",
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
        width="100%",
        height="100vh",
        overflow="hidden",
    )
