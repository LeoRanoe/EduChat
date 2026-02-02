"""Mobile navigation components for EduChat."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, T


def hamburger_button(
    on_click=None,
    is_open: bool = False,
) -> rx.Component:
    """Hamburger menu button for mobile navigation.
    
    Args:
        on_click: Click handler to toggle sidebar
        is_open: Whether sidebar is currently open
    """
    return rx.button(
        rx.cond(
            is_open,
            # Close icon (X)
            rx.box(
                rx.box(
                    width="20px",
                    height="2px",
                    background=T.text_secondary,
                    transform="rotate(45deg) translateY(0px)",
                    transition="all 0.3s ease",
                ),
                rx.box(
                    width="20px",
                    height="2px",
                    background=T.text_secondary,
                    transform="rotate(-45deg) translateY(0px)",
                    margin_top="-2px",
                    transition="all 0.3s ease",
                ),
                display="flex",
                flex_direction="column",
                align_items="center",
                justify_content="center",
            ),
            # Hamburger icon (three lines)
            rx.box(
                rx.box(
                    width="20px",
                    height="2px",
                    background=T.text_secondary,
                    margin_bottom="4px",
                    transition="all 0.3s ease",
                ),
                rx.box(
                    width="20px",
                    height="2px",
                    background=T.text_secondary,
                    margin_bottom="4px",
                    transition="all 0.3s ease",
                ),
                rx.box(
                    width="20px",
                    height="2px",
                    background=T.text_secondary,
                    transition="all 0.3s ease",
                ),
                display="flex",
                flex_direction="column",
                align_items="center",
                justify_content="center",
            ),
        ),
        on_click=on_click,
        background="transparent",
        border="none",
        padding="0.5rem",
        cursor="pointer",
        display="flex",
        align_items="center",
        justify_content="center",
        _hover={
            "background": T.bg_hover,
        },
        border_radius=RADIUS["sm"],
        width="40px",
        height="40px",
    )


def mobile_header(
    on_menu_click=None,
    is_sidebar_open: bool = False,
) -> rx.Component:
    """Mobile header with hamburger menu.
    
    Args:
        on_menu_click: Click handler for menu button
        is_sidebar_open: Whether sidebar is currently open
    """
    return rx.box(
        rx.hstack(
            hamburger_button(
                on_click=on_menu_click,
                is_open=is_sidebar_open,
            ),
            rx.text(
                "EduChat",
                font_size="1.25rem",
                font_weight="600",
                color=T.text_primary,
            ),
            spacing="3",
            align="center",
        ),
        padding="1rem",
        border_bottom=f"1px solid {T.border}",
        background=T.bg_card,
        width="100%",
        position="sticky",
        top="0",
        z_index="100",
    )


def sidebar_overlay(
    is_open: bool = False,
    on_click=None,
) -> rx.Component:
    """Dark overlay for mobile sidebar.
    
    Args:
        is_open: Whether overlay should be visible
        on_click: Click handler to close sidebar
    """
    return rx.box(
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        height="100vh",
        background=T.overlay,
        z_index="999",
        display=rx.cond(is_open, "block", "none"),
        on_click=on_click,
        # Hide on desktop
        **{
            "@media (min-width: 1024px)": {
                "display": "none !important",
            }
        }
    )

