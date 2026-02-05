"""
Email Confirmation Banner Component
Shows a persistent banner for users who need to confirm their email.
"""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.styles.theme import ThemeTokens as T


def email_confirmation_banner() -> rx.Component:
    """Banner prompting user to confirm their email address."""
    return rx.cond(
        # Only show if user is authenticated but email needs confirmation
        AuthState.is_authenticated & AuthState.email_needs_confirmation,
        rx.box(
            rx.box(
                # Icon
                rx.icon(
                    "mail",
                    size=20,
                    color=T.warning,
                ),
                
                # Message text
                rx.box(
                    rx.text(
                        "Bevestig je e-mailadres",
                        font_weight="600",
                        font_size="14px",
                        color=T.text_primary,
                        margin_bottom="2px",
                    ),
                    rx.text(
                        rx.text(
                            "We hebben een bevestigingsmail gestuurd naar ",
                            display="inline",
                        ),
                        rx.text(
                            AuthState.pending_confirmation_email,
                            font_weight="600",
                            display="inline",
                        ),
                        rx.text(
                            ". Check je inbox en spam folder.",
                            display="inline",
                        ),
                        font_size="13px",
                        color=T.text_secondary,
                    ),
                    flex="1",
                ),
                
                # Actions
                rx.box(
                    rx.button(
                        rx.cond(
                            AuthState.resending_confirmation,
                            rx.spinner(size="2"),
                            "Opnieuw verzenden",
                        ),
                        on_click=AuthState.resend_confirmation_email,
                        disabled=AuthState.resending_confirmation,
                        size="2",
                        variant="soft",
                        color_scheme="amber",
                    ),
                    rx.button(
                        rx.icon("x", size=16),
                        on_click=AuthState.set_email_needs_confirmation(False),
                        size="1",
                        variant="ghost",
                        color_scheme="gray",
                    ),
                    display="flex",
                    align_items="center",
                    gap="8px",
                ),
                
                display="flex",
                align_items="center",
                gap="16px",
                padding="16px 20px",
                background=f"{T.warning}15",
                border_left=f"4px solid {T.warning}",
                border_radius="8px",
                margin_bottom="20px",
            ),
            width="100%",
            animation="slideDown 0.3s ease-out",
        ),
    )


def email_confirmation_modal() -> rx.Component:
    """Modal for email confirmation status and resend option."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.box(
                    rx.icon("mail-check", size=24, color=T.primary),
                    "Bevestig je e-mailadres",
                    display="flex",
                    align_items="center",
                    gap="12px",
                ),
            ),
            
            rx.dialog.description(
                rx.box(
                    rx.text(
                        "We hebben een bevestigingsmail gestuurd naar:",
                        margin_bottom="8px",
                    ),
                    rx.text(
                        AuthState.pending_confirmation_email,
                        font_weight="600",
                        color=T.primary,
                        margin_bottom="16px",
                    ),
                    rx.text(
                        "Klik op de link in de e-mail om je account te activeren. Check ook je spam folder als je de mail niet ziet.",
                        color=T.text_secondary,
                        margin_bottom="24px",
                    ),
                    
                    # Resend button
                    rx.button(
                        rx.cond(
                            AuthState.resending_confirmation,
                            rx.box(
                                rx.spinner(size="2"),
                                rx.text("Verzenden...", margin_left="8px"),
                                display="flex",
                                align_items="center",
                            ),
                            rx.box(
                                rx.icon("send", size=16),
                                rx.text("E-mail opnieuw verzenden", margin_left="8px"),
                                display="flex",
                                align_items="center",
                            ),
                        ),
                        on_click=AuthState.resend_confirmation_email,
                        disabled=AuthState.resending_confirmation,
                        width="100%",
                        variant="soft",
                    ),
                ),
            ),
            
            rx.dialog.close(
                rx.button(
                    "Sluiten",
                    variant="outline",
                    width="100%",
                    margin_top="16px",
                ),
            ),
            
            max_width="450px",
        ),
        
        open=AuthState.email_needs_confirmation & AuthState.show_email_confirmation_modal,
    )
