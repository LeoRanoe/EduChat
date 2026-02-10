"""
Email confirmation page for EduChat.
Allows users to resend confirmation emails and provides status updates.
"""

import reflex as rx
from educhat.state.auth_state import AuthState


class EmailConfirmationState(AuthState):
    """State for email confirmation page."""
    
    # UI state
    email: str = ""
    is_loading: bool = False
    show_success: bool = False
    show_error: bool = False
    error_message: str = ""
    success_message: str = ""
    countdown: int = 0
    can_resend: bool = True
    
    def set_email_from_url(self, email_param: str):
        """Set email from URL parameter."""
        if email_param:
            self.email = email_param
            print(f"[EMAIL CONFIRM] Email set from URL: {email_param}")
    
    async def resend_confirmation_email(self):
        """Resend confirmation email to the user."""
        if not self.can_resend:
            return
            
        if not self.email or not self.email.strip():
            self.show_error = True
            self.error_message = "Vul je e-mailadres in"
            return
        
        self.is_loading = True
        self.show_error = False
        self.show_success = False
        
        try:
            result = await self.auth_service.resend_confirmation(self.email)
            
            if result.get("success"):
                self.show_success = True
                self.success_message = result.get("message", "Bevestigingsmail verzonden!")
                self.can_resend = False
                self.countdown = 60
                
                # Start countdown
                yield
                
                # Reset countdown after 60 seconds
                import asyncio
                for i in range(60, 0, -1):
                    await asyncio.sleep(1)
                    self.countdown = i
                    yield
                
                self.can_resend = True
                self.countdown = 0
                
            else:
                self.show_error = True
                self.error_message = result.get("error", "Er is iets misgegaan")
                
        except Exception as e:
            print(f"[EMAIL CONFIRM] Error: {str(e)}")
            self.show_error = True
            self.error_message = "Er is een fout opgetreden. Probeer het later opnieuw."
        finally:
            self.is_loading = False


def confirmation_card() -> rx.Component:
    """Main card for email confirmation interface."""
    return rx.box(
        # Email icon with gradient background
        rx.box(
            rx.html(
                """
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="url(#gradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <polyline points="22,6 12,13 2,6" stroke="url(#gradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <defs>
                        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#10A37F;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#0E9B6F;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                </svg>
                """
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            width="80px",
            height="80px",
            border_radius="50%",
            background="linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(14, 155, 111, 0.1) 100%)",
            margin="0 auto 24px auto",
        ),
        
        # Heading
        rx.heading(
            "Bevestig Je E-mailadres",
            size="7",
            font_weight="700",
            text_align="center",
            margin_bottom="12px",
            background="linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
            background_clip="text",
            style={
                "-webkit-background-clip": "text",
                "-webkit-text-fill-color": "transparent",
            },
        ),
        
        # Description
        rx.text(
            "We hebben je een bevestigingsmail gestuurd. Klik op de link in de email om je account te activeren.",
            font_size="15px",
            color="#666",
            text_align="center",
            line_height="1.6",
            margin_bottom="32px",
        ),
        
        # Email input
        rx.box(
            rx.input(
                placeholder="jouw@email.com",
                value=EmailConfirmationState.email,
                on_change=EmailConfirmationState.set_email,
                type="email",
                width="100%",
                padding="14px 16px",
                border="2px solid #e0e0e0",
                border_radius="12px",
                font_size="15px",
                color="#1a1a1a",
                background="#fff",
                transition="all 0.2s ease",
                _focus={
                    "outline": "none",
                    "border_color": "#10A37F",
                    "box_shadow": "0 0 0 3px rgba(16, 163, 127, 0.1)",
                },
                _hover={"border_color": "#10A37F"},
            ),
            margin_bottom="24px",
        ),
        
        # Success message
        rx.cond(
            EmailConfirmationState.show_success,
            rx.box(
                rx.hstack(
                    rx.html(
                        """
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke="#10A37F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            <polyline points="22 4 12 14.01 9 11.01" stroke="#10A37F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        """
                    ),
                    rx.text(
                        EmailConfirmationState.success_message,
                        font_size="14px",
                        color="#0e7c5d",
                        font_weight="500",
                    ),
                    spacing="3",
                    align_items="center",
                ),
                padding="14px 18px",
                background="linear-gradient(135deg, rgba(16, 163, 127, 0.08) 0%, rgba(14, 155, 111, 0.08) 100%)",
                border="1px solid rgba(16, 163, 127, 0.2)",
                border_radius="10px",
                margin_bottom="20px",
                animation="fadeIn 0.3s ease-in",
            ),
        ),
        
        # Error message
        rx.cond(
            EmailConfirmationState.show_error,
            rx.box(
                rx.hstack(
                    rx.html(
                        """
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="10" stroke="#ef4444" stroke-width="2"/>
                            <line x1="12" y1="8" x2="12" y2="12" stroke="#ef4444" stroke-width="2" stroke-linecap="round"/>
                            <line x1="12" y1="16" x2="12.01" y2="16" stroke="#ef4444" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                        """
                    ),
                    rx.text(
                        EmailConfirmationState.error_message,
                        font_size="14px",
                        color="#dc2626",
                        font_weight="500",
                    ),
                    spacing="3",
                    align_items="center",
                ),
                padding="14px 18px",
                background="rgba(239, 68, 68, 0.05)",
                border="1px solid rgba(239, 68, 68, 0.2)",
                border_radius="10px",
                margin_bottom="20px",
                animation="fadeIn 0.3s ease-in",
            ),
        ),
        
        # Resend button
        rx.button(
            rx.cond(
                EmailConfirmationState.is_loading,
                rx.hstack(
                    rx.spinner(size="3", color="white"),
                    rx.text("Verzenden...", font_size="15px", font_weight="600"),
                    spacing="3",
                    align_items="center",
                ),
                rx.cond(
                    EmailConfirmationState.can_resend,
                    rx.hstack(
                        rx.html(
                            """
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <polyline points="23 4 23 10 17 10" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            """
                        ),
                        rx.text("Opnieuw Verzenden", font_size="15px", font_weight="600"),
                        spacing="2",
                        align_items="center",
                    ),
                    rx.hstack(
                        rx.html(
                            """
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2"/>
                                <polyline points="12 6 12 12 16 14" stroke="white" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                            """
                        ),
                        rx.text(
                            f"Wacht {EmailConfirmationState.countdown}s",
                            font_size="15px",
                            font_weight="600",
                        ),
                        spacing="2",
                        align_items="center",
                    ),
                ),
            ),
            on_click=EmailConfirmationState.resend_confirmation_email,
            width="100%",
            padding="14px 24px",
            background=rx.cond(
                EmailConfirmationState.can_resend,
                "linear-gradient(135deg, #10A37F 0%, #0E9B6F 100%)",
                "linear-gradient(135deg, #9ca3af 0%, #6b7280 100%)",
            ),
            color="white",
            border="none",
            border_radius="12px",
            font_size="15px",
            font_weight="600",
            cursor=rx.cond(EmailConfirmationState.can_resend, "pointer", "not-allowed"),
            transition="all 0.2s ease",
            disabled=~EmailConfirmationState.can_resend | EmailConfirmationState.is_loading,
            _hover={
                "transform": rx.cond(EmailConfirmationState.can_resend, "translateY(-1px)", "none"),
                "box_shadow": rx.cond(
                    EmailConfirmationState.can_resend,
                    "0 10px 20px rgba(16, 163, 127, 0.2)",
                    "none"
                ),
            },
            _active={"transform": "translateY(0)"},
        ),
        
        # Helper text
        rx.box(
            rx.text(
                "📩",
                font_size="16px",
                display="inline",
                margin_right="8px",
            ),
            rx.text(
                "Geen email ontvangen? Check je spam folder of vraag een nieuwe aan.",
                font_size="13px",
                color="#999",
                display="inline",
            ),
            text_align="center",
            margin_top="24px",
            padding="16px",
            background="rgba(0, 0, 0, 0.02)",
            border_radius="10px",
        ),
        
        # Back to login link
        rx.link(
            rx.hstack(
                rx.html(
                    """
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <line x1="19" y1="12" x2="5" y2="12" stroke="#10A37F" stroke-width="2" stroke-linecap="round"/>
                        <polyline points="12 19 5 12 12 5" stroke="#10A37F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    """
                ),
                rx.text(
                    "Terug naar login",
                    font_size="14px",
                    font_weight="600",
                    color="#10A37F",
                ),
                spacing="2",
                align_items="center",
                justify_content="center",
            ),
            href="/",
            text_decoration="none",
            display="block",
            text_align="center",
            margin_top="24px",
            padding="12px",
            border_radius="8px",
            transition="all 0.2s ease",
            _hover={
                "background": "rgba(16, 163, 127, 0.05)",
            },
        ),
        
        width="100%",
        max_width="500px",
        background="white",
        padding="48px",
        border_radius="20px",
        box_shadow="0 20px 60px rgba(0, 0, 0, 0.08), 0 8px 24px rgba(0, 0, 0, 0.05)",
        margin="0 auto",
    )


@rx.page(route="/auth/confirm-email", title="Bevestig Email - EduChat")
def confirm_email() -> rx.Component:
    """Email confirmation page."""
    return rx.fragment(
        # CSS animations
        rx.html(
            """
            <style>
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            </style>
            """
        ),
        
        rx.box(
            confirmation_card(),
            min_height="100vh",
            display="flex",
            align_items="center",
            justify_content="center",
            padding="24px",
            background="linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)",
            background_size="200% 200%",
            animation="gradient 15s ease infinite",
        ),
        
        # Extract email from URL on mount
        rx.script(
            """
            // Get email from URL parameter on page load
            const urlParams = new URLSearchParams(window.location.search);
            const email = urlParams.get('email');
            if (email) {
                console.log('[EMAIL CONFIRM] Found email in URL:', email);
                // Send email to Reflex state
                window.dispatchEvent(new Event('set_email_from_url:' + email));
            }
            """
        ),
    )
