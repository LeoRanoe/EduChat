"""Redesigned onboarding page with modern card-based interface."""
import reflex as rx
from educhat.state.onboarding_state import (
    OnboardingState,
    EDUCATION_LEVELS,
    AGE_GROUPS,
    DISTRICTS,
    SCHOOL_SUBJECTS,
    STUDY_DIRECTIONS,
    IMPROVEMENT_GOALS,
    FORMALITY_OPTIONS,
    FUTURE_PLAN_OPTIONS,
)
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
    """Modern floating navigation with smooth transitions."""
    return rx.box(
        rx.hstack(
            # Back button - modern outline style
            rx.cond(
                state.current_step > 0,
                rx.button(
                    rx.icon("chevron-left", size=20),
                    on_click=state.previous_step,
                    background="white",
                    color=COLORS["text_secondary"],
                    border=f"1.5px solid {COLORS['border']}",
                    border_radius="12px",
                    padding="12px",
                    width="48px",
                    height="48px",
                    cursor="pointer",
                    transition="all 0.3s ease",
                    box_shadow="0 2px 8px rgba(0,0,0,0.04)",
                    _hover={
                        "border_color": COLORS["primary_green"],
                        "color": COLORS["primary_green"],
                        "box_shadow": "0 4px 12px rgba(16,163,127,0.15)",
                        "transform": "translateY(-2px)",
                    },
                ),
                rx.box(width="1px"),
            ),
            
            rx.spacer(),
            
            # Progress indicator dots
            rx.hstack(
                *[
                    rx.box(
                        width="8px",
                        height="8px",
                        border_radius="50%",
                        background=rx.cond(
                            state.current_step >= i,
                            COLORS["primary_green"],
                            COLORS["gray_300"]
                        ),
                        transition="all 0.3s ease",
                    )
                    for i in range(8)
                ],
                spacing="2",
                display=["none", "flex", "flex"],
            ),
            
            rx.spacer(),
            
            # Next/Skip/Complete button group
            rx.hstack(
                # Skip (ghost button)
                rx.cond(
                    state.current_step < state.total_steps - 1,
                    rx.button(
                        "Skip",
                        on_click=state.skip_step,
                        background="transparent",
                        color=COLORS["text_tertiary"],
                        border="none",
                        padding="12px 20px",
                        height="48px",
                        font_size="0.9375rem",
                        font_weight="500",
                        cursor="pointer",
                        transition="all 0.2s ease",
                        _hover={
                            "color": COLORS["text_secondary"],
                        },
                    ),
                    rx.box(width="1px"),
                ),
                
                # Next/Complete button
                rx.cond(
                    state.current_step < state.total_steps - 1,
                    rx.button(
                        rx.hstack(
                            rx.text("Next", font_weight="600"),
                            rx.icon("arrow-right", size=18),
                            spacing="2",
                            align="center",
                        ),
                        on_click=state.next_step,
                        background=COLORS["primary_green"],
                        color="white",
                        border="none",
                        border_radius="12px",
                        padding="12px 28px",
                        height="48px",
                        font_size="0.9375rem",
                        cursor="pointer",
                        transition="all 0.3s ease",
                        box_shadow="0 4px 16px rgba(16,163,127,0.25)",
                        _hover={
                            "background": COLORS["primary_hover"],
                            "box_shadow": "0 6px 20px rgba(16,163,127,0.35)",
                            "transform": "translateY(-2px)",
                        },
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("check-circle", size=18),
                            rx.text("Complete", font_weight="600"),
                            spacing="2",
                            align="center",
                        ),
                        on_click=state.complete_quiz,
                        background=COLORS["primary_green"],
                        color="white",
                        border="none",
                        border_radius="12px",
                        padding="12px 32px",
                        height="48px",
                        font_size="1rem",
                        cursor="pointer",
                        transition="all 0.3s ease",
                        box_shadow="0 4px 16px rgba(16,163,127,0.3)",
                        _hover={
                            "background": COLORS["primary_hover"],
                            "box_shadow": "0 6px 24px rgba(16,163,127,0.4)",
                            "transform": "translateY(-2px)",
                        },
                    ),
                ),
                spacing="3",
                align="center",
            ),
            
            spacing="4",
            width="100%",
            align="center",
            padding="16px 24px",
            max_width="800px",
            margin="0 auto",
        ),
        position="fixed",
        bottom="0",
        left="0",
        right="0",
        z_index="100",
        background="white",
        border_top=f"1px solid {COLORS['border_light']}",
        box_shadow="0 -4px 16px rgba(0,0,0,0.06)",
    )


def question_step_0(state: OnboardingState) -> rx.Component:
    """Question: Welke opleiding volg je momenteel?"""
    return rx.vstack(
        rx.heading(
            "Welke opleiding volg je momenteel?",
            font_size=["1rem", "1.0625rem", "1.125rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            line_height="1.3",
            margin_bottom="0.375rem",
            as_="h2",
        ),
        rx.text(
            "Dit helpt ons om informatie op jouw niveau aan te passen.",
            font_size="0.875rem",
            color=COLORS["text_secondary"],
            line_height="1.4",
            margin_bottom="1rem",
        ),
        dropdown_select(
            options=EDUCATION_LEVELS,
            value=state.education_level,
            on_change=state.set_education_level,
            placeholder="Selecteer je huidige opleiding...",
        ),
        spacing="0",
        align="start",
        width="100%",
    )


def question_step_1(state: OnboardingState) -> rx.Component:
    """Question: Wat is jouw leeftijd?"""
    return rx.vstack(
        rx.heading(
            "Wat is jouw leeftijd?",
            font_size=["1rem", "1.0625rem", "1.125rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            line_height="1.3",
            margin_bottom="0.375rem",
            as_="h2",
        ),
        rx.text(
            "We passen onze communicatie aan op jouw leeftijdsgroep.",
            font_size="0.875rem",
            color=COLORS["text_secondary"],
            line_height="1.4",
            margin_bottom="1rem",
        ),
        dropdown_select(
            options=AGE_GROUPS,
            value=state.age,
            on_change=state.set_age,
            placeholder="Selecteer je leeftijdsgroep...",
        ),
        spacing="0",
        align="start",
        width="100%",
    )


def question_step_2(state: OnboardingState) -> rx.Component:
    """Question: In welk district woon je?"""
    return rx.vstack(
        rx.heading(
            "In welk district woon je?",
            font_size=["1rem", "1.0625rem", "1.125rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            line_height="1.3",
            margin_bottom="0.375rem",
            as_="h2",
        ),
        rx.text(
            "We kunnen je informatie geven over scholen in jouw regio.",
            font_size="0.875rem",
            color=COLORS["text_secondary"],
            line_height="1.4",
            margin_bottom="1rem",
        ),
        dropdown_select(
            options=DISTRICTS,
            value=state.district,
            on_change=state.set_district,
            placeholder="Selecteer je district...",
        ),
        spacing="0",
        align="start",
        width="100%",
    )


def question_step_3(state: OnboardingState) -> rx.Component:
    """Question: Wat zijn je favoriete vakken?"""
    return rx.vstack(
        rx.heading(
            "Wat zijn je favoriete vakken?",
            font_size=["1rem", "1.0625rem", "1.125rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            line_height="1.3",
            margin_bottom="0.375rem",
            as_="h2",
        ),
        rx.text(
            "Selecteer de vakken waar je het meest van houdt (meerdere mogelijk).",
            font_size="0.875rem",
            color=COLORS["text_secondary"],
            line_height="1.4",
            margin_bottom="0.625rem",
        ),
        multi_select_group(
            options=SCHOOL_SUBJECTS,
            selected_values=state.favorite_subjects,
            on_toggle=state.toggle_subject,
        ),
        spacing="0",
        align="start",
        width="100%",
    )


def question_step_4(state: OnboardingState) -> rx.Component:
    """Question: Heb je plannen om verder te studeren na deze opleiding?"""
    return rx.vstack(
        rx.heading(
            "Heb je plannen om verder te studeren?",
            font_size=["1rem", "1.0625rem", "1.125rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            line_height="1.3",
            margin_bottom="0.375rem",
            as_="h2",
        ),
        rx.text(
            "We kunnen je helpen met studiekeuzes en toekomstplanning.",
            font_size="0.875rem",
            color=COLORS["text_secondary"],
            line_height="1.4",
            margin_bottom="0.625rem",
        ),
        radio_group(
            options=FUTURE_PLAN_OPTIONS,
            selected_value=state.future_plans,
            on_change=state.set_future_plans,
        ),
        spacing="0",
        align="start",
        width="100%",
    )


def question_step_5(state: OnboardingState) -> rx.Component:
    """Question: Wat wil je verbeteren met EduChat?"""
    return rx.vstack(
        rx.heading(
            "Waarmee kan EduChat je helpen?",
            font_size=["1rem", "1.0625rem", "1.125rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            line_height="1.3",
            margin_bottom="0.375rem",
            as_="h2",
        ),
        rx.text(
            "Selecteer alles wat van toepassing is (meerdere mogelijk).",
            font_size="0.875rem",
            color=COLORS["text_secondary"],
            line_height="1.4",
            margin_bottom="0.625rem",
        ),
        multi_select_group(
            options=IMPROVEMENT_GOALS,
            selected_values=state.improvement_areas,
            on_toggle=state.toggle_improvement_area,
        ),
        spacing="0",
        align="start",
        width="100%",
    )


def question_step_6(state: OnboardingState) -> rx.Component:
    """Question: Hoe formeel mag EduChat met je praten?"""
    return rx.vstack(
        rx.heading(
            "Hoe mag EduChat met je communiceren?",
            font_size=["1rem", "1.0625rem", "1.125rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            line_height="1.3",
            margin_bottom="0.375rem",
            as_="h2",
        ),
        rx.text(
            "Kies de communicatiestijl die het beste bij je past.",
            font_size="0.875rem",
            color=COLORS["text_secondary"],
            line_height="1.4",
            margin_bottom="0.625rem",
        ),
        radio_group(
            options=FORMALITY_OPTIONS,
            selected_value=state.formality,
            on_change=state.set_formality,
        ),
        spacing="0",
        align="start",
        width="100%",
    )


def question_step_7(state: OnboardingState) -> rx.Component:
    """Question: Welke studierichtingen interesseren je?"""
    return rx.vstack(
        rx.heading(
            "Welke studierichtingen interesseren je?",
            font_size=["1rem", "1.0625rem", "1.125rem"],
            font_weight="700",
            color=COLORS["text_primary"],
            line_height="1.3",
            margin_bottom="0.375rem",
            as_="h2",
        ),
        rx.text(
            "Selecteer de gebieden waar je meer over wilt weten (meerdere mogelijk).",
            font_size="0.875rem",
            color=COLORS["text_secondary"],
            line_height="1.4",
            margin_bottom="0.625rem",
        ),
        multi_select_group(
            options=STUDY_DIRECTIONS,
            selected_values=state.study_direction,
            on_toggle=state.toggle_study_direction,
        ),
        spacing="0",
        align="start",
        width="100%",
    )


def quiz_content(state: OnboardingState) -> rx.Component:
    """Reimagined quiz with animated cards and modern layout."""
    return rx.box(
        # Animated gradient background
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=f"linear-gradient(135deg, {COLORS['gray_50']} 0%, {COLORS['primary_light']} 50%, {COLORS['gray_50']} 100%)",
            opacity="0.4",
            z_index="0",
        ),
        
        # Main content - perfectly centered
        rx.center(
            rx.vstack(
                # Header with logo and step counter
                rx.hstack(
                    # Logo link
                    rx.link(
                        rx.hstack(
                            rx.icon("graduation-cap", size=24, color=COLORS["primary_green"]),
                            rx.text(
                                "EduChat",
                                font_size="1.25rem",
                                font_weight="700",
                                color=COLORS["primary_green"],
                            ),
                            spacing="2",
                            align="center",
                        ),
                        href="/chat",
                        text_decoration="none",
                    ),
                    
                    rx.spacer(),
                    
                    # Step counter badge
                    rx.hstack(
                        rx.text(
                            f"Step {state.current_step + 1}",
                            font_size="0.875rem",
                            font_weight="600",
                            color=COLORS["primary_green"],
                        ),
                        rx.text(
                            f"/ {state.total_steps}",
                            font_size="0.875rem",
                            color=COLORS["text_tertiary"],
                        ),
                        spacing="1",
                        padding="8px 16px",
                        background="white",
                        border_radius="24px",
                        border=f"2px solid {COLORS['primary_light']}",
                        box_shadow="0 2px 8px rgba(16,163,127,0.1)",
                    ),
                    
                    width="100%",
                    align="center",
                    margin_bottom="2rem",
                ),
                
                # Main question card with animation
                rx.box(
                    rx.vstack(
                        # Question icon and number
                        rx.center(
                            rx.box(
                                rx.text(
                                    state.current_step + 1,
                                    font_size="1.5rem",
                                    font_weight="700",
                                    color="white",
                                ),
                                width="56px",
                                height="56px",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['primary_hover']} 100%)",
                                border_radius="16px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                box_shadow="0 8px 24px rgba(16,163,127,0.3)",
                                margin_bottom="1.5rem",
                            ),
                        ),
                        
                        # Question content
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
                        
                        spacing="0",
                        align="center",
                        width="100%",
                    ),
                    
                    width="100%",
                    padding=["2rem", "2.5rem", "3rem"],
                    background="white",
                    border_radius="24px",
                    box_shadow="0 12px 48px rgba(0,0,0,0.08)",
                    border=f"1px solid {COLORS['border_light']}",
                    position="relative",
                    overflow="hidden",
                ),
                
                # Progress bar
                rx.box(
                    progress_bar(
                        current_step=state.current_step,
                        total_steps=state.total_steps,
                    ),
                    width="100%",
                    margin_top="2rem",
                    margin_bottom="2rem",
                ),
                
                spacing="0",
                width="100%",
                max_width="700px",
                padding=["1.5rem", "2rem"],
                padding_bottom="140px",  # Extra space for fixed buttons
            ),
            
            width="100%",
            min_height="100vh",
            padding_bottom="100px",
        ),
        
        # Navigation footer - fixed at bottom
        navigation_buttons(state),
        
        position="relative",
        width="100%",
        min_height="100vh",
        overflow_y="auto",
    )


def welcome_panel() -> rx.Component:
    """Redesigned modern sidebar with features and benefits."""
    return rx.box(
        rx.vstack(
            # Animated brand header
            rx.vstack(
                rx.box(
                    rx.icon(
                        "graduation-cap",
                        size=48,
                        color="white",
                    ),
                    width="88px",
                    height="88px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    background="rgba(255,255,255,0.15)",
                    backdrop_filter="blur(10px)",
                    border_radius="22px",
                    border="2px solid rgba(255,255,255,0.2)",
                    margin_bottom="1.5rem",
                ),
                
                rx.heading(
                    "Let's Get Started!",
                    font_size="2.5rem",
                    font_weight="700",
                    color="white",
                    text_align="center",
                    line_height="1.2",
                    margin_bottom="0.75rem",
                ),
                
                rx.text(
                    "Customize your learning experience in just a few steps",
                    font_size="1.125rem",
                    color="rgba(255,255,255,0.9)",
                    text_align="center",
                    line_height="1.6",
                    max_width="420px",
                ),
                
                spacing="0",
                align="center",
                margin_bottom="3rem",
            ),
            
            # Features list
            rx.vstack(
                # Feature 1
                rx.hstack(
                    rx.box(
                        rx.icon("sparkles", size=24, color=COLORS["primary_green"]),
                        width="56px",
                        height="56px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background="white",
                        border_radius="14px",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(
                            "AI-Powered Assistance",
                            font_size="1.0625rem",
                            font_weight="600",
                            color="white",
                            margin_bottom="4px",
                        ),
                        rx.text(
                            "Smart answers tailored to your education level",
                            font_size="0.9375rem",
                            color="rgba(255,255,255,0.85)",
                            line_height="1.5",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="4",
                    align="start",
                    width="100%",
                    padding="20px",
                    background="rgba(255,255,255,0.08)",
                    backdrop_filter="blur(10px)",
                    border_radius="16px",
                    border="1px solid rgba(255,255,255,0.12)",
                ),
                
                # Feature 2
                rx.hstack(
                    rx.box(
                        rx.icon("book-open", size=24, color=COLORS["primary_green"]),
                        width="56px",
                        height="56px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background="white",
                        border_radius="14px",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(
                            "Comprehensive Database",
                            font_size="1.0625rem",
                            font_weight="600",
                            color="white",
                            margin_bottom="4px",
                        ),
                        rx.text(
                            "Access to all Suriname education information",
                            font_size="0.9375rem",
                            color="rgba(255,255,255,0.85)",
                            line_height="1.5",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="4",
                    align="start",
                    width="100%",
                    padding="20px",
                    background="rgba(255,255,255,0.08)",
                    backdrop_filter="blur(10px)",
                    border_radius="16px",
                    border="1px solid rgba(255,255,255,0.12)",
                ),
                
                # Feature 3
                rx.hstack(
                    rx.box(
                        rx.icon("target", size=24, color=COLORS["primary_green"]),
                        width="56px",
                        height="56px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background="white",
                        border_radius="14px",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(
                            "Personalized Experience",
                            font_size="1.0625rem",
                            font_weight="600",
                            color="white",
                            margin_bottom="4px",
                        ),
                        rx.text(
                            "Content adapted to your goals and preferences",
                            font_size="0.9375rem",
                            color="rgba(255,255,255,0.85)",
                            line_height="1.5",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="4",
                    align="start",
                    width="100%",
                    padding="20px",
                    background="rgba(255,255,255,0.08)",
                    backdrop_filter="blur(10px)",
                    border_radius="16px",
                    border="1px solid rgba(255,255,255,0.12)",
                ),
                
                spacing="4",
                width="100%",
            ),
            
            spacing="0",
            align="center",
            justify="center",
            width="100%",
            height="100%",
            padding="4rem 3rem",
        ),
        
        width="100%",
        height="100%",
        position="relative",
    )


def onboarding() -> rx.Component:
    """Modern onboarding with side-by-side card layout."""
    return rx.fragment(
        rx.box(
            # Background decoration
            rx.box(
                rx.box(
                    position="absolute",
                    top="-200px",
                    right="-200px",
                    width="500px",
                    height="500px",
                    background=f"radial-gradient(circle, {COLORS['primary_light']} 0%, transparent 70%)",
                    opacity="0.5",
                    pointer_events="none",
                ),
                rx.box(
                    position="absolute",
                    bottom="-150px",
                    left="-150px",
                    width="400px",
                    height="400px",
                    background=f"radial-gradient(circle, {COLORS['primary_light']} 0%, transparent 70%)",
                    opacity="0.4",
                    pointer_events="none",
                ),
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                overflow="hidden",
                pointer_events="none",
            ),
            
            # Main content
            rx.box(
                rx.hstack(
                    # Main quiz area
                    rx.box(
                        quiz_content(OnboardingState),
                        width="100%",
                        height="100vh",
                        background="transparent",
                        position="relative",
                        z_index="1",
                        **{
                            "@media (min-width: 1024px)": {
                                "width": "60%",
                            }
                        }
                    ),
                    
                    # Right sidebar with features - visible on desktop
                    rx.box(
                        welcome_panel(),
                        width="0",
                        height="100vh",
                        background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['primary_hover']} 100%)",
                        position="relative",
                        display="none",
                        overflow="hidden",
                        box_shadow="-8px 0 24px rgba(0,0,0,0.08)",
                        **{
                            "@media (min-width: 1024px)": {
                                "display": "flex",
                                "width": "40%",
                            }
                        }
                    ),
                    
                    spacing="0",
                    width="100%",
                    align="stretch",
                ),
                
                position="relative",
                z_index="1",
            ),
            
            width="100vw",
            height="100vh",
            overflow="hidden",
            position="relative",
            background=COLORS["white"],
        ),
    )
