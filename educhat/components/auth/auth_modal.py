"""
Authentication Modal Component - Professional Implementation
Modern, responsive login/signup modal with proper validation feedback,
loading states, and accessibility features.
"""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.styles.theme import COLORS, RADIUS, SHADOWS, TRANSITIONS, T
from educhat.utils.translations import t


def tx(key: str) -> rx.Var:
    """Reactive translation helper for auth modal.
    
    Returns a reactive var that updates when language changes.
    """
    return rx.cond(
        AuthState.is_dutch,
        t(key, "nl"),
        t(key, "en"),
    )


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
        "color": T.text_primary,
        "background": T.bg_input,
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
                background=T.overlay,
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
                        color=T.text_secondary,
                    ),
                    position="absolute",
                    top="16px",
                    right="16px",
                    padding="10px",
                    cursor="pointer",
                    border_radius=RADIUS["full"],
                    background=T.bg_card,
                    box_shadow=SHADOWS["sm"],
                    z_index="10",
                    on_click=AuthState.close_auth_modal,
                    transition=TRANSITIONS["fast"],
                    _hover={
                        "background": T.bg_hover,
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
                max_height=["95vh", "90vh", "720px"],
                background=rx.color_mode_cond(
                    light="#FFFFFF",
                    dark="#111217"
                ),
                border_radius=RADIUS["2xl"],
                box_shadow=SHADOWS["2xl"],
                overflow="hidden",
                display="flex",
                z_index="1000",
                class_name="animate-scaleIn auth-modal-box",
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
                    color=T.text_on_primary,
                ),
                padding="16px",
                background=T.primary_light,
                border_radius=RADIUS["2xl"],
                margin_bottom="24px",
                box_shadow=T.shadow_primary,
            ),
            
            # Title
            rx.heading(
                tx("auth_welcome"),
                size="7",
                color=T.text_on_primary,
                margin_bottom="12px",
                font_weight="700",
                letter_spacing="-0.02em",
            ),
            
            # Subtitle
            rx.text(
                tx("auth_subtitle"),
                color=T.text_on_primary,
                font_size="15px",
                margin_bottom="32px",
                line_height="1.6",
            ),
            
            # Benefits list
            rx.box(
                _benefit_item(tx("benefit_direct_answers")),
                _benefit_item(tx("benefit_study_material")),
                _benefit_item(tx("benefit_24_7")),
                _benefit_item(tx("benefit_free")),
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
            "background": T.primary_muted,
            "border_radius": "50%",
        },
        _after={
            "content": "''",
            "position": "absolute",
            "bottom": "-30px",
            "left": "-30px",
            "width": "100px",
            "height": "100px",
            "background": T.primary_muted,
            "border_radius": "50%",
        },
    )


def _benefit_item(text) -> rx.Component:
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
            background=T.text_on_primary,
            border_radius=RADIUS["full"],
            flex_shrink="0",
        ),
        rx.text(
            text,
            color=T.text_on_primary,
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
                    size=32,
                    color=COLORS["primary_green"],
                ),
                rx.text(
                    "EduChat",
                    font_size="26px",
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
                    tx("auth_login_title"),
                    tx("auth_signup_title"),
                ),
                color=T.text_secondary,
                font_size="14px",
                line_height="1.4",
            ),
            margin_bottom="20px",
        ),
        
        # Tab Selector
        _tab_selector(),
        
        # Success Message
        rx.cond(
            AuthState.auth_success != "",
            rx.box(
                rx.box(
                    rx.icon(tag="check", size=16, color=T.success),
                    width="24px",
                    height="24px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    background=T.success_light,
                    border_radius=RADIUS["full"],
                    flex_shrink="0",
                ),
                rx.text(
                    AuthState.auth_success,
                    color=COLORS["primary_green"],
                    font_size="13px",
                    margin_left="10px",
                    font_weight="500",
                ),
                display="flex",
                align_items="center",
                padding="14px 16px",
                background=T.success_light,
                border=f"1px solid {COLORS['primary_green']}30",
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
                        rx.icon(tag="triangle-alert", size=16, color=T.error),
                        width="24px",
                        height="24px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background=T.error_light,
                        border_radius=RADIUS["full"],
                        flex_shrink="0",
                    ),
                    rx.text(
                        AuthState.auth_error,
                        color=T.error,
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
                background=T.error_light,
                border=f"1px solid {T.error}30",
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
                background=T.border_light,
            ),
            rx.text(
                "of",
                color=T.text_tertiary,
                font_size="12px",
                padding="0 16px",
                font_weight="500",
            ),
            rx.box(
                flex="1",
                height="1px",
                background=T.border_light,
            ),
            display="flex",
            align_items="center",
            margin="16px 0",
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
                "background": COLORS["primary_light"],
                "border_color": COLORS["dark_green"],
            },
        ),
        
        # Guest info
        rx.text(
            "Gastmodus: beperkte functies",
            color=T.text_tertiary,
            font_size="11px",
            text_align="center",
            margin_top="8px",
        ),
        
        width=["100%", "100%", MODAL_CONFIG["right_panel_width"]],
        padding=["24px 18px", "28px 24px", "32px 28px"],
        display="flex",
        flex_direction="column",
        overflow_y="auto",
        background=T.bg_primary,
        class_name="auth-form-panel",
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
                    tx("auth_login_btn"),
                    font_size="14px",
                    font_weight="600",
                    color=rx.cond(
                        AuthState.auth_mode == "login",
                        "white",
                        T.text_secondary
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
                    tx("auth_signup_btn"),
                    font_size="14px",
                    font_weight="600",
                    color=rx.cond(
                        AuthState.auth_mode == "signup",
                        "white",
                        T.text_secondary
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
        background=T.bg_tertiary,
        padding="4px",
        border_radius=RADIUS["xl"],
        margin_bottom="20px",
    )


# ============================================================================
# GOOGLE LOGIN BUTTON
# ============================================================================


def _google_login_button() -> rx.Component:
    """Google OAuth login button."""
    return rx.box(
        # Divider with "of" text
        rx.box(
            rx.box(
                height="1px",
                background=T.border,
                flex="1",
            ),
            rx.text(
                "of",
                font_size="13px",
                color=T.text_secondary,
                padding="0 12px",
            ),
            rx.box(
                height="1px",
                background=T.border,
                flex="1",
            ),
            display="flex",
            align_items="center",
            margin="20px 0",
        ),
        
        # Google Button
        rx.button(
            rx.cond(
                AuthState.google_auth_loading,
                rx.box(
                    rx.icon("loader-circle", size=18, class_name="animate-spin"),
                    rx.text("Bezig...", margin_left="8px"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    # Google icon (using a circle with "G")
                    rx.box(
                        rx.html(
                            """<svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
                                <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z" fill="#4285F4"/>
                                <path d="M9.003 18c2.43 0 4.467-.806 5.956-2.18L12.05 13.56c-.806.54-1.837.86-3.047.86-2.344 0-4.328-1.584-5.036-3.711H.96v2.332C2.438 15.983 5.482 18 9.003 18z" fill="#34A853"/>
                                <path d="M3.964 10.712c-.18-.54-.282-1.117-.282-1.71 0-.593.102-1.17.282-1.71V4.96H.957C.347 6.175 0 7.55 0 9.002c0 1.452.348 2.827.957 4.042l3.007-2.332z" fill="#FBBC05"/>
                                <path d="M9.003 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.464.891 11.426 0 9.003 0 5.482 0 2.438 2.017.96 4.958L3.967 7.29c.708-2.127 2.692-3.71 5.036-3.71z" fill="#EA4335"/>
                            </svg>"""
                        ),
                        display="inline-block",
                        margin_right="10px",
                    ),
                    rx.text("Doorgaan met Google"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            width="100%",
            padding="14px",
            min_height="50px",
            background=T.bg_card,
            color=T.text_primary,
            border=f"1.5px solid {T.border}",
            border_radius=RADIUS["lg"],
            cursor=rx.cond(AuthState.google_auth_loading, "not-allowed", "pointer"),
            font_size="15px",
            font_weight="600",
            disabled=AuthState.google_auth_loading,
            on_click=AuthState.google_signin,
            transition=TRANSITIONS["fast"],
            _hover={
                "background": T.bg_hover,
                "border_color": COLORS["primary_green"],
            },
        ),
        
        width="100%",
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
                color=T.text_primary,
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="mail",
                    size=18,
                    color=T.text_tertiary,
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
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius=RADIUS["lg"],
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=T.text_primary,
                    background=T.bg_input,
                    outline="none",
                    transition=TRANSITIONS["fast"],
                    _focus={
                        "border_color": COLORS["primary_green"],
                        "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.12)",
                    },
                    _placeholder={"color": T.text_tertiary},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.email_error != "",
                rx.hstack(
                    rx.icon("circle-alert", size=12, color=T.error),
                    rx.text(
                        AuthState.email_error,
                        color=T.error,
                        font_size="12px",
                    ),
                    spacing="1",
                    margin_top="6px",
                ),
            ),
            margin_bottom="14px",
        ),
        
        # Password Field
        rx.box(
            rx.text(
                "Wachtwoord",
                font_size="13px",
                font_weight="500",
                color=T.text_primary,
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="lock",
                    size=18,
                    color=T.text_tertiary,
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
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius=RADIUS["lg"],
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=T.text_primary,
                    background=T.bg_input,
                    outline="none",
                    transition=TRANSITIONS["fast"],
                    _focus={
                        "border_color": COLORS["primary_green"],
                        "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.12)",
                    },
                    _placeholder={"color": T.text_tertiary},
                ),
                rx.box(
                    rx.icon(
                        tag=rx.cond(AuthState.show_login_password, "eye-off", "eye"),
                        size=18,
                        color=T.text_tertiary,
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
                        "background": COLORS["primary_light"],
                    },
                    z_index="1",
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.password_error != "",
                rx.hstack(
                    rx.icon("circle-alert", size=12, color=T.error),
                    rx.text(
                        AuthState.password_error,
                        color=T.error,
                        font_size="12px",
                    ),
                    spacing="1",
                    margin_top="6px",
                ),
            ),
            margin_bottom="14px",
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
                    color=T.text_secondary,
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
            margin_bottom="16px",
        ),
        
        # Submit Button
        rx.button(
            rx.cond(
                AuthState.auth_loading,
                rx.box(
                    rx.icon("loader-circle", size=18, class_name="animate-spin"),
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
        
        # Google Login Button
        _google_login_button(),
        
        width="100%",
    )


# ============================================================================
# SIGNUP FORM
# ============================================================================


def _signup_form() -> rx.Component:
    """Signup form."""
    return rx.box(
        # First Name Field
        rx.box(
            rx.text(
                "Voornaam",
                font_size="13px",
                font_weight="500",
                color=T.text_primary,
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="user",
                    size=18,
                    color=T.text_secondary,
                    position="absolute",
                    left="12px",
                    top="50%",
                    transform="translateY(-50%)",
                ),
                rx.input(
                    value=AuthState.signup_firstname,
                    on_change=AuthState.set_signup_firstname,
                    placeholder="Je voornaam",
                    width="100%",
                    padding="14px 14px 14px 40px",
                    border=rx.cond(
                        AuthState.firstname_error != "",
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=T.text_primary,
                    background=T.bg_input,
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": T.text_secondary},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.firstname_error != "",
                rx.text(
                    AuthState.firstname_error,
                    color=T.error,
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="10px",
        ),
        
        # Last Name Field
        rx.box(
            rx.text(
                "Achternaam",
                font_size="13px",
                font_weight="500",
                color=T.text_primary,
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="user",
                    size=18,
                    color=T.text_secondary,
                    position="absolute",
                    left="12px",
                    top="50%",
                    transform="translateY(-50%)",
                ),
                rx.input(
                    value=AuthState.signup_lastname,
                    on_change=AuthState.set_signup_lastname,
                    placeholder="Je achternaam",
                    width="100%",
                    padding="14px 14px 14px 40px",
                    border=rx.cond(
                        AuthState.lastname_error != "",
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=T.text_primary,
                    background=T.bg_input,
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": T.text_secondary},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.lastname_error != "",
                rx.text(
                    AuthState.lastname_error,
                    color=T.error,
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="10px",
        ),
        
        # Email Field
        rx.box(
            rx.text(
                "E-mailadres",
                font_size="13px",
                font_weight="500",
                color=T.text_primary,
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="mail",
                    size=18,
                    color=T.text_secondary,
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
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=T.text_primary,
                    background=T.bg_input,
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": T.text_secondary},
                ),
                position="relative",
            ),
            rx.cond(
                AuthState.email_error != "",
                rx.text(
                    AuthState.email_error,
                    color=T.error,
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="10px",
        ),
        
        # Password Field
        rx.box(
            rx.text(
                "Wachtwoord",
                font_size="13px",
                font_weight="500",
                color=T.text_primary,
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="lock",
                    size=18,
                    color=T.text_secondary,
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
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=T.text_primary,
                    background=T.bg_input,
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": T.text_secondary},
                ),
                rx.icon(
                    tag=rx.cond(AuthState.show_signup_password, "eye-off", "eye"),
                    size=18,
                    color=T.text_secondary,
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
                    color=T.error,
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="10px",
        ),
        
        # Confirm Password Field
        rx.box(
            rx.text(
                "Bevestig wachtwoord",
                font_size="13px",
                font_weight="500",
                color=T.text_primary,
                margin_bottom="6px",
            ),
            rx.box(
                rx.icon(
                    tag="lock",
                    size=18,
                    color=T.text_secondary,
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
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="48px",
                    color=T.text_primary,
                    background=T.bg_input,
                    outline="none",
                    _focus={"border_color": COLORS["primary_green"], "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)"},
                    _placeholder={"color": T.text_secondary},
                ),
                rx.icon(
                    tag=rx.cond(AuthState.show_confirm_password, "eye-off", "eye"),
                    size=18,
                    color=T.text_secondary,
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
                    color=T.error,
                    font_size="12px",
                    margin_top="4px",
                ),
            ),
            margin_bottom="16px",
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
        
        # Google Login Button
        _google_login_button(),
        
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
                    rx.icon(tag="circle-check-big", size=20, color="white"),
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


