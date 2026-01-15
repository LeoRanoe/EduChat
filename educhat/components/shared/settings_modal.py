"""Settings modal component for EduChat."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS
from educhat.state.auth_state import AuthState
from educhat.state.onboarding_state import OnboardingState


def settings_modal() -> rx.Component:
    """Modal for user settings and preferences."""
    return rx.cond(
        AuthState.show_settings_modal,
        rx.box(
            # Overlay
            rx.box(
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background="rgba(0, 0, 0, 0.5)",
                z_index="1000",
                on_click=AuthState.toggle_settings_modal,
            ),
            # Modal content
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.hstack(
                            rx.icon("settings", size=20, color=COLORS["primary_green"]),
                            rx.text(
                                "Instellingen",
                                font_size="1.25rem",
                                font_weight="700",
                                color=COLORS["text_primary"],
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.box(
                            rx.icon("x", size=18, color=COLORS["text_secondary"]),
                            on_click=AuthState.toggle_settings_modal,
                            cursor="pointer",
                            padding="0.625rem",
                            border_radius=RADIUS["sm"],
                            _hover={
                                "background": COLORS["light_gray"],
                            },
                            transition="all 0.2s ease",
                        ),
                        justify="between",
                        width="100%",
                    ),
                    
                    # Settings content
                    rx.vstack(
                        # Personalization section - Edit onboarding
                        rx.cond(
                            AuthState.is_authenticated,
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "Personalisatie",
                                        font_size="0.875rem",
                                        font_weight="600",
                                        color=COLORS["text_primary"],
                                        margin_bottom="0.5rem",
                                    ),
                                    # Edit preferences button
                                    rx.link(
                                        rx.hstack(
                                            rx.hstack(
                                                rx.icon("user-cog", size=18, color=COLORS["primary_green"]),
                                                rx.vstack(
                                                    rx.text(
                                                        "Mijn voorkeuren aanpassen",
                                                        font_size="0.9375rem",
                                                        font_weight="500",
                                                        color=COLORS["text_primary"],
                                                        line_height="1.2",
                                                    ),
                                                    rx.text(
                                                        "Wijzig je opleiding, interesses en communicatiestijl",
                                                        font_size="0.75rem",
                                                        color=COLORS["text_tertiary"],
                                                        line_height="1.2",
                                                    ),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                spacing="3",
                                                align="center",
                                                flex="1",
                                            ),
                                            rx.icon("chevron-right", size=18, color=COLORS["text_secondary"]),
                                            justify="between",
                                            align="center",
                                            width="100%",
                                            padding="1rem",
                                            border_radius=RADIUS["md"],
                                            border=f"1px solid {COLORS['border_light']}",
                                            _hover={
                                                "background": f"rgba(16, 163, 127, 0.05)",
                                                "border_color": COLORS["primary_green"],
                                            },
                                            transition="all 0.2s ease",
                                        ),
                                        href="/onboarding",
                                        text_decoration="none",
                                        on_click=[OnboardingState.start_edit_mode, AuthState.toggle_settings_modal],
                                        width="100%",
                                    ),
                                    # Show current preferences summary
                                    rx.cond(
                                        OnboardingState.quiz_completed,
                                        rx.box(
                                            rx.vstack(
                                                rx.cond(
                                                    OnboardingState.education_level != "",
                                                    rx.hstack(
                                                        rx.text("Opleiding:", font_size="0.75rem", color=COLORS["text_secondary"], font_weight="600"),
                                                        rx.text(OnboardingState.education_level, font_size="0.75rem", color=COLORS["text_primary"]),
                                                        spacing="2",
                                                    ),
                                                    rx.fragment(),
                                                ),
                                                rx.cond(
                                                    OnboardingState.district != "",
                                                    rx.hstack(
                                                        rx.text("District:", font_size="0.75rem", color=COLORS["text_secondary"], font_weight="600"),
                                                        rx.text(OnboardingState.district, font_size="0.75rem", color=COLORS["text_primary"]),
                                                        spacing="2",
                                                    ),
                                                    rx.fragment(),
                                                ),
                                                rx.cond(
                                                    OnboardingState.formality != "",
                                                    rx.hstack(
                                                        rx.text("Stijl:", font_size="0.75rem", color=COLORS["text_secondary"], font_weight="600"),
                                                        rx.text(OnboardingState.formality, font_size="0.75rem", color=COLORS["text_primary"]),
                                                        spacing="2",
                                                    ),
                                                    rx.fragment(),
                                                ),
                                                spacing="1",
                                                align_items="start",
                                            ),
                                            padding="0.75rem",
                                            margin_top="0.5rem",
                                            border_radius=RADIUS["sm"],
                                            background=COLORS["light_gray"],
                                            width="100%",
                                        ),
                                        rx.box(
                                            rx.text(
                                                "Je hebt nog geen voorkeuren ingesteld. Klik hierboven om te beginnen.",
                                                font_size="0.75rem",
                                                color=COLORS["text_tertiary"],
                                                font_style="italic",
                                            ),
                                            padding="0.75rem",
                                            margin_top="0.5rem",
                                            border_radius=RADIUS["sm"],
                                            background=COLORS["light_gray"],
                                            width="100%",
                                        ),
                                    ),
                                    spacing="2",
                                    width="100%",
                                ),
                                width="100%",
                                margin_bottom="0.5rem",
                            ),
                            rx.fragment(),
                        ),
                        
                        # Appearance section
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Weergave",
                                    font_size="0.875rem",
                                    font_weight="600",
                                    color=COLORS["text_primary"],
                                    margin_bottom="0.5rem",
                                ),
                                # Dark mode toggle
                                rx.hstack(
                                    rx.hstack(
                                        rx.cond(
                                            AuthState.dark_mode,
                                            rx.icon("moon", size=18, color="#F59E0B"),
                                            rx.icon("sun", size=18, color="#6B7280"),
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                "Donkere modus",
                                                font_size="0.9375rem",
                                                font_weight="500",
                                                color=COLORS["text_primary"],
                                                line_height="1.2",
                                            ),
                                            rx.text(
                                                "Pas het kleurenschema aan",
                                                font_size="0.75rem",
                                                color=COLORS["text_tertiary"],
                                                line_height="1.2",
                                            ),
                                            spacing="1",
                                            align_items="start",
                                        ),
                                        spacing="3",
                                        align="center",
                                        flex="1",
                                    ),
                                    rx.box(
                                        rx.box(
                                            width="44px",
                                            height="24px",
                                            border_radius="12px",
                                            background=rx.cond(
                                                AuthState.dark_mode,
                                                COLORS["primary_green"],
                                                COLORS["border_gray"]
                                            ),
                                            position="relative",
                                            cursor="pointer",
                                            on_click=AuthState.toggle_dark_mode,
                                            transition="all 0.3s ease",
                                            _hover={
                                                "opacity": "0.8",
                                            },
                                        ),
                                        rx.box(
                                            width="18px",
                                            height="18px",
                                            border_radius="50%",
                                            background="white",
                                            position="absolute",
                                            top="3px",
                                            left=rx.cond(AuthState.dark_mode, "23px", "3px"),
                                            transition="all 0.3s ease",
                                            box_shadow="0 2px 4px rgba(0,0,0,0.2)",
                                        ),
                                        position="relative",
                                    ),
                                    justify="between",
                                    align="center",
                                    width="100%",
                                    padding="1rem",
                                    border_radius=RADIUS["md"],
                                    border=f"1px solid {COLORS['border_light']}",
                                    _hover={
                                        "background": COLORS["light_gray"],
                                    },
                                    transition="all 0.2s ease",
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            width="100%",
                        ),
                        
                        # Account section
                        rx.cond(
                            AuthState.is_authenticated,
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "Account",
                                        font_size="0.875rem",
                                        font_weight="600",
                                        color=COLORS["text_primary"],
                                        margin_bottom="0.5rem",
                                    ),
                                    # User info
                                    rx.box(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.icon("user", size=16, color=COLORS["text_secondary"]),
                                                rx.text(
                                                    AuthState.user_name,
                                                    font_size="0.9375rem",
                                                    color=COLORS["text_primary"],
                                                ),
                                                spacing="2",
                                                align="center",
                                            ),
                                            rx.hstack(
                                                rx.icon("mail", size=16, color=COLORS["text_secondary"]),
                                                rx.text(
                                                    AuthState.user_email,
                                                    font_size="0.875rem",
                                                    color=COLORS["text_secondary"],
                                                ),
                                                spacing="2",
                                                align="center",
                                            ),
                                            spacing="2",
                                            align_items="start",
                                            width="100%",
                                        ),
                                        padding="1rem",
                                        border_radius=RADIUS["md"],
                                        border=f"1px solid {COLORS['border_light']}",
                                        background=COLORS["light_gray"],
                                        width="100%",
                                    ),
                                    spacing="2",
                                    width="100%",
                                ),
                                width="100%",
                                margin_top="1rem",
                            ),
                            rx.fragment(),
                        ),
                        
                        # About section
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Over EduChat",
                                    font_size="0.875rem",
                                    font_weight="600",
                                    color=COLORS["text_primary"],
                                    margin_bottom="0.5rem",
                                ),
                                rx.box(
                                    rx.text(
                                        "EduChat is jouw persoonlijke AI-assistent voor onderwijs en studie in Suriname. Vraag naar opleidingen, inschrijvingen, deadlines en meer!",
                                        font_size="0.875rem",
                                        color=COLORS["text_secondary"],
                                        line_height="1.6",
                                    ),
                                    padding="1rem",
                                    border_radius=RADIUS["md"],
                                    background=COLORS["light_gray"],
                                    width="100%",
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            width="100%",
                            margin_top="1rem",
                        ),
                        
                        spacing="3",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                width=["90%", "400px", "480px"],
                max_width="90vw",
                max_height="85vh",
                background=COLORS["white"],
                border_radius=RADIUS["xl"],
                padding="1.5rem",
                box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
                z_index="1001",
                overflow_y="auto",
            ),
        ),
    )
