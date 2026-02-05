"""
Password Reset Page
Allows users to reset their password using a token from their email.
"""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.styles.theme import ThemeTokens as T


class ResetPasswordState(AuthState):
    """State for password reset page."""
    
    # Form fields
    new_password: str = ""
    confirm_new_password: str = ""
    reset_token: str = ""
    
    # UI state
    reset_loading: bool = False
    reset_success: bool = False
    reset_error: str = ""
    show_new_password: bool = False
    show_confirm_new_password: bool = False
    
    # Password validation
    new_password_error: str = ""
    confirm_new_password_error: str = ""
    
    def on_load(self):
        """Extract reset token from URL on page load."""
        try:
            # Get hash fragment parameters (Supabase sends token in hash)
            # For now, we'll use query params as fallback
            params = self.router.page.params
            
            # Check for access_token in params (Supabase password reset)
            if "access_token" in params:
                self.reset_token = params.get("access_token", "")
            elif "token" in params:
                self.reset_token = params.get("token", "")
            
            if not self.reset_token:
                self.reset_error = "Ongeldige of verlopen reset link. Vraag een nieuwe aan."
        except Exception as e:
            print(f"Error extracting reset token: {e}")
            self.reset_error = "Fout bij het laden van de pagina."
    
    def set_new_password(self, value: str):
        """Set new password with validation."""
        self.new_password = value
        self.new_password_error = ""
        self.reset_error = ""
        
        # Real-time validation
        if value and len(value) < 8:
            self.new_password_error = "Wachtwoord moet minimaal 8 tekens bevatten"
    
    def set_confirm_new_password(self, value: str):
        """Set confirm password with validation."""
        self.confirm_new_password = value
        self.confirm_new_password_error = ""
        self.reset_error = ""
        
        # Check if passwords match
        if value and self.new_password and value != self.new_password:
            self.confirm_new_password_error = "Wachtwoorden komen niet overeen"
    
    def toggle_new_password(self):
        """Toggle new password visibility."""
        self.show_new_password = not self.show_new_password
    
    def toggle_confirm_new_password(self):
        """Toggle confirm password visibility."""
        self.show_confirm_new_password = not self.show_confirm_new_password
    
    def _validate_reset_form(self) -> bool:
        """Validate password reset form."""
        is_valid = True
        
        # Validate new password
        if not self.new_password or not self.new_password.strip():
            self.new_password_error = "Wachtwoord is verplicht"
            is_valid = False
        elif len(self.new_password) < 8:
            self.new_password_error = "Wachtwoord moet minimaal 8 tekens bevatten"
            is_valid = False
        
        # Validate confirm password
        if not self.confirm_new_password:
            self.confirm_new_password_error = "Bevestig je wachtwoord"
            is_valid = False
        elif self.new_password != self.confirm_new_password:
            self.confirm_new_password_error = "Wachtwoorden komen niet overeen"
            is_valid = False
        
        # Check token
        if not self.reset_token:
            self.reset_error = "Geen reset token gevonden"
            is_valid = False
        
        return is_valid
    
    async def reset_password_with_token(self):
        """Reset password using the token from email."""
        # Clear errors
        self.new_password_error = ""
        self.confirm_new_password_error = ""
        self.reset_error = ""
        
        # Validate form
        if not self._validate_reset_form():
            return
        
        self.reset_loading = True
        yield
        
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            # Update password with token
            result = await auth_service.update_password_with_token(
                self.reset_token,
                self.new_password
            )
            
            if result.get("success"):
                self.reset_success = True
                self.toast_message = "Wachtwoord succesvol gewijzigd! Je wordt doorgestuurd..."
                self.toast_type = "success"
                self.show_toast = True
                
                # Wait a moment then redirect to login
                yield
                import asyncio
                await asyncio.sleep(2)
                yield rx.redirect("/")
            else:
                self.reset_error = result.get("error", "Kon wachtwoord niet wijzigen. Probeer opnieuw.")
        
        except Exception as e:
            print(f"Password reset error: {e}")
            self.reset_error = "Er is een fout opgetreden. Probeer het opnieuw."
        
        finally:
            self.reset_loading = False


def reset_password_page() -> rx.Component:
    """Password reset page component."""
    return rx.box(
        # Main container
        rx.box(
            # Logo/Header
            rx.box(
                rx.heading(
                    rx.icon("graduation-cap", size=32, color=T.primary),
                    " EduChat",
                    size="8",
                    weight="bold",
                    color=T.primary,
                    margin_bottom="8px",
                ),
                rx.text(
                    "Wachtwoord opnieuw instellen",
                    font_size="18px",
                    color=T.text_secondary,
                    margin_bottom="32px",
                ),
                text_align="center",
            ),
            
            # Success message
            rx.cond(
                ResetPasswordState.reset_success,
                rx.box(
                    rx.icon("check-circle", size=48, color=T.success),
                    rx.heading(
                        "Wachtwoord gewijzigd!",
                        size="6",
                        margin_top="16px",
                        margin_bottom="8px",
                    ),
                    rx.text(
                        "Je wordt doorgestuurd naar de inlogpagina...",
                        color=T.text_secondary,
                    ),
                    text_align="center",
                    padding="32px",
                ),
                # Reset form
                rx.box(
                    # Error message
                    rx.cond(
                        ResetPasswordState.reset_error != "",
                        rx.box(
                            rx.icon("alert-circle", size=16, color=T.error),
                            rx.text(
                                ResetPasswordState.reset_error,
                                font_size="14px",
                                margin_left="8px",
                            ),
                            display="flex",
                            align_items="center",
                            padding="12px 16px",
                            background_color=f"{T.error}15",
                            border_radius="8px",
                            color=T.error,
                            margin_bottom="20px",
                        ),
                    ),
                    
                    # New password field
                    rx.box(
                        rx.text(
                            "Nieuw wachtwoord",
                            font_size="14px",
                            font_weight="500",
                            margin_bottom="8px",
                            color=T.text_primary,
                        ),
                        rx.box(
                            rx.icon("lock", size=18, color=T.text_secondary),
                            rx.input(
                                type=rx.cond(
                                    ResetPasswordState.show_new_password,
                                    "text",
                                    "password"
                                ),
                                placeholder="Minimaal 8 tekens",
                                value=ResetPasswordState.new_password,
                                on_change=ResetPasswordState.set_new_password,
                                border="none",
                                outline="none",
                                flex="1",
                                font_size="15px",
                            ),
                            rx.icon(
                                rx.cond(
                                    ResetPasswordState.show_new_password,
                                    "eye-off",
                                    "eye"
                                ),
                                size=18,
                                color=T.text_secondary,
                                cursor="pointer",
                                on_click=ResetPasswordState.toggle_new_password,
                            ),
                            display="flex",
                            align_items="center",
                            gap="12px",
                            padding="12px 16px",
                            border=f"1.5px solid {rx.cond(ResetPasswordState.new_password_error != '', T.error, T.border)}",
                            border_radius="8px",
                            _focus_within={
                                "border_color": T.primary,
                            },
                        ),
                        rx.cond(
                            ResetPasswordState.new_password_error != "",
                            rx.text(
                                ResetPasswordState.new_password_error,
                                font_size="13px",
                                color=T.error,
                                margin_top="6px",
                            ),
                        ),
                        margin_bottom="20px",
                    ),
                    
                    # Confirm password field
                    rx.box(
                        rx.text(
                            "Bevestig wachtwoord",
                            font_size="14px",
                            font_weight="500",
                            margin_bottom="8px",
                            color=T.text_primary,
                        ),
                        rx.box(
                            rx.icon("lock", size=18, color=T.text_secondary),
                            rx.input(
                                type=rx.cond(
                                    ResetPasswordState.show_confirm_new_password,
                                    "text",
                                    "password"
                                ),
                                placeholder="Herhaal wachtwoord",
                                value=ResetPasswordState.confirm_new_password,
                                on_change=ResetPasswordState.set_confirm_new_password,
                                border="none",
                                outline="none",
                                flex="1",
                                font_size="15px",
                            ),
                            rx.icon(
                                rx.cond(
                                    ResetPasswordState.show_confirm_new_password,
                                    "eye-off",
                                    "eye"
                                ),
                                size=18,
                                color=T.text_secondary,
                                cursor="pointer",
                                on_click=ResetPasswordState.toggle_confirm_new_password,
                            ),
                            display="flex",
                            align_items="center",
                            gap="12px",
                            padding="12px 16px",
                            border=f"1.5px solid {rx.cond(ResetPasswordState.confirm_new_password_error != '', T.error, T.border)}",
                            border_radius="8px",
                            _focus_within={
                                "border_color": T.primary,
                            },
                        ),
                        rx.cond(
                            ResetPasswordState.confirm_new_password_error != "",
                            rx.text(
                                ResetPasswordState.confirm_new_password_error,
                                font_size="13px",
                                color=T.error,
                                margin_top="6px",
                            ),
                        ),
                        margin_bottom="24px",
                    ),
                    
                    # Submit button
                    rx.button(
                        rx.cond(
                            ResetPasswordState.reset_loading,
                            rx.spinner(size="3"),
                            "Wachtwoord wijzigen",
                        ),
                        on_click=ResetPasswordState.reset_password_with_token,
                        disabled=ResetPasswordState.reset_loading,
                        width="100%",
                        padding="12px",
                        font_size="15px",
                        font_weight="600",
                        background_color=T.primary,
                        color="white",
                        border_radius="8px",
                        cursor=rx.cond(
                            ResetPasswordState.reset_loading,
                            "not-allowed",
                            "pointer"
                        ),
                        _hover={
                            "background_color": T.primary_hover,
                        },
                        margin_bottom="16px",
                    ),
                    
                    # Back to login link
                    rx.box(
                        rx.link(
                            rx.icon("arrow-left", size=14),
                            " Terug naar inloggen",
                            href="/",
                            font_size="14px",
                            color=T.primary,
                            display="flex",
                            align_items="center",
                            gap="4px",
                            _hover={
                                "text_decoration": "underline",
                            },
                        ),
                        text_align="center",
                    ),
                ),
            ),
            
            max_width="420px",
            margin="0 auto",
            padding="40px 24px",
            background="white",
            border_radius="12px",
            box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
        ),
        
        display="flex",
        align_items="center",
        justify_content="center",
        min_height="100vh",
        background=f"linear-gradient(135deg, {T.primary}15, {T.accent}15)",
        on_mount=ResetPasswordState.on_load,
    )
