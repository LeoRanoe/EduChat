"""
Authentication Modal Component - Modern Professional Implementation
Sleek, responsive login/signup modal with:
- Glass morphism design
- Smooth animations and transitions
- Real-time password strength feedback
- Email confirmation prompts
- Accessibility features
- Dark mode support
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
    "max_height": ["95vh", "90vh", "680px"],
    "left_panel_width": "42%",
    "right_panel_width": "58%",
}

INPUT_STYLES = {
    "height": "52px",
    "font_size": "15px",
    "border_radius": RADIUS["xl"],
    "transition": TRANSITIONS["normal"],
}


# ============================================================================
# MAIN MODAL COMPONENT
# ============================================================================

def auth_modal() -> rx.Component:
    """Main authentication modal component with modern glass morphism design."""
    return rx.cond(
        AuthState.show_auth_modal,
        rx.box(
            # Simplified Backdrop
            rx.box(
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                background="rgba(0, 0, 0, 0.5)",
                z_index="999",
                on_click=AuthState.close_auth_modal,
            ),
            
            # Modal Container with glass effect
            rx.box(
                # Modern Close Button
                rx.box(
                    rx.icon(
                        tag="x",
                        size=20,
                        color=T.text_secondary,
                    ),
                    position="absolute",
                    top="20px",
                    right="20px",
                    width="40px",
                    height="40px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    cursor="pointer",
                    border_radius=RADIUS["full"],
                    background=rx.color_mode_cond(
                        light="rgba(255, 255, 255, 0.9)",
                        dark="rgba(30, 30, 35, 0.9)"
                    ),
                    border=f"1px solid {T.border_light}",
                    box_shadow=SHADOWS["sm"],
                    z_index="10",
                    on_click=AuthState.close_auth_modal,
                    transition=TRANSITIONS["fast"],
                    _hover={
                        "background": T.bg_hover,
                        "transform": "scale(1.05)",
                        "border_color": T.error,
                    },
                ),
                
                # Two-column layout
                rx.box(
                    # Left: Enhanced Branding (hidden on mobile)
                    _left_panel(),
                    
                    # Right: Form Panel
                    _right_panel(),
                    
                    display="flex",
                    width="100%",
                    height="100%",
                ),
                
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%) translateZ(0)",
                width=MODAL_CONFIG["width"],
                max_width="900px",
                max_height=["95vh", "90vh", "800px"],
                background=rx.color_mode_cond(
                    light="white",
                    dark="rgba(17, 18, 23, 1)"
                ),
                border=f"1px solid {T.border}",
                border_radius=RADIUS["xl"],
                box_shadow=SHADOWS["lg"],
                overflow="hidden",
                display="flex",
                z_index="1000",
                class_name="auth-modal-box",
            ),
        ),
    )


# ============================================================================
# LEFT PANEL (BRANDING)
# ============================================================================


def _left_panel() -> rx.Component:
    """Left branding panel with modern gradient and floating elements."""
    return rx.box(
        rx.box(
            # Static Logo
            rx.box(
                rx.box(
                    rx.icon(
                        tag="graduation-cap",
                        size=56,
                        color="white",
                    ),
                    padding="20px",
                    background="rgba(255, 255, 255, 0.2)",
                    border="2px solid rgba(255, 255, 255, 0.3)",
                    border_radius=RADIUS["2xl"],
                    box_shadow="0 4px 12px rgba(0, 0, 0, 0.1)",
                ),
                margin_bottom="32px",
                display="flex",
                justify_content="center",
            ),
            
            # Modern Title
            rx.box(
                rx.heading(
                    "Welkom bij",
                    size="5",
                    color="rgba(255, 255, 255, 0.95)",
                    margin_bottom="4px",
                    font_weight="500",
                    letter_spacing="-0.01em",
                ),
                rx.heading(
                    "EduChat",
                    size="8",
                    color="white",
                    margin_bottom="16px",
                    font_weight="800",
                    letter_spacing="-0.02em",
                ),
                text_align="center",
            ),
            
            # Subtitle with better spacing
            rx.text(
                "Jouw AI-assistent voor Surinaams onderwijs",
                color="rgba(255, 255, 255, 0.9)",
                font_size="16px",
                margin_bottom="40px",
                line_height="1.6",
                text_align="center",
                font_weight="400",
            ),
            
            # Modern Benefits list with cards
            rx.box(
                _modern_benefit_card("sparkles", "Directe antwoorden", "Op al je vragen over onderwijs"),
                _modern_benefit_card("book-open", "Studiemateriaal", "Persoonlijk voor jou samengesteld"),
                _modern_benefit_card("clock", "24/7 beschikbaar", "Leer wanneer het jou uitkomt"),
                _modern_benefit_card("heart", "Gratis te gebruiken", "Geen kosten, geen verplichtingen"),
                display="flex",
                flex_direction="column",
                gap="12px",
            ),
            
            padding=["32px 24px", "40px 32px", "48px 40px"],
            display="flex",
            flex_direction="column",
            justify_content="center",
            height="100%",
        ),
        
        width=MODAL_CONFIG["left_panel_width"],
        background=f"linear-gradient(135deg, #10A37F 0%, #0D8F6F 50%, #0A7B5F 100%)",
        display=["none", "none", "flex"],
        position="relative",
        overflow="hidden",
        # Modern decorative elements
        _before={
            "content": "''",
            "position": "absolute",
            "top": "-100px",
            "right": "-100px",
            "width": "250px",
            "height": "250px",
            "background": "radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)",
            "border_radius": "50%",
            "animation": "pulse 4s ease-in-out infinite",
        },
        _after={
            "content": "''",
            "position": "absolute",
            "bottom": "-80px",
            "left": "-80px",
            "width": "200px",
            "height": "200px",
            "background": "radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%)",
            "border_radius": "50%",
            "animation": "pulse 5s ease-in-out infinite reverse",
        },
    )


def _modern_benefit_card(icon: str, title: str, description: str) -> rx.Component:
    """Modern benefit card with icon, title and description."""
    return rx.box(
        rx.box(
            rx.icon(
                tag=icon,
                size=20,
                color=COLORS["primary_green"],
            ),
            width="40px",
            height="40px",
            display="flex",
            align_items="center",
            justify_content="center",
            background="white",
            border_radius=RADIUS["lg"],
            flex_shrink="0",
            box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
        ),
        rx.box(
            rx.text(
                title,
                color="white",
                font_size="14px",
                font_weight="600",
                margin_bottom="2px",
            ),
            rx.text(
                description,
                color="rgba(255, 255, 255, 0.8)",
                font_size="12px",
                line_height="1.4",
            ),
        ),
        display="flex",
        align_items="center",
        gap="16px",
        padding="16px",
        background="rgba(255, 255, 255, 0.15)",
        border="1px solid rgba(255, 255, 255, 0.2)",
        border_radius=RADIUS["lg"],
        transition=TRANSITIONS["fast"],
        _hover={
            "background": "rgba(255, 255, 255, 0.2)",
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
    """Right panel with modern form design."""
    return rx.box(
        # Compact Header with logo (visible on mobile)
        rx.box(
            rx.box(
                rx.box(
                    rx.icon(
                        tag="graduation-cap",
                        size=28,
                        color=COLORS["primary_green"],
                    ),
                    width="48px",
                    height="48px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    background=rx.color_mode_cond(
                        light=f"{COLORS['primary_light']}",
                        dark=f"rgba(16, 163, 127, 0.12)"
                    ),
                    border_radius=RADIUS["xl"],
                    margin_bottom="12px",
                ),
                rx.heading(
                    "EduChat",
                    size="6",
                    font_weight="700",
                    color=T.text_primary,
                    letter_spacing="-0.02em",
                    margin_bottom="4px",
                ),
                rx.text(
                    rx.cond(
                        AuthState.auth_mode == "login",
                        "Log in op je account",
                        "Maak een nieuw account",
                    ),
                    color=T.text_secondary,
                    font_size="14px",
                    line_height="1.4",
                ),
                text_align="center",
            ),
            margin_bottom="28px",
            display=["block", "block", "none"],  # Only show on mobile
        ),
        
        # Enhanced Tab Selector
        _modern_tab_selector(),
        
        # Success Message with modern styling
        rx.cond(
            AuthState.auth_success != "",
            rx.box(
                rx.box(
                    rx.icon(tag="check_check", size=18, color=T.success),
                    width="32px",
                    height="32px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    background=T.success_light,
                    border_radius=RADIUS["full"],
                    flex_shrink="0",
                ),
                rx.text(
                    AuthState.auth_success,
                    color=T.success,
                    font_size="14px",
                    font_weight="500",
                    line_height="1.5",
                ),
                display="flex",
                align_items="center",
                gap="12px",
                padding="16px 18px",
                background=T.success_light,
                border=f"1px solid {rx.color_mode_cond(light=COLORS['success'], dark='rgba(52, 211, 153, 0.3)')}",
                border_radius=RADIUS["lg"],
                margin_bottom="20px",
            ),
        ),
        
        # Error Message with modern styling
        rx.cond(
            AuthState.auth_error != "",
            rx.box(
                rx.box(
                    rx.box(
                        rx.icon(tag="triangle_alert", size=18, color=T.error),
                        width="32px",
                        height="32px",
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
                        font_size="14px",
                        font_weight="500",
                        line_height="1.5",
                    ),
                    display="flex",
                    align_items="center",
                    gap="12px",
                ),
                
                # Enhanced "Resend confirmation" button
                rx.cond(
                    AuthState.email_needs_confirmation,
                    rx.button(
                        rx.cond(
                            AuthState.resending_confirmation,
                            rx.box(
                                rx.spinner(size="2", color="white"),
                                rx.text("Verzenden...", margin_left="8px", font_size="13px", font_weight="500"),
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            rx.box(
                                rx.icon(tag="mail-check", size=16),
                                rx.text("Bevestigingsmail opnieuw verzenden", margin_left="8px", font_size="13px", font_weight="500"),
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                        ),
                        width="100%",
                        padding="12px 16px",
                        margin_top="14px",
                        background=COLORS["primary_green"],
                        color="white",
                        border="none",
                        border_radius=RADIUS["lg"],
                        cursor=rx.cond(AuthState.resending_confirmation, "not-allowed", "pointer"),
                        font_weight="500",
                        min_height="44px",
                        on_click=AuthState.resend_confirmation_email,
                        transition=TRANSITIONS["normal"],
                        _hover={"background": COLORS["dark_green"], "transform": "translateY(-1px)"},
                        _active={"transform": "translateY(0)"},
                        disabled=AuthState.resending_confirmation,
                    ),
                ),
                
                padding="16px 18px",
                background=T.error_light,
                border=f"1px solid {rx.color_mode_cond(light=T.error, dark='rgba(248, 113, 113, 0.3)')}",
                border_radius=RADIUS["lg"],
                margin_bottom="20px",
                display="flex",
                flex_direction="column",
            ),
        ),
        
        # Form Content
        rx.cond(
            AuthState.auth_mode == "login",
            _login_form(),
            _signup_form(),
        ),
        
        # Modern Divider
        rx.box(
            rx.box(
                flex="1",
                height="1px",
                background=T.border_light,
            ),
            rx.text(
                "of",
                color=T.text_tertiary,
                font_size="13px",
                padding="0 16px",
                font_weight="500",
                letter_spacing="0.5px",
            ),
            rx.box(
                flex="1",
                height="1px",
                background=T.border_light,
            ),
            display="flex",
            align_items="center",
            margin="20px 0",
        ),
        
        # Enhanced Guest Button with improved visibility
        rx.button(
            rx.box(
                rx.icon(tag="user-round", size=18),
                rx.text("Doorgaan als gast", margin_left="10px", font_weight="600"),
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            width="100%",
            padding="15px",
            min_height="52px",
            background="transparent",
            color=T.primary,
            border=f"2px solid {T.primary}",
            border_radius=RADIUS["xl"],
            cursor="pointer",
            font_size="15px",
            on_click=AuthState.continue_as_guest,
            transition=TRANSITIONS["normal"],
            _hover={
                "background": T.primary_muted,
                "border_color": T.primary_hover,
                "transform": "translateY(-1px)",
                "box_shadow": T.shadow_sm,
            },
            _active={
                "transform": "translateY(0)",
            },
        ),
        
        # Guest info with icon
        rx.box(
            rx.icon(tag="info", size=12, color=T.text_tertiary),
            rx.text(
                "Gastmodus: beperkte functies, geen opgeslagen voorkeuren",
                font_size="11px",
                margin_left="6px",
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            color=T.text_tertiary,
            margin_top="10px",
        ),
        
        width=["100%", "100%", MODAL_CONFIG["right_panel_width"]],
        padding=["24px 16px", "28px 20px", "32px 28px"],
        display="flex",
        flex_direction="column",
        overflow_y="auto",
        overflow_x="hidden",
        style={
            "scroll-behavior": "smooth",
            "-webkit-overflow-scrolling": "touch",
        },
        background=T.bg_primary,
    )


# ============================================================================
# TAB SELECTOR
# ============================================================================


def _modern_tab_selector() -> rx.Component:
    """Modern tab selector with smooth transitions and elevated design."""
    return rx.box(
        rx.box(
            # Login Tab
            rx.box(
                rx.box(
                    rx.icon(
                        tag="log-in",
                        size=16,
                        color=rx.cond(
                            AuthState.auth_mode == "login",
                            "white",
                            T.text_secondary
                        ),
                        margin_right="8px",
                    ),
                    rx.text(
                        "Inloggen",
                        font_size="14px",
                        font_weight="600",
                        color=rx.cond(
                            AuthState.auth_mode == "login",
                            "white",
                            T.text_secondary
                        ),
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                padding="12px 20px",
                cursor="pointer",
                border_radius=RADIUS["xl"],
                background=rx.cond(
                    AuthState.auth_mode == "login",
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    "transparent"
                ),
                box_shadow=rx.cond(
                    AuthState.auth_mode == "login",
                    "0 4px 12px rgba(16, 163, 127, 0.3)",
                    "none"
                ),
                flex="1",
                text_align="center",
                transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                transform=rx.cond(
                    AuthState.auth_mode == "login",
                    "translateY(-2px)",
                    "translateY(0)"
                ),
                on_click=lambda: AuthState.set_auth_mode("login"),
                _hover={
                    "background": rx.cond(
                        AuthState.auth_mode != "login",
                        T.bg_hover,
                        None
                    ),
                },
            ),
            
            # Signup Tab
            rx.box(
                rx.box(
                    rx.icon(
                        tag="user-plus",
                        size=16,
                        color=rx.cond(
                            AuthState.auth_mode == "signup",
                            "white",
                            T.text_secondary
                        ),
                        margin_right="8px",
                    ),
                    rx.text(
                        "Registreren",
                        font_size="14px",
                        font_weight="600",
                        color=rx.cond(
                            AuthState.auth_mode == "signup",
                            "white",
                            T.text_secondary
                        ),
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                padding="12px 20px",
                cursor="pointer",
                border_radius=RADIUS["xl"],
                background=rx.cond(
                    AuthState.auth_mode == "signup",
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    "transparent"
                ),
                box_shadow=rx.cond(
                    AuthState.auth_mode == "signup",
                    "0 4px 12px rgba(16, 163, 127, 0.3)",
                    "none"
                ),
                flex="1",
                text_align="center",
                transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                transform=rx.cond(
                    AuthState.auth_mode == "signup",
                    "translateY(-2px)",
                    "translateY(0)"
                ),
                on_click=lambda: AuthState.set_auth_mode("signup"),
                _hover={
                    "background": rx.cond(
                        AuthState.auth_mode != "signup",
                        T.bg_hover,
                        None
                    ),
                },
            ),
            
            display="flex",
            gap="6px",
        ),
        background=rx.color_mode_cond(
            light="rgba(243, 244, 246, 0.8)",
            dark="rgba(30, 30, 35, 0.8)"
        ),
        padding="5px",
        border_radius=RADIUS["2xl"],
        margin_bottom="24px",
        border=f"1px solid {T.border_light}",
    )


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
                margin_bottom="4px",
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
                    padding="12px 12px 12px 36px",
                    border=rx.cond(
                        AuthState.firstname_error != "",
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="14px",
                    line_height="1.4",
                    height="44px",
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
            margin_bottom="8px",
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
            margin_bottom="8px",
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
                    padding="12px 12px 12px 36px",
                    border=rx.cond(
                        AuthState.email_error != "",
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="44px",
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
            margin_bottom="8px",
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
                    padding="12px 36px 12px 36px",
                    border=rx.cond(
                        AuthState.password_error != "",
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="44px",
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
            margin_bottom="8px",
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
                    padding="12px 36px 12px 36px",
                    border=rx.cond(
                        AuthState.confirm_password_error != "",
                        f"1.5px solid {T.error}",
                        f"1.5px solid {T.border}"
                    ),
                    border_radius="8px",
                    font_size="15px",
                    line_height="1.5",
                    height="44px",
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
            margin_bottom="12px",
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


