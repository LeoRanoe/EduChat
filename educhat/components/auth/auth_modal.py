"""
Authentication Modal Component - Professional Implementation
Modern, responsive login/signup modal with proper validation feedback,
loading states, and accessibility features.
"""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.styles.theme import COLORS, RADIUS, SHADOWS, TRANSITIONS


# ============================================================================
# CONFIGURATION
# ============================================================================

MODAL_CONFIG = {
    "width": ["95vw", "90vw", "900px"],
    "max_height": ["90vh", "85vh", "620px"],
    "left_panel_width": "45%",
    "right_panel_width": "55%",
}

INPUT_STYLES = {
    "base": {
        "width": "100%",
        "padding": "14px 14px 14px 42px",
        "border_radius": RADIUS["lg"],
        "font_size": "15px",
        "line_height": "1.5",
        "height": "48px",
        "color": COLORS["text_primary"],
        "background": "white",
        "outline": "none",
        "transition": TRANSITIONS["fast"],
    },
    "focus": {
        "border_color": COLORS["primary_green"],
        "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.12)",
    },
}


# ============================================================================
# MAIN MODAL COMPONENT
# ============================================================================

def auth_modal() -> rx.Component:
    """Main authentication modal component."""
    return rx.cond(
        AuthState.show_auth_modal,
        rx.box(
            # Backdrop with blur
            rx.box(
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                background="rgba(0, 0, 0, 0.5)",
                backdrop_filter="blur(8px)",
                z_index="999",
                on_click=AuthState.close_auth_modal,
                class_name="animate-fadeIn",
            ),
            
            # Modal Container
            rx.box(
                # Close Button
                rx.box(
                    rx.icon(
                        tag="x",
                        size=18,
                        color=COLORS["text_secondary"],
                    ),
                    position="absolute",
                    top="16px",
                    right="16px",
                    padding="10px",
                    cursor="pointer",
                    border_radius=RADIUS["full"],
                    background="white",
                    box_shadow=SHADOWS["sm"],
                    z_index="10",
                    on_click=AuthState.close_auth_modal,
                    transition=TRANSITIONS["fast"],
                    _hover={
                        "background": COLORS["light_gray"],
                        "transform": "scale(1.05)",
                    },
                ),
                
                # Two-column layout
                rx.box(
                    # Left: Branding (hidden on mobile)
                    _left_panel(),
                    
                    # Right: Form
                    _right_panel(),
                    
                    display="flex",
                    width="100%",
                    height="100%",
                ),
                
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                width=MODAL_CONFIG["width"],
                max_width="900px",
                max_height=MODAL_CONFIG["max_height"],
                background="white",
                border_radius=RADIUS["2xl"],
                box_shadow=SHADOWS["2xl"],
                overflow="hidden",
                z_index="1000",
                class_name="animate-scaleIn",
            ),
        ),
    )


# ============================================================================
# LEFT PANEL (BRANDING)
# ============================================================================


def _left_panel() -> rx.Component:
    """Left branding panel - hidden on mobile."""
    return rx.box(
        rx.box(
            # Logo with glow effect
            rx.box(
                rx.icon(
                    tag="shield-check",
                    size=48,
                    color="white",
                ),
                padding="16px",
                background="rgba(255, 255, 255, 0.15)",
                border_radius=RADIUS["2xl"],
                margin_bottom="24px",
                box_shadow="0 0 40px rgba(255, 255, 255, 0.2)",
            ),
            
            # Title
            rx.heading(
                "Welkom bij EduChat",
                size="7",
                color="white",
                margin_bottom="12px",
                font_weight="700",
                letter_spacing="-0.02em",
            ),
            
            # Subtitle
            rx.text(
                "Jouw AI-assistent voor Surinaams onderwijs",
                color="rgba(255,255,255,0.9)",
                font_size="15px",
                margin_bottom="32px",
                line_height="1.6",
            ),
            
            # Benefits list
            rx.box(
                _benefit_item("Directe antwoorden op je vragen"),
                _benefit_item("Studiemateriaal op maat"),
                _benefit_item("24/7 beschikbaar"),
                _benefit_item("Gratis te gebruiken"),
                display="flex",
                flex_direction="column",
                gap="14px",
            ),
            
            padding="40px",
            display="flex",
            flex_direction="column",
            justify_content="center",
            height="100%",
        ),
        
        width=MODAL_CONFIG["left_panel_width"],
        background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
        display=["none", "none", "flex"],
        position="relative",
        overflow="hidden",
        # Decorative circles
        _before={
            "content": "''",
            "position": "absolute",
            "top": "-50px",
            "right": "-50px",
            "width": "150px",
            "height": "150px",
            "background": "rgba(255,255,255,0.1)",
            "border_radius": "50%",
        },
        _after={
            "content": "''",
            "position": "absolute",
            "bottom": "-30px",
            "left": "-30px",
            "width": "100px",
            "height": "100px",
            "background": "rgba(255,255,255,0.08)",
            "border_radius": "50%",
        },
    )


def _benefit_item(text: str) -> rx.Component:
    """Single benefit item with checkmark."""
    return rx.box(
        rx.box(
            rx.icon(
                tag="check",
                size=14,
                color=COLORS["primary_green"],
            ),
            width="20px",
            height="20px",
            display="flex",
            align_items="center",
            justify_content="center",
            background="rgba(255,255,255,0.95)",
            border_radius=RADIUS["full"],
            flex_shrink="0",
        ),
        rx.text(
            text,
            color="rgba(255,255,255,0.95)",
            font_size="14px",
            margin_left="12px",
            font_weight="500",
        ),
        display="flex",
        align_items="center",
    )


# ============================================================================
# RIGHT PANEL (FORM)
# ============================================================================


def _right_panel() -> rx.Component:
    """Right panel with form."""
    return rx.box(
        # Header with logo (visible on mobile)
        rx.box(
            rx.box(
                rx.icon(
                    tag="graduation-cap",
                    size=28,
                    color=COLORS["primary_green"],
                ),
                rx.text(
                    "EduChat",
                    font_size="24px",
                    font_weight="700",
                    color=COLORS["primary_green"],
                    margin_left="10px",
                    letter_spacing="-0.02em",
                ),
                display="flex",
                align_items="center",
                margin_bottom="8px",
            ),
            rx.text(
                rx.cond(
                    AuthState.auth_mode == "login",
                    "Log in op je account",
                    "Maak een account aan"
                ),
                color=COLORS["text_secondary"],
                font_size="14px",
            ),
            margin_bottom="24px",
        ),
        
        # Tab Selector
        _tab_selector(),
        
        # Success Message
        rx.cond(
            AuthState.auth_success != "",
            rx.box(
                rx.box(
                    rx.icon(tag="check-circle", size=16, color=COLORS["success"]),
                    width="24px",
                    height="24px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    background=COLORS["success_light"],
                    border_radius=RADIUS["full"],
                    flex_shrink="0",
                ),
                rx.text(
                    AuthState.auth_success,
                    color=COLORS["success_dark"],
                    font_size="13px",
                    margin_left="10px",
                    font_weight="500",
                ),
                display="flex",
                align_items="center",
                padding="14px 16px",
                background=COLORS["success_light"],
                border=f"1px solid {COLORS['success']}30",
                border_radius=RADIUS["lg"],
                margin_bottom="16px",
                class_name="animate-fadeInUp",
            ),
        ),
        
        # Error Message  
        rx.cond(
            AuthState.auth_error != "",
            rx.box(
                rx.box(
                    rx.box(
                        rx.icon(tag="alert-circle", size=16, color=COLORS["error"]),
                        width="24px",
                        height="24px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background=COLORS["error_light"],
                        border_radius=RADIUS["full"],
                        flex_shrink="0",
                    ),
                    rx.text(
                        AuthState.auth_error,
                        color=COLORS["error_dark"],
                        font_size="13px",
                        margin_left="10px",
                        font_weight="500",
                    ),
                    display="flex",
                    align_items="center",
                ),
                
                # Show "Resend confirmation" button if email needs confirmation
                rx.cond(
                    AuthState.email_needs_confirmation,
                    rx.button(
                        rx.cond(
                            AuthState.resending_confirmation,
                            rx.box(
                                rx.spinner(size="1", color="white"),
                                rx.text("Verzenden...", margin_left="8px", font_size="12px"),
                                display="flex",
                                align_items="center",
                            ),
                            rx.box(
                                rx.icon(tag="mail", size=14),
                                rx.text("Bevestigingsmail opnieuw verzenden", margin_left="6px", font_size="12px"),
                                display="flex",
                                align_items="center",
                            ),
                        ),
                        width="100%",
                        padding="10px",
                        margin_top="12px",
                        background=COLORS["primary_green"],
                        color="white",
                        border="none",
                        border_radius=RADIUS["md"],
                        cursor="pointer",
                        font_weight="500",
                        on_click=AuthState.resend_confirmation_email,
                        transition=TRANSITIONS["fast"],
                        _hover={"background": COLORS["dark_green"]},
                        disabled=AuthState.resending_confirmation,
                    ),
                ),
                
                padding="14px 16px",
                background=COLORS["error_light"],
                border=f"1px solid {COLORS['error']}30",
                border_radius=RADIUS["lg"],
                margin_bottom="16px",
                display="flex",
                flex_direction="column",
                class_name="animate-shake",
            ),
        ),
        
        # Form Content
        rx.cond(
            AuthState.auth_mode == "login",
            _login_form(),
            _signup_form(),
        ),
        
        # Divider
        rx.box(
            rx.box(
                flex="1",
                height="1px",
                background=COLORS["border_light"],
            ),
            rx.text(
                "of",
                color=COLORS["text_tertiary"],
                font_size="12px",
                padding="0 16px",
                font_weight="500",
            ),
            rx.box(
                flex="1",
                height="1px",
                background=COLORS["border_light"],
            ),
            display="flex",
            align_items="center",
            margin="20px 0",
        ),
        
        # Guest Button
        rx.button(
            rx.icon(tag="user", size=16),
            rx.text("Doorgaan als gast", margin_left="8px"),
            width="100%",
            padding="14px",
            min_height="48px",
            background="transparent",
            color=COLORS["primary_green"],
            border=f"1.5px solid {COLORS['primary_green']}",
            border_radius=RADIUS["lg"],
            cursor="pointer",
            font_size="14px",
            font_weight="500",
            on_click=AuthState.continue_as_guest,
            transition=TRANSITIONS["fast"],
            _hover={
                "background": COLORS["light_green"],
                "border_color": COLORS["dark_green"],
            },
        ),
        
        # Guest info
        rx.text(
            "Gastmodus: beperkte functies",
            color=COLORS["text_tertiary"],
            font_size="11px",
            text_align="center",
            margin_top="8px",
        ),
        
        width=["100%", "100%", MODAL_CONFIG["right_panel_width"]],
        padding=["24px", "32px", "40px"],
        display="flex",
        flex_direction="column",
        overflow_y="auto",
    )


# ============================================================================
# TAB SELECTOR
# ============================================================================


def _tab_selector() -> rx.Component:
    """Login/Signup tab selector with pill design."""
    return rx.box(
        rx.box(
            # Login Tab
            rx.box(
                rx.text(
                    "Inloggen",
                    font_size="14px",
                    font_weight="600",
                    color=rx.cond(
                        AuthState.auth_mode == "login",
                        "white",
                        COLORS["text_secondary"]
                    ),
                ),
                padding="10px 0",
                cursor="pointer",
                border_radius=RADIUS["lg"],
                background=rx.cond(
                    AuthState.auth_mode == "login",
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    "transparent"
                ),
                box_shadow=rx.cond(
                    AuthState.auth_mode == "login",
                    SHADOWS["primary_sm"],
                    "none"
                ),
                flex="1",
                text_align="center",
                transition=TRANSITIONS["fast"],
                on_click=lambda: AuthState.set_auth_mode("login"),
            ),
            
            # Signup Tab
            rx.box(
                rx.text(
                    "Registreren",
                    font_size="14px",
                    font_weight="600",
                    color=rx.cond(
                        AuthState.auth_mode == "signup",
                        "white",
                        COLORS["text_secondary"]
                    ),
                ),
                padding="10px 0",
                cursor="pointer",
                border_radius=RADIUS["lg"],
                background=rx.cond(
                    AuthState.auth_mode == "signup",
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    "transparent"
                ),
                box_shadow=rx.cond(
                    AuthState.auth_mode == "signup",
                    SHADOWS["primary_sm"],
                    "none"
                ),
                flex="1",
                text_align="center",
                transition=TRANSITIONS["fast"],
                on_click=lambda: AuthState.set_auth_mode("signup"),
            ),
            
            display="flex",
            gap="4px",
        ),
        background=COLORS["light_gray"],
        padding="4px",
        border_radius=RADIUS["xl"],
        margin_bottom="20px",
    )


# ============================================================================
# LOGIN FORM
# ============================================================================


def _login_form() -> rx.Component:
    """Login form with email and password fields."""
    return rx.box(
        # Email Field
        rx.box(
            rx.text(
                "E-mailadres",
                font_size="13px",
                font_weight="500",
                color=COLORS["text_primary"],
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="mail",
                    size=18,
                    color=COLORS["text_tertiary"],
                    position="absolute",
                    left="14px",
                    top="50%",
                    transform="translateY(-50%)",
                    z_index="1",
                ),
                rx.input(
                    value=AuthState.login_email,
                    on_change=AuthState.set_login_email,
                    placeholder="jouw@email.com",
                    type="email",
                    width="100%",
                    padding="14px 14px 14px 42px",
                    border=rx.cond(
                        AuthState.email_error != "",
                        f"1.5px solid {COLORS['error']}",
                        f"1.5px solid {COLORS['border']}"
                    ),
                    border_radius=RADIUS["lg"],
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=COLORS["text_primary"],
                    background="white",
                    outline="none",
                    transition=TRANSITIONS["fast"],
                    _focus={
                        "border_color": COLORS["primary_green"],
                        "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.12)",
                    },
                    _placeholder={"color": COLORS["text_tertiary"]},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.email_error != "",
                rx.hstack(
                    rx.icon("alert-circle", size=12, color=COLORS["error"]),
                    rx.text(
                        AuthState.email_error,
                        color=COLORS["error"],
                        font_size="12px",
                    ),
                    spacing="1",
                    margin_top="6px",
                ),
            ),
            margin_bottom="16px",
        ),
        
        # Password Field
        rx.box(
            rx.text(
                "Wachtwoord",
                font_size="13px",
                font_weight="500",
                color=COLORS["text_primary"],
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="lock",
                    size=18,
                    color=COLORS["text_tertiary"],
                    position="absolute",
                    left="14px",
                    top="50%",
                    transform="translateY(-50%)",
                    z_index="1",
                ),
                rx.input(
                    value=AuthState.login_password,
                    on_change=AuthState.set_login_password,
                    placeholder="••••••••",
                    type=rx.cond(AuthState.show_login_password, "text", "password"),
                    width="100%",
                    padding="14px 42px 14px 42px",
                    border=rx.cond(
                        AuthState.password_error != "",
                        f"1.5px solid {COLORS['error']}",
                        f"1.5px solid {COLORS['border']}"
                    ),
                    border_radius=RADIUS["lg"],
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=COLORS["text_primary"],
                    background="white",
                    outline="none",
                    transition=TRANSITIONS["fast"],
                    _focus={
                        "border_color": COLORS["primary_green"],
                        "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.12)",
                    },
                    _placeholder={"color": COLORS["text_tertiary"]},
                ),
                rx.box(
                    rx.icon(
                        tag=rx.cond(AuthState.show_login_password, "eye-off", "eye"),
                        size=18,
                        color=COLORS["text_tertiary"],
                    ),
                    position="absolute",
                    right="14px",
                    top="50%",
                    transform="translateY(-50%)",
                    cursor="pointer",
                    on_click=AuthState.toggle_login_password,
                    padding="4px",
                    border_radius=RADIUS["sm"],
                    transition=TRANSITIONS["fast"],
                    _hover={
                        "color": COLORS["primary_green"],
                        "background": COLORS["light_green"],
                    },
                    z_index="1",
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.password_error != "",
                rx.hstack(
                    rx.icon("alert-circle", size=12, color=COLORS["error"]),
                    rx.text(
                        AuthState.password_error,
                        color=COLORS["error"],
                        font_size="12px",
                    ),
                    spacing="1",
                    margin_top="6px",
                ),
            ),
            margin_bottom="16px",
        ),
        
        # Remember me & Forgot password row
        rx.box(
            rx.box(
                rx.checkbox(
                    checked=AuthState.remember_me,
                    on_change=lambda _: AuthState.toggle_remember_me(),
                ),
                rx.text(
                    "Onthoud mij",
                    font_size="13px",
                    color=COLORS["text_secondary"],
                    margin_left="8px",
                ),
                display="flex",
                align_items="center",
            ),
            rx.text(
                "Wachtwoord vergeten?",
                font_size="13px",
                color=COLORS["primary_green"],
                cursor="pointer",
                on_click=AuthState.request_password_reset,
                font_weight="500",
                transition=TRANSITIONS["fast"],
                _hover={"color": COLORS["dark_green"]},
            ),
            display="flex",
            justify_content="space-between",
            align_items="center",
            margin_bottom="20px",
        ),
        
        # Submit Button
        rx.button(
            rx.cond(
                AuthState.auth_loading,
                rx.box(
                    rx.icon("loader-2", size=18, class_name="animate-spin"),
                    rx.text("Bezig...", margin_left="8px"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    rx.icon(tag="log-in", size=18),
                    rx.text("Inloggen", margin_left="8px"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            width="100%",
            padding="14px",
            min_height="50px",
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            color="white",
            border="none",
            border_radius=RADIUS["lg"],
            cursor=rx.cond(AuthState.auth_loading, "not-allowed", "pointer"),
            font_size="15px",
            font_weight="600",
            disabled=AuthState.auth_loading,
            on_click=AuthState.login,
            box_shadow=SHADOWS["primary_sm"],
            transition=TRANSITIONS["fast"],
            _hover={
                "transform": "translateY(-1px)",
                "box_shadow": SHADOWS["primary_md"],
            },
            _active={
                "transform": "translateY(0)",
            },
        ),
        
        width="100%",
    )


# ============================================================================
# SIGNUP FORM
# ============================================================================


def _signup_form() -> rx.Component:
    """Signup form."""
    return rx.box(
        # Name Field
        rx.box(
            rx.text(
                "Naam",
                font_size="13px",
                font_weight="500",
                color=COLORS["text_primary"],
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="user",
                    size=18,
                    color=COLORS["text_secondary"],
                    position="absolute",
                    left="12px",
                    top="50%",
                    transform="translateY(-50%)",
                ),
                rx.input(
                    value=AuthState.signup_name,
                    on_change=AuthState.set_signup_name,
                    placeholder="Je naam",
                    width="100%",
                    padding="14px 14px 14px 40px",
                    border=rx.cond(
                        AuthState.name_error != "",
                        "1.5px solid #dc2626",
                        f"1.5px solid {COLORS['border']}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color="#000000",
                    background="white",
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": COLORS["text_secondary"]},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.name_error != "",
                rx.text(
                    AuthState.name_error,
                    color="#dc2626",
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="12px",
        ),
        
        # Email Field
        rx.box(
            rx.text(
                "E-mailadres",
                font_size="13px",
                font_weight="500",
                color=COLORS["text_primary"],
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="mail",
                    size=18,
                    color=COLORS["text_secondary"],
                    position="absolute",
                    left="12px",
                    top="50%",
                    transform="translateY(-50%)",
                ),
                rx.input(
                    value=AuthState.signup_email,
                    on_change=AuthState.set_signup_email,
                    placeholder="jouw@email.com",
                    type="email",
                    width="100%",
                    padding="14px 14px 14px 40px",
                    border=rx.cond(
                        AuthState.email_error != "",
                        "1.5px solid #dc2626",
                        f"1.5px solid {COLORS['border']}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color="#000000",
                    background="white",
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": COLORS["text_secondary"]},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.email_error != "",
                rx.text(
                    AuthState.email_error,
                    color="#dc2626",
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="12px",
        ),
        
        # Password Field
        rx.box(
            rx.text(
                "Wachtwoord",
                font_size="13px",
                font_weight="500",
                color=COLORS["text_primary"],
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="lock",
                    size=18,
                    color=COLORS["text_secondary"],
                    position="absolute",
                    left="12px",
                    top="50%",
                    transform="translateY(-50%)",
                ),
                rx.input(
                    value=AuthState.signup_password,
                    on_change=AuthState.set_signup_password,
                    placeholder="Minimaal 8 karakters",
                    type=rx.cond(AuthState.show_signup_password, "text", "password"),
                    width="100%",
                    padding="14px 40px 14px 40px",
                    border=rx.cond(
                        AuthState.password_error != "",
                        "1.5px solid #dc2626",
                        f"1.5px solid {COLORS['border']}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color="#000000",
                    background="white",
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": COLORS["text_secondary"]},
                ),
                rx.icon(
                    tag=rx.cond(AuthState.show_signup_password, "eye-off", "eye"),
                    size=18,
                    color=COLORS["text_secondary"],
                    position="absolute",
                    right="12px",
                    top="50%",
                    transform="translateY(-50%)",
                    cursor="pointer",
                    on_click=AuthState.toggle_signup_password,
                    _hover={"color": COLORS["primary_green"]},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.password_error != "",
                rx.text(
                    AuthState.password_error,
                    color="#dc2626",
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="12px",
        ),
        
        # Confirm Password Field
        rx.box(
            rx.text(
                "Bevestig wachtwoord",
                font_size="13px",
                font_weight="500",
                color=COLORS["text_primary"],
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="lock",
                    size=18,
                    color=COLORS["text_secondary"],
                    position="absolute",
                    left="12px",
                    top="50%",
                    transform="translateY(-50%)",
                ),
                rx.input(
                    value=AuthState.signup_confirm_password,
                    on_change=AuthState.set_signup_confirm_password,
                    placeholder="Herhaal wachtwoord",
                    type=rx.cond(AuthState.show_confirm_password, "text", "password"),
                    width="100%",
                    padding="14px 40px 14px 40px",
                    border=rx.cond(
                        AuthState.confirm_password_error != "",
                        "1.5px solid #dc2626",
                        f"1.5px solid {COLORS['border']}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color="#000000",
                    background="white",
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": COLORS["text_secondary"]},
                ),
                rx.icon(
                    tag=rx.cond(AuthState.show_confirm_password, "eye-off", "eye"),
                    size=18,
                    color=COLORS["text_secondary"],
                    position="absolute",
                    right="12px",
                    top="50%",
                    transform="translateY(-50%)",
                    cursor="pointer",
                    on_click=AuthState.toggle_confirm_password,
                    _hover={"color": COLORS["primary_green"]},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.confirm_password_error != "",
                rx.text(
                    AuthState.confirm_password_error,
                    color="#dc2626",
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="20px",
        ),
        
        # Submit Button
        rx.button(
            rx.cond(
                AuthState.auth_loading,
                rx.box(
                    rx.spinner(size="1"),
                    rx.text("Bezig...", margin_left="8px"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    rx.icon(tag="user-plus", size=18),
                    rx.text("Account aanmaken", margin_left="8px"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            width="100%",
            padding="14px",
            min_height="50px",
            background=COLORS["primary_green"],
            color="white",
            border="none",
            border_radius="8px",
            cursor=rx.cond(AuthState.auth_loading, "not-allowed", "pointer"),
            font_size="15px",
            font_weight="600",
            disabled=AuthState.auth_loading,
            on_click=AuthState.signup,
            _hover={"background": COLORS["dark_green"]},
        ),
        
        width="100%",
    )


def toast_notification() -> rx.Component:
    """Toast notification component."""
    return rx.cond(
        AuthState.show_toast,
        rx.box(
            rx.box(
                rx.cond(
                    AuthState.toast_type == "success",
                    rx.icon(tag="circle-check", size=20, color="white"),
                    rx.cond(
                        AuthState.toast_type == "error",
                        rx.icon(tag="circle-alert", size=20, color="white"),
                        rx.icon(tag="info", size=20, color="white"),
                    ),
                ),
                rx.text(
                    AuthState.toast_message,
                    color="white",
                    font_size="14px",
                    margin_left="12px",
                ),
                rx.icon(
                    tag="x",
                    size=16,
                    color="white",
                    cursor="pointer",
                    margin_left="auto",
                    on_click=AuthState.hide_toast,
                ),
                display="flex",
                align_items="center",
                width="100%",
            ),
            position="fixed",
            bottom="24px",
            right="24px",
            padding="16px 20px",
            background=rx.cond(
                AuthState.toast_type == "success",
                COLORS["primary_green"],
                rx.cond(
                    AuthState.toast_type == "error",
                    "#dc2626",
                    "#3b82f6",
                ),
            ),
            border_radius="12px",
            box_shadow="0 10px 25px rgba(0,0,0,0.2)",
            z_index="9999",
            min_width="300px",
            max_width="400px",
        ),
    )


