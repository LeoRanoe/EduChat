"""Authentication modal component."""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.styles.theme import COLORS


def lock_illustration_svg() -> rx.Component:
    """SVG illustration for auth screens."""
    return rx.html("""
        <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Shield background -->
            <path d="M100 20 L160 40 L160 90 Q160 130 100 170 Q40 130 40 90 L40 40 Z" 
                  fill="#10a37f" opacity="0.1"/>
            
            <!-- Shield outline -->
            <path d="M100 25 L155 43 L155 88 Q155 125 100 162 Q45 125 45 88 L45 43 Z" 
                  fill="none" stroke="#10a37f" stroke-width="2.5"/>
            
            <!-- Lock body -->
            <rect x="80" y="95" width="40" height="45" rx="4" 
                  fill="#10a37f" opacity="0.9"/>
            
            <!-- Lock shackle -->
            <path d="M85 95 L85 75 Q85 60 100 60 Q115 60 115 75 L115 95" 
                  fill="none" stroke="#10a37f" stroke-width="4" opacity="0.9"/>
            
            <!-- Keyhole -->
            <circle cx="100" cy="110" r="4" fill="white"/>
            <rect x="98" y="110" width="4" height="12" rx="1" fill="white"/>
            
            <!-- Decorative dots -->
            <circle cx="65" cy="60" r="3" fill="#10a37f" opacity="0.4">
                <animate attributeName="opacity" values="0.4;0.8;0.4" dur="2s" repeatCount="indefinite"/>
            </circle>
            <circle cx="135" cy="60" r="3" fill="#10a37f" opacity="0.4">
                <animate attributeName="opacity" values="0.4;0.8;0.4" dur="2s" begin="0.5s" repeatCount="indefinite"/>
            </circle>
            <circle cx="65" cy="140" r="3" fill="#10a37f" opacity="0.4">
                <animate attributeName="opacity" values="0.4;0.8;0.4" dur="2s" begin="1s" repeatCount="indefinite"/>
            </circle>
            <circle cx="135" cy="140" r="3" fill="#10a37f" opacity="0.4">
                <animate attributeName="opacity" values="0.4;0.8;0.4" dur="2s" begin="1.5s" repeatCount="indefinite"/>
            </circle>
        </svg>
    """)


def auth_modal() -> rx.Component:
    """Authentication modal with login/signup forms and guest option."""
    
    return rx.cond(
        AuthState.show_auth_modal,
        rx.box(
            # Modal overlay with fade-in animation
            rx.box(
                width="100vw",
                height="100vh",
                position="fixed",
                top="0",
                left="0",
                background="rgba(0, 0, 0, 0.6)",
                backdrop_filter="blur(8px)",
                z_index="999",
                on_click=AuthState.toggle_auth_modal,
                animation="fadeIn 0.3s ease-out",
            ),
            
            # Modal content - Split design
            rx.box(
                # Close button
                rx.box(
                    rx.icon(
                        tag="x",
                        size=24,
                        color=COLORS["text_secondary"],
                        cursor="pointer",
                        transition="all 0.2s ease",
                        _hover={
                            "color": COLORS["text_primary"],
                            "transform": "rotate(90deg)",
                            "scale": "1.1",
                        },
                        on_click=AuthState.toggle_auth_modal,
                    ),
                    position="absolute",
                    top="24px",
                    right="24px",
                    z_index="1",
                    padding="8px",
                    border_radius="50%",
                    background="white",
                    box_shadow="0 2px 8px rgba(0,0,0,0.1)",
                    _hover={
                        "background": COLORS["light_gray"],
                    },
                ),
                
                rx.box(
                    # Left side - Illustration & Info (hidden on mobile)
                    rx.box(
                        rx.box(
                            lock_illustration_svg(),
                            display="flex",
                            justify_content="center",
                            margin_bottom="32px",
                        ),
                        
                        rx.heading(
                            "Welkom bij EduChat",
                            size="8",
                            color="white",
                            margin_bottom="16px",
                            text_align="center",
                            font_weight="700",
                        ),
                        
                        rx.text(
                            "Jouw persoonlijke AI-assistent voor Surinaams onderwijs",
                            color="rgba(255,255,255,0.9)",
                            font_size="16px",
                            text_align="center",
                            line_height="1.6",
                            margin_bottom="32px",
                        ),
                        
                        # Benefits list
                        rx.box(
                            benefit_item_auth("Directe antwoorden op jouw vragen"),
                            benefit_item_auth("Studiemateriaal op maat"),
                            benefit_item_auth("24/7 beschikbaar"),
                            benefit_item_auth("Gratis te gebruiken"),
                            display="flex",
                            flex_direction="column",
                            gap="16px",
                        ),
                        
                        padding=["0", "48px 40px", "48px 40px"],
                        display=["none", "flex", "flex"],
                        flex_direction="column",
                        justify_content="center",
                    ),
                    
                    # Right side - Form
                    rx.box(
                        # Logo/Title (show on mobile too)
                        rx.box(
                            rx.heading(
                                rx.icon(
                                    tag="graduation-cap",
                                    size=32,
                                    color=COLORS["primary_green"],
                                    margin_right="12px",
                                ),
                                "EduChat",
                                size="8",
                                color=COLORS["primary_green"],
                                margin_bottom="8px",
                                display="flex",
                                align_items="center",
                                font_weight="700",
                            ),
                            rx.text(
                                rx.cond(
                                    AuthState.auth_mode == "login",
                                    "Inloggen op je account",
                                    "Maak een gratis account"
                                ),
                                color=COLORS["text_secondary"],
                                font_size="15px",
                                font_weight="500",
                            ),
                            margin_bottom="32px",
                        ),
                        
                        # Auth mode selector (Login/Signup tabs) - Modern pill style
                        rx.box(
                            rx.box(
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
                                    padding="10px 24px",
                                    cursor="pointer",
                                    border_radius="8px",
                                    background=rx.cond(
                                        AuthState.auth_mode == "login",
                                        COLORS["primary_green"],
                                        "transparent"
                                    ),
                                    transition="all 0.3s ease",
                                    on_click=lambda: AuthState.set_auth_mode("login"),
                                    flex="1",
                                    text_align="center",
                                    _hover={
                                        "background": rx.cond(
                                            AuthState.auth_mode == "login",
                                            COLORS["primary_green"],
                                            f"rgba(16, 163, 127, 0.1)"
                                        ),
                                    },
                                ),
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
                                    padding="10px 24px",
                                    cursor="pointer",
                                    border_radius="8px",
                                    background=rx.cond(
                                        AuthState.auth_mode == "signup",
                                        COLORS["primary_green"],
                                        "transparent"
                                    ),
                                    transition="all 0.3s ease",
                                    on_click=lambda: AuthState.set_auth_mode("signup"),
                                    flex="1",
                                    text_align="center",
                                    _hover={
                                        "background": rx.cond(
                                            AuthState.auth_mode == "signup",
                                            COLORS["primary_green"],
                                            f"rgba(16, 163, 127, 0.1)"
                                        ),
                                    },
                                ),
                                display="flex",
                                gap="8px",
                            ),
                            background=COLORS["light_gray"],
                            padding="6px",
                            border_radius="12px",
                            margin_bottom="32px",
                        ),
                        
                        # Login/Signup form
                        rx.cond(
                            AuthState.auth_mode == "login",
                            login_form(),
                            signup_form(),
                        ),
                        
                        # Divider
                        rx.box(
                            rx.box(height="1px", flex="1", background=COLORS["border"]),
                            rx.text("of", padding="0 16px", color=COLORS["text_secondary"], font_size="14px"),
                            rx.box(height="1px", flex="1", background=COLORS["border"]),
                            display="flex",
                            align_items="center",
                            margin="28px 0",
                        ),
                        
                        # Guest option
                        rx.button(
                            rx.icon(tag="user", size=18, margin_right="10px"),
                            "Doorgaan als Gast",
                            width="100%",
                            padding="14px",
                            background="white",
                            color=COLORS["primary_green"],
                            border=f"2px solid {COLORS['primary_green']}",
                            border_radius="10px",
                            cursor="pointer",
                            font_weight="600",
                            font_size="15px",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            transition="all 0.3s ease",
                            _hover={
                                "background": f"rgba(16, 163, 127, 0.05)",
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 12px rgba(16, 163, 127, 0.15)",
                            },
                            on_click=AuthState.continue_as_guest,
                        ),
                        
                        rx.box(
                            rx.icon(tag="info", size=14, color=COLORS["text_secondary"], margin_right="6px"),
                            rx.text(
                                "Gastmodus: Beperkte functies, gegevens worden niet opgeslagen",
                                font_size="13px",
                                color=COLORS["text_secondary"],
                            ),
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            margin_top="12px",
                            padding="8px",
                            background=COLORS["light_gray"],
                            border_radius="6px",
                        ),
                        
                        padding=["32px 24px", "48px 40px", "48px 40px"],
                    ),
                    
                    display="grid",
                    grid_template_columns=["1fr", "1fr", "repeat(2, 1fr)"],
                    min_height=["auto", "auto", "600px"],
                ),
                
                # Modal card styling
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                background="white",
                border_radius=["16px", "20px", "20px"],
                width=["95%", "90%", "90%"],
                max_width=["100%", "600px", "1000px"],
                box_shadow="0 25px 70px rgba(0, 0, 0, 0.3)",
                z_index="1000",
                max_height="90vh",
                overflow_y="auto",
                overflow_x="hidden",
                animation="modalSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                
                # Left side gradient background (only on desktop)
                background_image=[
                    "white",
                    "white", 
                    f"linear-gradient(to right, {COLORS['primary_green']} 0%, {COLORS['primary_green']} 50%, white 50%, white 100%)"
                ],
            ),
            
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            z_index="998",
        )
    )


def benefit_item_auth(text: str) -> rx.Component:
    """Benefit item for auth modal left side."""
    return rx.box(
        rx.icon(
            tag="circle-check",
            size=20,
            color="white",
            margin_right="12px",
            flex_shrink="0",
        ),
        rx.text(
            text,
            color="white",
            font_size="15px",
            line_height="1.5",
        ),
        display="flex",
        align_items="center",
    )


def login_form() -> rx.Component:
    """Login form component."""
    
    return rx.box(
        # Error message with icon
        rx.cond(
            AuthState.auth_error != "",
            rx.box(
                rx.icon(
                    tag="alert-triangle",
                    size=18,
                    color="#dc2626",
                    margin_right="10px",
                    flex_shrink="0",
                ),
                rx.text(
                    AuthState.auth_error,
                    color="#dc2626",
                    font_size="14px",
                    flex="1",
                    line_height="1.4",
                ),
                display="flex",
                align_items="start",
                background="#fee2e2",
                padding="14px 16px",
                border_radius="10px",
                margin_bottom="20px",
                border="1px solid #fecaca",
                animation="slideDown 0.3s ease-out",
            ),
        ),
        
        # Email input
        rx.box(
            rx.box(
                rx.icon(
                    tag="mail",
                    size=16,
                    color=COLORS["text_secondary"],
                    margin_right="6px",
                ),
                rx.text(
                    "E-mailadres",
                    font_weight="600",
                    font_size="14px",
                    color=COLORS["text_primary"],
                ),
                display="flex",
                align_items="center",
                margin_bottom="8px",
            ),
            rx.input(
                placeholder="jouw.email@voorbeeld.com",
                value=AuthState.email,
                on_change=AuthState.set_email,
                type="email",
                width="100%",
                padding="14px 16px",
                border=f"2px solid {COLORS['border']}",
                border_radius="10px",
                font_size="15px",
                transition="all 0.2s ease",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                    "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)",
                },
            ),
            margin_bottom="20px",
        ),
        
        # Password input
        rx.box(
            rx.box(
                rx.icon(
                    tag="lock",
                    size=16,
                    color=COLORS["text_secondary"],
                    margin_right="6px",
                ),
                rx.text(
                    "Wachtwoord",
                    font_weight="600",
                    font_size="14px",
                    color=COLORS["text_primary"],
                ),
                display="flex",
                align_items="center",
                margin_bottom="8px",
            ),
            rx.input(
                placeholder="••••••••",
                value=AuthState.password,
                on_change=AuthState.set_password,
                type="password",
                width="100%",
                padding="14px 16px",
                border=f"2px solid {COLORS['border']}",
                border_radius="10px",
                font_size="15px",
                transition="all 0.2s ease",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                    "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)",
                },
            ),
            margin_bottom="16px",
        ),
        
        # Remember me & Forgot password
        rx.box(
            rx.box(
                rx.input(
                    type="checkbox",
                    checked=AuthState.remember_me,
                    on_change=AuthState.toggle_remember_me,
                    margin_right="8px",
                    accent_color=COLORS["primary_green"],
                ),
                rx.text(
                    "Onthoud mij",
                    font_size="14px",
                    color=COLORS["text_secondary"],
                    font_weight="500",
                ),
                display="flex",
                align_items="center",
            ),
            rx.text(
                "Wachtwoord vergeten?",
                font_size="14px",
                color=COLORS["primary_green"],
                cursor="pointer",
                font_weight="600",
                transition="all 0.2s ease",
                _hover={
                    "text_decoration": "underline",
                    "color": COLORS["dark_green"],
                },
            ),
            display="flex",
            justify_content="space-between",
            align_items="center",
            margin_bottom="28px",
        ),
        
        # Login button with loading state
        rx.button(
            rx.cond(
                AuthState.auth_loading,
                rx.box(
                    rx.spinner(size="1", color="white", margin_right="10px"),
                    rx.text("Aan het inloggen...", font_weight="600"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    rx.icon(tag="log-in", size=20, margin_right="10px"),
                    rx.text("Inloggen", font_weight="600"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            width="100%",
            padding="16px",
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            color="white",
            border="none",
            border_radius="10px",
            cursor=rx.cond(AuthState.auth_loading, "not-allowed", "pointer"),
            font_size="16px",
            transition="all 0.3s ease",
            box_shadow="0 4px 12px rgba(16, 163, 127, 0.3)",
            _hover={
                "transform": rx.cond(AuthState.auth_loading, "none", "translateY(-2px)"),
                "box_shadow": rx.cond(AuthState.auth_loading, "0 4px 12px rgba(16, 163, 127, 0.3)", "0 6px 20px rgba(16, 163, 127, 0.4)"),
            },
            _active={
                "transform": "translateY(0)",
            },
            disabled=AuthState.auth_loading,
            on_click=AuthState.login,
        ),
        
        width="100%",
    )


def signup_form() -> rx.Component:
    """Signup form component."""
    
    return rx.box(
        # Error message with icon
        rx.cond(
            AuthState.auth_error != "",
            rx.box(
                rx.icon(
                    tag="alert-triangle",
                    size=18,
                    color="#dc2626",
                    margin_right="10px",
                    flex_shrink="0",
                ),
                rx.text(
                    AuthState.auth_error,
                    color="#dc2626",
                    font_size="14px",
                    flex="1",
                    line_height="1.4",
                ),
                display="flex",
                align_items="start",
                background="#fee2e2",
                padding="14px 16px",
                border_radius="10px",
                margin_bottom="20px",
                border="1px solid #fecaca",
                animation="slideDown 0.3s ease-out",
            ),
        ),
        
        # Name input
        rx.box(
            rx.box(
                rx.icon(
                    tag="user",
                    size=16,
                    color=COLORS["text_secondary"],
                    margin_right="6px",
                ),
                rx.text(
                    "Volledige Naam",
                    font_weight="600",
                    font_size="14px",
                    color=COLORS["text_primary"],
                ),
                display="flex",
                align_items="center",
                margin_bottom="8px",
            ),
            rx.input(
                placeholder="Voor- en achternaam",
                value=AuthState.name,
                on_change=AuthState.set_name,
                width="100%",
                padding="14px 16px",
                border=f"2px solid {COLORS['border']}",
                border_radius="10px",
                font_size="15px",
                transition="all 0.2s ease",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                    "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)",
                },
            ),
            margin_bottom="18px",
        ),
        
        # Email input
        rx.box(
            rx.box(
                rx.icon(
                    tag="mail",
                    size=16,
                    color=COLORS["text_secondary"],
                    margin_right="6px",
                ),
                rx.text(
                    "E-mailadres",
                    font_weight="600",
                    font_size="14px",
                    color=COLORS["text_primary"],
                ),
                display="flex",
                align_items="center",
                margin_bottom="8px",
            ),
            rx.input(
                placeholder="jouw.email@voorbeeld.com",
                value=AuthState.email,
                on_change=AuthState.set_email,
                type="email",
                width="100%",
                padding="14px 16px",
                border=f"2px solid {COLORS['border']}",
                border_radius="10px",
                font_size="15px",
                transition="all 0.2s ease",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                    "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)",
                },
            ),
            margin_bottom="18px",
        ),
        
        # Password input
        rx.box(
            rx.box(
                rx.icon(
                    tag="lock",
                    size=16,
                    color=COLORS["text_secondary"],
                    margin_right="6px",
                ),
                rx.text(
                    "Wachtwoord",
                    font_weight="600",
                    font_size="14px",
                    color=COLORS["text_primary"],
                ),
                display="flex",
                align_items="center",
                margin_bottom="8px",
            ),
            rx.input(
                placeholder="Minimaal 8 tekens",
                value=AuthState.password,
                on_change=AuthState.set_password,
                type="password",
                width="100%",
                padding="14px 16px",
                border=f"2px solid {COLORS['border']}",
                border_radius="10px",
                font_size="15px",
                transition="all 0.2s ease",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                    "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)",
                },
            ),
            margin_bottom="18px",
        ),
        
        # Confirm password input
        rx.box(
            rx.box(
                rx.icon(
                    tag="shield-check",
                    size=16,
                    color=COLORS["text_secondary"],
                    margin_right="6px",
                ),
                rx.text(
                    "Bevestig Wachtwoord",
                    font_weight="600",
                    font_size="14px",
                    color=COLORS["text_primary"],
                ),
                display="flex",
                align_items="center",
                margin_bottom="8px",
            ),
            rx.input(
                placeholder="Herhaal je wachtwoord",
                value=AuthState.confirm_password,
                on_change=AuthState.set_confirm_password,
                type="password",
                width="100%",
                padding="14px 16px",
                border=f"2px solid {COLORS['border']}",
                border_radius="10px",
                font_size="15px",
                transition="all 0.2s ease",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                    "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.1)",
                },
            ),
            margin_bottom="20px",
        ),
        
        # Terms agreement
        rx.box(
            rx.box(
                rx.input(
                    type="checkbox",
                    checked=AuthState.remember_me,
                    on_change=AuthState.toggle_remember_me,
                    margin_right="8px",
                    accent_color=COLORS["primary_green"],
                ),
                rx.text(
                    "Ik ga akkoord met de ",
                    rx.text(
                        "voorwaarden",
                        color=COLORS["primary_green"],
                        font_weight="600",
                        cursor="pointer",
                        _hover={"text_decoration": "underline"},
                    ),
                    " en ",
                    rx.text(
                        "privacybeleid",
                        color=COLORS["primary_green"],
                        font_weight="600",
                        cursor="pointer",
                        _hover={"text_decoration": "underline"},
                    ),
                    font_size="13px",
                    color=COLORS["text_secondary"],
                    line_height="1.4",
                ),
                display="flex",
                align_items="start",
            ),
            margin_bottom="24px",
        ),
        
        # Signup button with loading state
        rx.button(
            rx.cond(
                AuthState.auth_loading,
                rx.box(
                    rx.spinner(size="1", color="white", margin_right="10px"),
                    rx.text("Account aanmaken...", font_weight="600"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    rx.icon(tag="user-plus", size=20, margin_right="10px"),
                    rx.text("Account Aanmaken", font_weight="600"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            width="100%",
            padding="16px",
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            color="white",
            border="none",
            border_radius="10px",
            cursor=rx.cond(AuthState.auth_loading, "not-allowed", "pointer"),
            font_size="16px",
            transition="all 0.3s ease",
            box_shadow="0 4px 12px rgba(16, 163, 127, 0.3)",
            _hover={
                "transform": rx.cond(AuthState.auth_loading, "none", "translateY(-2px)"),
                "box_shadow": rx.cond(AuthState.auth_loading, "0 4px 12px rgba(16, 163, 127, 0.3)", "0 6px 20px rgba(16, 163, 127, 0.4)"),
            },
            _active={
                "transform": "translateY(0)",
            },
            disabled=AuthState.auth_loading,
            on_click=AuthState.signup,
        ),
        
        width="100%",
    )


