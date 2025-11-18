"""Authentication modal component."""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.styles.theme import COLORS


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
                background="rgba(0, 0, 0, 0.5)",
                z_index="999",
                on_click=AuthState.toggle_auth_modal,
                animation="fadeIn 0.2s ease-out",
            ),
            
            # Modal content
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
                        },
                        on_click=AuthState.toggle_auth_modal,
                    ),
                    position="absolute",
                    top="20px",
                    right="20px",
                    z_index="1",
                ),
                
                # Logo/Title with gradient
                rx.box(
                    rx.heading(
                        rx.icon(
                            tag="sparkles",
                            size=36,
                            color=COLORS["primary_green"],
                            margin_right="12px",
                        ),
                        "EduChat",
                        size="9",
                        color=COLORS["primary_green"],
                        margin_bottom="8px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    rx.text(
                        "Your AI Study Assistant",
                        color=COLORS["text_secondary"],
                        font_size="16px",
                    ),
                    text_align="center",
                    margin_bottom="32px",
                ),
                
                # Auth mode selector (Login/Signup tabs)
                rx.box(
                    rx.box(
                        rx.text(
                            "Login",
                            padding="12px 24px",
                            cursor="pointer",
                            border_bottom=rx.cond(
                                AuthState.auth_mode == "login",
                                f"3px solid {COLORS['primary_green']}",
                                "3px solid transparent"
                            ),
                            color=rx.cond(
                                AuthState.auth_mode == "login",
                                COLORS["primary_green"],
                                COLORS["text_secondary"]
                            ),
                            font_weight=rx.cond(
                                AuthState.auth_mode == "login",
                                "600",
                                "400"
                            ),
                            on_click=lambda: AuthState.set_auth_mode("login"),
                            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                            _hover={
                                "color": COLORS["primary_green"],
                                "background": f"rgba(16, 163, 127, 0.05)",
                            },
                        ),
                        flex="1",
                        text_align="center",
                    ),
                    rx.box(
                        rx.text(
                            "Sign Up",
                            padding="12px 24px",
                            cursor="pointer",
                            border_bottom=rx.cond(
                                AuthState.auth_mode == "signup",
                                f"3px solid {COLORS['primary_green']}",
                                "3px solid transparent"
                            ),
                            color=rx.cond(
                                AuthState.auth_mode == "signup",
                                COLORS["primary_green"],
                                COLORS["text_secondary"]
                            ),
                            font_weight=rx.cond(
                                AuthState.auth_mode == "signup",
                                "600",
                                "400"
                            ),
                            on_click=lambda: AuthState.set_auth_mode("signup"),
                            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                            _hover={
                                "color": COLORS["primary_green"],
                                "background": f"rgba(16, 163, 127, 0.05)",
                            },
                        ),
                        flex="1",
                        text_align="center",
                    ),
                    display="flex",
                    border_bottom=f"1px solid {COLORS['border']}",
                    margin_bottom="32px",
                ),
                
                # Login form
                rx.cond(
                    AuthState.auth_mode == "login",
                    login_form(),
                    signup_form(),
                ),
                
                # Divider
                rx.box(
                    rx.box(height="1px", flex="1", background=COLORS["border"]),
                    rx.text("or", padding="0 16px", color=COLORS["text_secondary"]),
                    rx.box(height="1px", flex="1", background=COLORS["border"]),
                    display="flex",
                    align_items="center",
                    margin="24px 0",
                ),
                
                # Guest option
                rx.button(
                    "Continue as Guest",
                    width="100%",
                    padding="12px",
                    background="white",
                    color=COLORS["primary_green"],
                    border=f"2px solid {COLORS['primary_green']}",
                    border_radius="8px",
                    cursor="pointer",
                    font_weight="600",
                    transition="all 0.2s ease",
                    _hover={
                        "background": COLORS["light_gray"],
                    },
                    on_click=AuthState.continue_as_guest,
                ),
                
                rx.text(
                    "Guest mode: Limited features, no data saved",
                    font_size="14px",
                    color=COLORS["text_secondary"],
                    text_align="center",
                    margin_top="12px",
                ),
                
                # Modal card styling
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                background="white",
                border_radius="16px",
                padding="40px",
                width="90%",
                max_width="480px",
                box_shadow="0 20px 60px rgba(0, 0, 0, 0.2)",
                z_index="1000",
                max_height="90vh",
                overflow_y="auto",
                animation="scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            ),
            
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            z_index="998",
        )
    )


def login_form() -> rx.Component:
    """Login form component."""
    
    return rx.box(
        # Error message with icon
        rx.cond(
            AuthState.auth_error != "",
            rx.box(
                rx.icon(
                    tag="triangle-alert",
                    size=16,
                    color="#dc2626",
                    margin_right="8px",
                ),
                rx.text(
                    AuthState.auth_error,
                    color="#dc2626",
                    font_size="14px",
                    flex="1",
                ),
                display="flex",
                align_items="center",
                background="#fee2e2",
                padding="12px 16px",
                border_radius="8px",
                margin_bottom="16px",
                border="1px solid #fecaca",
                animation="slideInUp 0.3s ease-out",
            ),
        ),
        
        # Email input
        rx.box(
            rx.text(
                "Email",
                font_weight="500",
                margin_bottom="8px",
                color=COLORS["text_primary"],
            ),
            rx.input(
                placeholder="your.email@example.com",
                value=AuthState.email,
                on_change=AuthState.set_email,
                type="email",
                width="100%",
                padding="12px",
                border=f"1px solid {COLORS['border']}",
                border_radius="8px",
                font_size="16px",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                },
            ),
            margin_bottom="16px",
        ),
        
        # Password input
        rx.box(
            rx.text(
                "Password",
                font_weight="500",
                margin_bottom="8px",
                color=COLORS["text_primary"],
            ),
            rx.input(
                placeholder="••••••••",
                value=AuthState.password,
                on_change=AuthState.set_password,
                type="password",
                width="100%",
                padding="12px",
                border=f"1px solid {COLORS['border']}",
                border_radius="8px",
                font_size="16px",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
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
                ),
                rx.text(
                    "Remember me",
                    font_size="14px",
                    color=COLORS["text_secondary"],
                ),
                display="flex",
                align_items="center",
            ),
            rx.text(
                "Forgot password?",
                font_size="14px",
                color=COLORS["primary_green"],
                cursor="pointer",
                _hover={"text_decoration": "underline"},
            ),
            display="flex",
            justify_content="space-between",
            align_items="center",
            margin_bottom="24px",
        ),
        
        # Login button with loading state
        rx.button(
            rx.cond(
                AuthState.auth_loading,
                rx.box(
                    rx.spinner(size="1", color="white", margin_right="8px"),
                    rx.text("Logging in..."),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    rx.icon(tag="log-in", size=18, margin_right="8px"),
                    rx.text("Login"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            width="100%",
            padding="14px",
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            color="white",
            border="none",
            border_radius="10px",
            cursor=rx.cond(AuthState.auth_loading, "not-allowed", "pointer"),
            font_weight="600",
            font_size="16px",
            transition="all 0.3s ease",
            box_shadow="0 2px 8px rgba(16, 163, 127, 0.3)",
            _hover={
                "transform": rx.cond(AuthState.auth_loading, "none", "translateY(-2px)"),
                "box_shadow": rx.cond(AuthState.auth_loading, "0 2px 8px rgba(16, 163, 127, 0.3)", "0 4px 12px rgba(16, 163, 127, 0.4)"),
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
                    tag="triangle-alert",
                    size=18,
                    color="#dc2626",
                    margin_right="8px",
                ),
                rx.text(
                    AuthState.auth_error,
                    color="#dc2626",
                    font_size="14px",
                    flex="1",
                ),
                display="flex",
                align_items="center",
                background="#fee2e2",
                padding="12px 16px",
                border_radius="8px",
                margin_bottom="16px",
                border="1px solid #fecaca",
                animation="slideInUp 0.3s ease-out",
            ),
        ),
        
        # Name input
        rx.box(
            rx.text(
                "Full Name",
                font_weight="500",
                margin_bottom="8px",
                color=COLORS["text_primary"],
            ),
            rx.input(
                placeholder="John Doe",
                value=AuthState.name,
                on_change=AuthState.set_name,
                width="100%",
                padding="12px",
                border=f"1px solid {COLORS['border']}",
                border_radius="8px",
                font_size="16px",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                },
            ),
            margin_bottom="16px",
        ),
        
        # Email input
        rx.box(
            rx.text(
                "Email",
                font_weight="500",
                margin_bottom="8px",
                color=COLORS["text_primary"],
            ),
            rx.input(
                placeholder="your.email@example.com",
                value=AuthState.email,
                on_change=AuthState.set_email,
                type="email",
                width="100%",
                padding="12px",
                border=f"1px solid {COLORS['border']}",
                border_radius="8px",
                font_size="16px",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                },
            ),
            margin_bottom="16px",
        ),
        
        # Password input
        rx.box(
            rx.text(
                "Password",
                font_weight="500",
                margin_bottom="8px",
                color=COLORS["text_primary"],
            ),
            rx.input(
                placeholder="••••••••",
                value=AuthState.password,
                on_change=AuthState.set_password,
                type="password",
                width="100%",
                padding="12px",
                border=f"1px solid {COLORS['border']}",
                border_radius="8px",
                font_size="16px",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                },
            ),
            margin_bottom="16px",
        ),
        
        # Confirm password input
        rx.box(
            rx.text(
                "Confirm Password",
                font_weight="500",
                margin_bottom="8px",
                color=COLORS["text_primary"],
            ),
            rx.input(
                placeholder="••••••••",
                value=AuthState.confirm_password,
                on_change=AuthState.set_confirm_password,
                type="password",
                width="100%",
                padding="12px",
                border=f"1px solid {COLORS['border']}",
                border_radius="8px",
                font_size="16px",
                _focus={
                    "outline": "none",
                    "border_color": COLORS["primary_green"],
                },
            ),
            margin_bottom="16px",
        ),
        
        # Remember me
        rx.box(
            rx.input(
                type="checkbox",
                checked=AuthState.remember_me,
                on_change=AuthState.toggle_remember_me,
                margin_right="8px",
            ),
            rx.text(
                "Remember me",
                font_size="14px",
                color=COLORS["text_secondary"],
            ),
            display="flex",
            align_items="center",
            margin_bottom="24px",
        ),
        
        # Signup button with loading state
        rx.button(
            rx.cond(
                AuthState.auth_loading,
                rx.box(
                    rx.spinner(size="1", color="white", margin_right="8px"),
                    rx.text("Creating account..."),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    rx.icon(tag="user-plus", size=18, margin_right="8px"),
                    rx.text("Create Account"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            width="100%",
            padding="14px",
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            color="white",
            border="none",
            border_radius="10px",
            cursor=rx.cond(AuthState.auth_loading, "not-allowed", "pointer"),
            font_weight="600",
            font_size="16px",
            transition="all 0.3s ease",
            box_shadow="0 2px 8px rgba(16, 163, 127, 0.3)",
            _hover={
                "transform": rx.cond(AuthState.auth_loading, "none", "translateY(-2px)"),
                "box_shadow": rx.cond(AuthState.auth_loading, "0 2px 8px rgba(16, 163, 127, 0.3)", "0 4px 12px rgba(16, 163, 127, 0.4)"),
            },
            _active={
                "transform": "translateY(0)",
            },
            disabled=AuthState.auth_loading,
            on_click=AuthState.signup,
        ),
        
        width="100%",
    )


