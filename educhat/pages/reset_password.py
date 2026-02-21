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
    
    def set_token_from_hash(self, data: str):
        """Set token or error from URL hash (extracted via rx.call_script callback)."""
        data_str = str(data) if data is not None else ""

        print(f"\n{'='*60}")
        print(f"[RESET PASSWORD - TOKEN EXTRACTION] Received from JavaScript:")
        print(f"  - Data string: {data_str[:100] if data_str else 'Empty/None'}...")
        print(f"  - Data length: {len(data_str) if data_str else 0}")
        print(f"{'='*60}\n")

        # If no data received or empty string, ignore it
        if not data_str or data_str in ("None", "null", "undefined") or data_str.strip() == "":
            print("[RESET PASSWORD] ⚠️  No data in hash - page opened directly or waiting for token")
            return

        # Parse the data (format: "token:xxx" or "error:xxx")
        if data_str.startswith("token:"):
            token = data_str[6:]  # Remove "token:" prefix
            print(f"[RESET PASSWORD] 🔍 Extracted token from data:")
            print(f"  - Token length: {len(token) if token else 0}")
            print(f"  - Token prefix: {token[:30] if token else 'N/A'}...")

            if token and len(token) >= 4:  # Accept any non-trivial token
                self.reset_token = token
                self.reset_error = ""
                print(f"[RESET PASSWORD] ✅ Token set successfully!")
                print(f"  - State token length: {len(self.reset_token)}")
                print(f"  - State token prefix: {self.reset_token[:30]}...")
            else:
                print(f"[RESET PASSWORD] ❌ Invalid token length: {len(token) if token else 0}")
                self.reset_error = "Ongeldige reset link. Vraag een nieuwe aan."
        elif data_str.startswith("error:"):
            error_info = data_str[6:]  # Remove "error:" prefix
            print(f"[RESET PASSWORD] ❌ Error from Supabase: {error_info}")

            # Parse different error types
            if "otp_expired" in error_info or "expired" in error_info.lower():
                self.reset_error = "De reset link is verlopen. Vraag een nieuwe reset link aan."
            elif "invalid" in error_info.lower() or "invalid_token_type" in error_info:
                self.reset_error = "De reset link is ongeldig. Vraag een nieuwe reset link aan."
            else:
                self.reset_error = "Er is een probleem met de reset link. Vraag een nieuwe aan."
        else:
            print(f"[RESET PASSWORD] ❌ Unknown data format: {data_str}")
            self.reset_error = "Ongeldige URL. Gebruik de link uit je e-mail."

    def on_load(self):
        """Extract token from URL hash on page load using rx.call_script callback."""
        print("[RESET PASSWORD] Page loading, extracting token via call_script...")
        js_code = (
            "(function(){"
            "var hash=window.location.hash;"
            "console.log('[RESET PASSWORD] call_script hash: '+hash);"
            "if(!hash||hash.length<=1){return null;}"
            "var p=new URLSearchParams(hash.slice(1));"
            "var err=p.get('error'),errCode=p.get('error_code'),errDesc=p.get('error_description');"
            "var tok=p.get('access_token'),type=p.get('type');"
            "console.log('[RESET PASSWORD] tok='+tok+' type='+type);"
            "if(err){return 'error:'+(errCode||err)+':'+(errDesc||'');}"
            "if(tok&&type==='recovery'){return 'token:'+tok;}"
            "if(tok){return 'error:invalid_token_type';}"
            "return null;"
            "})()"
        )
        return rx.call_script(js_code, callback=ResetPasswordState.set_token_from_hash)
    
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
        
        print(f"\n{'='*60}")
        print(f"[RESET PASSWORD - VALIDATION] Starting form validation:")
        print(f"  - New password length: {len(self.new_password) if self.new_password else 0}")
        print(f"  - Confirm password length: {len(self.confirm_new_password) if self.confirm_new_password else 0}")
        print(f"  - Reset token length: {len(self.reset_token) if self.reset_token else 0}")
        print(f"  - Reset token value: {self.reset_token[:30] if self.reset_token else 'EMPTY/NONE'}...")
        print(f"{'='*60}\n")
        
        # Validate new password
        if not self.new_password or not self.new_password.strip():
            self.new_password_error = "Wachtwoord is verplicht"
            is_valid = False
            print("[VALIDATION] ❌ New password is empty")
        elif len(self.new_password) < 8:
            self.new_password_error = "Wachtwoord moet minimaal 8 tekens bevatten"
            is_valid = False
            print("[VALIDATION] ❌ New password too short")
        
        # Validate confirm password
        if not self.confirm_new_password:
            self.confirm_new_password_error = "Bevestig je wachtwoord"
            is_valid = False
            print("[VALIDATION] ❌ Confirm password is empty")
        elif self.new_password != self.confirm_new_password:
            self.confirm_new_password_error = "Wachtwoorden komen niet overeen"
            is_valid = False
            print("[VALIDATION] ❌ Passwords don't match")
        
        # Check token
        if not self.reset_token:
            self.reset_error = "Geen reset token gevonden"
            is_valid = False
            print("[VALIDATION] ❌ NO RESET TOKEN FOUND - This is the main issue!")
            print(f"  - Token value: '{self.reset_token}'")
            print(f"  - Token type: {type(self.reset_token)}")
        else:
            print(f"[VALIDATION] ✅ Reset token present: {len(self.reset_token)} chars")
        
        print(f"\n[VALIDATION] Final result: {'✅ VALID' if is_valid else '❌ INVALID'}\n")
        return is_valid
    
    async def reset_password_with_token(self):
        """Reset password using the token from email."""
        print(f"\n{'='*60}")
        print(f"[RESET PASSWORD - SUBMIT] Form submitted!")
        print(f"  - Current token: {self.reset_token[:30] if self.reset_token else 'NONE'}...")
        print(f"  - Token length: {len(self.reset_token) if self.reset_token else 0}")
        print(f"{'='*60}\n")
        
        # Clear errors
        self.new_password_error = ""
        self.confirm_new_password_error = ""
        self.reset_error = ""
        
        # Validate form
        if not self._validate_reset_form():
            print("[RESET PASSWORD] ❌ Validation failed, aborting submission")
            return
        
        self.reset_loading = True
        yield
        
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            print(f"[RESET PASSWORD] 🚀 Calling auth service with token: {self.reset_token[:30]}...")
            
            # Update password with token
            result = await auth_service.update_password_with_token(
                self.reset_token,
                self.new_password
            )
            
            print(f"[RESET PASSWORD] 📥 Auth service result: {result}")
            
            if result.get("success"):
                self.reset_success = True
                self.toast_message = "Wachtwoord succesvol gewijzigd! Je wordt doorgestuurd..."
                self.toast_type = "success"
                self.show_toast = True
                print("[RESET PASSWORD] ✅ Password reset successful!")
                
                # Wait a moment then redirect to login
                yield
                import asyncio
                await asyncio.sleep(2)
                yield rx.redirect("/")
            else:
                error_msg = result.get("error", "Kon wachtwoord niet wijzigen. Probeer opnieuw.")
                self.reset_error = error_msg
                print(f"[RESET PASSWORD] ❌ Password reset failed: {error_msg}")
        
        except Exception as e:
            print(f"[RESET PASSWORD] 💥 Exception during password reset: {e}")
            import traceback
            traceback.print_exc()
            self.reset_error = "Er is een fout opgetreden. Probeer het opnieuw."
        
        finally:
            self.reset_loading = False


def reset_password_page() -> rx.Component:
    """Password reset page component with modern design."""
    return rx.box(
        # Background with gradient
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            background="linear-gradient(135deg, rgba(16, 163, 127, 0.05) 0%, rgba(13, 138, 107, 0.08) 100%)",
            z_index="-1",
        ),
        
        # Main centered card
        rx.box(
            # Modern card container
            rx.box(
                # Logo with animation
                rx.box(
                    rx.box(
                        rx.icon("graduation-cap", size=40, color="white"),
                        width="72px",
                        height="72px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background="linear-gradient(135deg, #10A37F 0%, #0D8F6F 100%)",
                        border_radius="18px",
                        box_shadow="0 8px 24px rgba(16, 163, 127, 0.25)",
                        margin="0 auto 24px",
                    ),
                    text_align="center",
                ),
                
                # Header
                rx.heading(
                    "Wachtwoord Opnieuw Instellen",
                    size="7",
                    font_weight="700",
                    color=T.text_primary,
                    text_align="center",
                    margin_bottom="8px",
                ),
                rx.text(
                    "Voer je nieuwe wachtwoord in om verder te gaan",
                    font_size="15px",
                    color=T.text_secondary,
                    text_align="center",
                    margin_bottom="16px",
                    line_height="1.6",
                ),
                
                # Debug token status indicator (helpful for troubleshooting)
                rx.box(
                    rx.box(
                        rx.icon(
                            rx.cond(
                                ResetPasswordState.reset_token != "",
                                "circle-check",
                                "circle-x"
                            ),
                            size=16,
                            color=rx.cond(
                                ResetPasswordState.reset_token != "",
                                "#10A37F",
                                "#DC2626"
                            ),
                        ),
                        rx.text(
                            rx.cond(
                                ResetPasswordState.reset_token != "",
                                "Reset token geladen",
                                "Wachten op reset token..."
                            ),
                            font_size="13px",
                            color=T.text_tertiary,
                            font_weight="500",
                        ),
                        display="flex",
                        align_items="center",
                        gap="8px",
                    ),
                    padding="12px 16px",
                    background=rx.cond(
                        ResetPasswordState.reset_token != "",
                        "rgba(16, 163, 127, 0.08)",
                        "rgba(220, 38, 38, 0.08)"
                    ),
                    border=rx.cond(
                        ResetPasswordState.reset_token != "",
                        "1px solid rgba(16, 163, 127, 0.2)",
                        "1px solid rgba(220, 38, 38, 0.2)"
                    ),
                    border_radius="10px",
                    margin_bottom="24px",
                    text_align="center",
                ),
                
                # Success message with animation
                rx.cond(
                    ResetPasswordState.reset_success,
                    rx.box(
                        rx.box(
                            rx.icon("circle-check", size=64, color="#10A37F"),
                            margin_bottom="20px",
                        ),
                        rx.heading(
                            "Wachtwoord Gewijzigd!",
                            size="6",
                            font_weight="700",
                            color=T.text_primary,
                            margin_bottom="12px",
                        ),
                        rx.text(
                            "Je wachtwoord is succesvol gewijzigd.",
                            font_size="15px",
                            color=T.text_secondary,
                            margin_bottom="8px",
                        ),
                        rx.text(
                            "Je wordt doorgestuurd naar de inlogpagina...",
                            font_size="14px",
                            color=T.text_tertiary,
                        ),
                        text_align="center",
                        padding="48px 32px",
                        animation="fadeIn 0.5s ease-out",
                    ),
                    # Reset form
                    rx.box(
                        # Error message with better styling
                        rx.cond(
                            ResetPasswordState.reset_error != "",
                            rx.box(
                                rx.box(
                                    rx.icon("triangle-alert", size=20, color="#DC2626"),
                                    width="40px",
                                    height="40px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    background="rgba(220, 38, 38, 0.1)",
                                    border_radius="10px",
                                    flex_shrink="0",
                                ),
                                rx.text(
                                    ResetPasswordState.reset_error,
                                    font_size="14px",
                                    color="#DC2626",
                                    font_weight="500",
                                    line_height="1.5",
                                ),
                                display="flex",
                                align_items="center",
                                gap="14px",
                                padding="16px 20px",
                                background="rgba(220, 38, 38, 0.08)",
                                border="1px solid rgba(220, 38, 38, 0.2)",
                                border_radius="12px",
                                margin_bottom="24px",
                            ),
                        ),
                        
                        # New password field with modern styling
                        rx.box(
                            rx.text(
                                "Nieuw Wachtwoord",
                                font_size="14px",
                                font_weight="600",
                                margin_bottom="10px",
                                color=T.text_primary,
                            ),
                            rx.box(
                                rx.icon("lock", size=20, color="#6B7280"),
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
                                    background="transparent",
                                    flex="1",
                                    font_size="15px",
                                    color=T.text_primary,
                                ),
                                rx.icon(
                                    rx.cond(
                                        ResetPasswordState.show_new_password,
                                        "eye-off",
                                        "eye"
                                    ),
                                    size=20,
                                    color="#6B7280",
                                    cursor="pointer",
                                    on_click=ResetPasswordState.toggle_new_password,
                                    _hover={"color": "#10A37F"},
                                ),
                                display="flex",
                                align_items="center",
                                gap="12px",
                                padding="14px 16px",
                                border=f"2px solid {rx.cond(ResetPasswordState.new_password_error != '', '#DC2626', 'rgba(0, 0, 0, 0.1)')}",
                                border_radius="12px",
                                background=T.bg_input,
                                transition="all 0.2s ease",
                                _focus_within={
                                    "border_color": "#10A37F",
                                    "box_shadow": "0 0 0 3px rgba(16, 163, 127, 0.1)",
                                },
                            ),
                            rx.cond(
                                ResetPasswordState.new_password_error != "",
                                rx.text(
                                    ResetPasswordState.new_password_error,
                                    font_size="13px",
                                    color="#DC2626",
                                    margin_top="8px",
                                    font_weight="500",
                                ),
                            ),
                            margin_bottom="20px",
                        ),
                        
                        # Confirm password field with modern styling
                        rx.box(
                            rx.text(
                                "Bevestig Wachtwoord",
                                font_size="14px",
                                font_weight="600",
                                margin_bottom="10px",
                                color=T.text_primary,
                            ),
                            rx.box(
                                rx.icon("lock-keyhole", size=20, color="#6B7280"),
                                rx.input(
                                    type=rx.cond(
                                        ResetPasswordState.show_confirm_new_password,
                                        "text",
                                        "password"
                                    ),
                                    placeholder="Herhaal je wachtwoord",
                                    value=ResetPasswordState.confirm_new_password,
                                    on_change=ResetPasswordState.set_confirm_new_password,
                                    border="none",
                                    outline="none",
                                    background="transparent",
                                    flex="1",
                                    font_size="15px",
                                    color=T.text_primary,
                                ),
                                rx.icon(
                                    rx.cond(
                                        ResetPasswordState.show_confirm_new_password,
                                        "eye-off",
                                        "eye"
                                    ),
                                    size=20,
                                    color="#6B7280",
                                    cursor="pointer",
                                    on_click=ResetPasswordState.toggle_confirm_new_password,
                                    _hover={"color": "#10A37F"},
                                ),
                                display="flex",
                                align_items="center",
                                gap="12px",
                                padding="14px 16px",
                                border=f"2px solid {rx.cond(ResetPasswordState.confirm_new_password_error != '', '#DC2626', 'rgba(0, 0, 0, 0.1)')}",
                                border_radius="12px",
                                background=T.bg_input,
                                transition="all 0.2s ease",
                                _focus_within={
                                    "border_color": "#10A37F",
                                    "box_shadow": "0 0 0 3px rgba(16, 163, 127, 0.1)",
                                },
                            ),
                            rx.cond(
                                ResetPasswordState.confirm_new_password_error != "",
                                rx.text(
                                    ResetPasswordState.confirm_new_password_error,
                                    font_size="13px",
                                    color="#DC2626",
                                    margin_top="8px",
                                    font_weight="500",
                                ),
                            ),
                            margin_bottom="28px",
                        ),
                        
                        # Submit button with modern styling
                        rx.button(
                            rx.cond(
                                ResetPasswordState.reset_loading,
                                rx.hstack(
                                    rx.spinner(size="3", color="white"),
                                    rx.text("Bezig met wijzigen...", font_size="15px", font_weight="600"),
                                    spacing="2",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.icon("key", size=20, color="white"),
                                    rx.text("Wachtwoord Wijzigen", font_size="15px", font_weight="600"),
                                    spacing="2",
                                    align="center",
                                ),
                            ),
                            on_click=ResetPasswordState.reset_password_with_token,
                            disabled=ResetPasswordState.reset_loading,
                            width="100%",
                            padding="16px 24px",
                            background="linear-gradient(135deg, #10A37F 0%, #0D8F6F 100%)",
                            color="white",
                            border="none",
                            border_radius="12px",
                            cursor=rx.cond(ResetPasswordState.reset_loading, "not-allowed", "pointer"),
                            font_size="15px",
                            font_weight="600",
                            transition="all 0.3s ease",
                            box_shadow="0 4px 12px rgba(16, 163, 127, 0.2)",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 6px 20px rgba(16, 163, 127, 0.3)",
                            },
                            _active={
                                "transform": "translateY(0)",
                            },
                            margin_bottom="24px",
                        ),
                        
                        # Back to login link
                        rx.box(
                            rx.link(
                                rx.hstack(
                                    rx.icon("arrow-left", size=16, color="#10A37F"),
                                    rx.text(
                                        "Terug naar inloggen",
                                        font_size="14px",
                                        font_weight="600",
                                        color="#10A37F",
                                    ),
                                    spacing="2",
                                    align="center",
                                ),
                                href="/",
                                display="flex",
                                justify_content="center",
                                transition="all 0.2s ease",
                                _hover={
                                    "opacity": "0.8",
                                },
                            ),
                        ),
                    ),
                ),
                
                max_width="500px",
                width="100%",
                margin="0 auto",
                padding="48px 40px",
                background=rx.color_mode_cond(
                    light="#FFFFFF",
                    dark="#111217"
                ),
                border=rx.color_mode_cond(
                    light="1px solid rgba(0, 0, 0, 0.05)",
                    dark="1px solid #2d3039"
                ),
                border_radius="20px",
                box_shadow=rx.color_mode_cond(
                    light="0 20px 60px rgba(0, 0, 0, 0.08)",
                    dark="0 20px 60px rgba(0, 0, 0, 0.3)"
                ),
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            min_height="100vh",
            padding="24px",
            on_mount=ResetPasswordState.on_load,
        ),
    )
