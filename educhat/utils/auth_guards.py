"""Route protection and authentication guards."""

import reflex as rx
from educhat.state.auth_state import AuthState


def require_auth(component_fn):
    """
    Decorator to protect routes requiring authentication.
    Redirects to landing page if not authenticated.
    
    Usage:
        @require_auth
        def protected_page():
            return rx.text("Protected content")
    """
    def wrapper(*args, **kwargs):
        return rx.cond(
            AuthState.is_authenticated | AuthState.is_guest,
            component_fn(*args, **kwargs),
            rx.redirect("/"),
        )
    return wrapper


def guest_restricted(component_fn):
    """
    Decorator to restrict features for guest users.
    Shows upgrade prompt if guest tries to access.
    
    Usage:
        @guest_restricted
        def premium_feature():
            return rx.text("Premium content")
    """
    def wrapper(*args, **kwargs):
        return rx.cond(
            AuthState.is_authenticated & ~AuthState.is_guest,
            component_fn(*args, **kwargs),
            upgrade_prompt(),
        )
    return wrapper


def upgrade_prompt() -> rx.Component:
    """Show prompt encouraging guest users to sign up."""
    return rx.box(
        rx.box(
            rx.icon(
                tag="lock",
                size=48,
                color="#6366f1",
                margin_bottom="16px",
            ),
            rx.heading(
                "Sign up to unlock this feature",
                size="7",
                margin_bottom="12px",
                color="#1a202c",
            ),
            rx.text(
                "Create a free account to save your conversations, access history, and more!",
                color="#64748b",
                font_size="16px",
                margin_bottom="24px",
                text_align="center",
            ),
            rx.button(
                "Create Free Account",
                padding="12px 24px",
                background="#6366f1",
                color="white",
                border="none",
                border_radius="8px",
                cursor="pointer",
                font_weight="600",
                _hover={
                    "background": "#4f46e5",
                },
                on_click=AuthState.toggle_auth_modal,
            ),
            display="flex",
            flex_direction="column",
            align_items="center",
            text_align="center",
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        padding="48px",
        background="white",
        border_radius="12px",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
        margin="32px auto",
        max_width="500px",
    )

