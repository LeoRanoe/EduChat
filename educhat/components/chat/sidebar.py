"""Sidebar component for EduChat.

Professional sidebar with:
- Collapsible design for desktop
- Smooth slide animation for mobile
- Conversation grouping by date
- Search functionality
- User profile section
- Skeleton loading states
"""

import reflex as rx
from typing import List, Dict
from educhat.styles.theme import COLORS, RADIUS, SHADOWS, TRANSITIONS
from educhat.components.shared import logo, secondary_button, search_input, avatar
from educhat.state.app_state import AppState
from educhat.state.auth_state import AuthState


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

SIDEBAR_CONFIG = {
    "width_expanded": "280px",
    "width_collapsed": "72px",
    "mobile_width": "300px",
    "z_index_mobile": "1001",
}


# ============================================================================
# CONVERSATION ITEM COMPONENT
# ============================================================================


def render_conversation_item(conv, current_id):
    """Render a single conversation item with professional styling.
    
    Args:
        conv: Conversation dict with 'id' and 'title' (Reflex Var)
        current_id: Currently active conversation ID (Reflex Var)
    """
    conv_id = conv["id"]
    conv_title = conv["title"]
    is_active = conv_id == current_id
    
    return rx.box(
        rx.hstack(
            # Icon with gradient background when active
            rx.box(
                rx.icon(
                    "message-circle",
                    size=14,
                    color=rx.cond(
                        is_active,
                        "white",
                        COLORS["text_tertiary"]
                    ),
                ),
                background=rx.cond(
                    is_active,
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    COLORS["light_gray"]
                ),
                padding="0.375rem",
                border_radius=RADIUS["md"],
                flex_shrink="0",
                transition=TRANSITIONS["fast"],
            ),
            # Title with ellipsis
            rx.text(
                conv_title,
                font_size="0.8125rem",
                color=rx.cond(
                    is_active,
                    COLORS["primary_green"],
                    COLORS["text_primary"]
                ),
                font_weight=rx.cond(
                    is_active,
                    "600",
                    "400"
                ),
                overflow="hidden",
                text_overflow="ellipsis",
                white_space="nowrap",
                flex="1",
                min_width="0",
                line_height="1.4",
            ),
            # Delete button (visible on hover)
            rx.box(
                rx.icon("trash-2", size=12, color=COLORS["text_tertiary"]),
                on_click=lambda: AppState.delete_conversation(conv_id),
                cursor="pointer",
                padding="0.375rem",
                border_radius=RADIUS["sm"],
                opacity="0",
                class_name="conv-delete-btn",
                transition=TRANSITIONS["fast"],
                _hover={
                    "background": f"rgba(239, 68, 68, 0.1)",
                    "color": COLORS["error"],
                },
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        background=rx.cond(
            is_active,
            f"rgba(16, 163, 127, 0.08)",
            "transparent"
        ),
        border_radius=RADIUS["lg"],
        padding="0.5rem 0.625rem",
        margin_bottom="0.125rem",
        cursor="pointer",
        on_click=AppState.load_conversation(conv_id),
        border_left=rx.cond(
            is_active,
            f"3px solid {COLORS['primary_green']}",
            "3px solid transparent"
        ),
        transition=TRANSITIONS["fast"],
        _hover={
            "background": rx.cond(
                is_active,
                f"rgba(16, 163, 127, 0.12)",
                COLORS["hover_bg"]
            ),
            ".conv-delete-btn": {"opacity": "1"},
        },
    )


# ============================================================================
# SIDEBAR ACTION BUTTON COMPONENT
# ============================================================================

def sidebar_action_button(
    icon: str,
    label: str,
    on_click=None,
    icon_color: str = COLORS["text_secondary"],
    hover_bg: str = COLORS["light_gray"],
) -> rx.Component:
    """Sidebar action button with icon and label."""
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=16, color=icon_color),
            rx.text(label, font_size="0.8125rem", color=COLORS["text_secondary"]),
            spacing="2",
            align="center",
        ),
        on_click=on_click,
        cursor="pointer",
        padding="0.625rem 0.75rem",
        border_radius=RADIUS["lg"],
        flex="1",
        min_height="40px",
        transition=TRANSITIONS["fast"],
        _hover={"background": hover_bg},
    )


# ============================================================================
# MAIN SIDEBAR COMPONENT
# ============================================================================

def sidebar(
    conversations: List[Dict] = [],
    current_conversation_id: str = "",
    on_new_conversation=None,
    on_search=None,
    on_conversation_click=None,
    user_name: str = "John Doe",
    user_email: str = "johndoe@email.com",
    is_open: bool = False,
    is_collapsed: bool = False,
    on_toggle_collapse=None,
) -> rx.Component:
    """Professional sidebar with conversation list and user profile.
    
    Features:
    - Collapsible design for desktop (72px collapsed, 280px expanded)
    - Slide-in animation for mobile
    - New conversation button
    - Conversation list with active state
    - User profile section with actions
    - Settings, reminders, events, dark mode toggles
    
    Args:
        conversations: List of conversation dicts with 'id' and 'title'
        current_conversation_id: ID of active conversation
        on_new_conversation: Handler for new conversation button
        on_search: Handler for search input
        on_conversation_click: Handler for conversation click
        user_name: User's display name
        user_email: User's email
        is_open: Whether sidebar is open (mobile)
        is_collapsed: Whether sidebar is collapsed (desktop)
        on_toggle_collapse: Handler for collapse toggle
    """
    return rx.box(
        rx.vstack(
            # ============================================================
            # HEADER
            # ============================================================
            rx.box(
                rx.cond(
                    is_collapsed,
                    # Collapsed: Centered logo and toggle
                    rx.vstack(
                        # Logo icon
                        rx.box(
                            rx.icon("graduation-cap", size=28, color=COLORS["primary_green"]),
                            width="52px",
                            height="52px",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            background=COLORS["primary_light"],
                            border_radius="14px",
                            margin_bottom="0.75rem",
                        ),
                        # Expand button
                        rx.tooltip(
                            rx.box(
                                rx.icon("panel-left-open", size=18, color=COLORS["primary_green"]),
                                on_click=on_toggle_collapse,
                                cursor="pointer",
                                width="44px",
                                height="44px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                border_radius="12px",
                                border=f"1.5px solid {COLORS['primary_green']}",
                                transition=TRANSITIONS["fast"],
                                _hover={
                                    "background": COLORS["primary_green"],
                                    "transform": "scale(1.05)",
                                },
                                _hover_child={
                                    "color": "white",
                                },
                            ),
                            content="Uitklappen",
                        ),
                        spacing="0",
                        align="center",
                        width="100%",
                    ),
                    # Expanded: Logo and buttons
                    rx.hstack(
                        logo(size="md"),
                        rx.spacer(),
                        rx.hstack(
                            # Mobile close
                            rx.box(
                                rx.icon("x", size=20, color=COLORS["text_secondary"]),
                                on_click=AppState.close_sidebar,
                                cursor="pointer",
                                padding="0.5rem",
                                border_radius=RADIUS["lg"],
                                display=["flex", "flex", "none"],
                                transition=TRANSITIONS["fast"],
                                _hover={"background": COLORS["light_gray"]},
                            ),
                            # Desktop collapse toggle
                            rx.box(
                                rx.icon("panel-left-close", size=18, color=COLORS["text_secondary"]),
                                on_click=on_toggle_collapse,
                                cursor="pointer",
                                padding="0.5rem",
                                border_radius=RADIUS["lg"],
                                display=["none", "none", "flex"],
                                transition=TRANSITIONS["fast"],
                                _hover={
                                    "background": COLORS["light_green"],
                                    "color": COLORS["primary_green"],
                                },
                            ),
                        ),
                        align="center",
                        width="100%",
                    ),
                ),
                padding="1rem 0.75rem",
                border_bottom=f"1px solid {COLORS['border_light']}",
                width="100%",
            ),
            
            # ============================================================
            # NEW CONVERSATION BUTTON
            # ============================================================
            rx.box(
                rx.cond(
                    is_collapsed,
                    # Collapsed: modern icon button
                    rx.center(
                        rx.tooltip(
                            rx.box(
                                rx.icon("plus", size=20, color="white"),
                                on_click=on_new_conversation,
                                cursor="pointer",
                                width="48px",
                                height="48px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                border_radius="12px",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['primary_hover']} 100%)",
                                box_shadow="0 2px 8px rgba(16, 163, 127, 0.2)",
                                transition=TRANSITIONS["fast"],
                                _hover={
                                    "transform": "translateY(-2px)",
                                    "box_shadow": "0 4px 12px rgba(16, 163, 127, 0.3)",
                                },
                            ),
                            content="Nieuw gesprek",
                        ),
                        width="100%",
                    ),
                    # Expanded: full button
                    rx.box(
                        rx.hstack(
                            rx.icon("plus", size=16, color=COLORS["primary_green"]),
                            rx.text(
                                "Nieuw gesprek",
                                font_size="0.875rem",
                                font_weight="500",
                                color=COLORS["primary_green"],
                            ),
                            spacing="2",
                            align="center",
                            justify="center",
                        ),
                        on_click=on_new_conversation,
                        cursor="pointer",
                        padding="0.625rem 1rem",
                        border_radius=RADIUS["lg"],
                        border=f"1.5px dashed {COLORS['primary_green']}",
                        width="100%",
                        transition=TRANSITIONS["fast"],
                        _hover={
                            "background": COLORS["light_green"],
                            "border_style": "solid",
                        },
                    ),
                ),
                padding="0.75rem",
                width="100%",
            ),
            
            # ============================================================
            # CONVERSATIONS SECTION
            # ============================================================
            rx.cond(
                is_collapsed,
                rx.fragment(),
                rx.box(
                    rx.hstack(
                        rx.text(
                            "Gesprekken",
                            font_size="0.6875rem",
                            color=COLORS["text_tertiary"],
                            text_transform="uppercase",
                            font_weight="600",
                            letter_spacing="0.5px",
                        ),
                        rx.box(
                            rx.text(
                                conversations.length(),
                                font_size="0.625rem",
                                color="white",
                                font_weight="600",
                            ),
                            background=COLORS["primary_green"],
                            padding="0.125rem 0.5rem",
                            border_radius=RADIUS["full"],
                            min_width="1.25rem",
                            text_align="center",
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                    ),
                    padding="0.5rem 0.75rem",
                    width="100%",
                ),
            ),
            
            # ============================================================
            # CONVERSATION LIST
            # ============================================================
            rx.box(
                rx.cond(
                    is_collapsed,
                    # Collapsed: Minimal dot indicators
                    rx.vstack(
                        rx.foreach(
                            conversations,
                            lambda conv: rx.tooltip(
                                rx.box(
                                    rx.box(
                                        width=rx.cond(
                                            conv["id"] == current_conversation_id,
                                            "32px",
                                            "8px"
                                        ),
                                        height="8px",
                                        background=rx.cond(
                                            conv["id"] == current_conversation_id,
                                            COLORS["primary_green"],
                                            COLORS["gray_300"]
                                        ),
                                        border_radius="4px",
                                        transition="all 0.3s ease",
                                    ),
                                    on_click=AppState.load_conversation(conv["id"]),
                                    cursor="pointer",
                                    width="100%",
                                    display="flex",
                                    justify_content="center",
                                    padding="0.5rem 0",
                                    transition=TRANSITIONS["fast"],
                                    _hover_child={
                                        "transform": "scale(1.2)",
                                        "background": COLORS["primary_green"],
                                    },
                                ),
                                content=conv["title"],
                            ),
                        ),
                        spacing="1",
                        padding="1rem 0.5rem",
                        width="100%",
                    ),
                    # Expanded: full conversation list
                    rx.cond(
                        conversations.length() > 0,
                        rx.box(
                            rx.foreach(
                                conversations,
                                lambda conv: render_conversation_item(conv, current_conversation_id),
                            ),
                            padding="0 0.5rem",
                            width="100%",
                        ),
                        # Empty state
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.icon("message-square-plus", size=28, color=COLORS["text_tertiary"]),
                                    padding="1rem",
                                    background=COLORS["light_gray"],
                                    border_radius=RADIUS["full"],
                                ),
                                rx.text(
                                    "Nog geen gesprekken",
                                    font_size="0.875rem",
                                    color=COLORS["text_secondary"],
                                    font_weight="500",
                                ),
                                rx.text(
                                    "Start je eerste gesprek hierboven",
                                    font_size="0.75rem",
                                    color=COLORS["text_tertiary"],
                                    text_align="center",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            padding="2.5rem 1rem",
                            text_align="center",
                            width="100%",
                        ),
                    ),
                ),
                flex="1",
                overflow_y="auto",
                overflow_x="hidden",
                width="100%",
                class_name="custom-scrollbar",
            ),
            
            # ============================================================
            # ONBOARDING LINK (expanded only)
            # ============================================================
            rx.cond(
                is_collapsed,
                # Collapsed: Show modern icon button
                rx.center(
                    rx.tooltip(
                        rx.link(
                            rx.box(
                                rx.icon("user-cog", size=22, color="white"),
                                width="48px",
                                height="48px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['primary_hover']} 100%)",
                                border_radius="14px",
                                transition=TRANSITIONS["fast"],
                                box_shadow="0 2px 8px rgba(16, 163, 127, 0.2)",
                                _hover={
                                    "transform": "translateY(-2px)",
                                    "box_shadow": "0 4px 12px rgba(16, 163, 127, 0.3)",
                                },
                            ),
                            href="/onboarding",
                        ),
                        content="Voorkeuren",
                    ),
                    padding="0.75rem 0.5rem",
                    border_top=f"1px solid {COLORS['border_light']}",
                    border_bottom=f"1px solid {COLORS['border_light']}",
                    width="100%",
                ),
                rx.box(
                    rx.link(
                        rx.box(
                            rx.hstack(
                                rx.icon("graduation-cap", size=18, color="white"),
                                rx.text(
                                    "Start Onboarding",
                                    font_size="0.875rem",
                                    font_weight="600",
                                    color="white",
                                ),
                                spacing="2",
                                align="center",
                                justify="center",
                            ),
                            width="100%",
                            padding="0.75rem 1rem",
                            border_radius=RADIUS["lg"],
                            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                            box_shadow=SHADOWS["primary_sm"],
                            transition=TRANSITIONS["fast"],
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": SHADOWS["primary_md"],
                            },
                        ),
                        href="/onboarding",
                        text_decoration="none",
                        width="100%",
                    ),
                    padding="0.875rem",
                    border_top=f"1px solid {COLORS['border_light']}",
                    border_bottom=f"1px solid {COLORS['border_light']}",
                    width="100%",
                ),
            ),
            
            # ============================================================
            # FOOTER / USER SECTION
            # ============================================================
            rx.box(
                rx.cond(
                    is_collapsed,
                    # Collapsed: modern icon stack
                    rx.vstack(
                        # Avatar with better styling
                        rx.box(
                            avatar(name=user_name, size="md"),
                            margin_bottom="0.5rem",
                        ),
                        # Logout button - modern
                        rx.tooltip(
                            rx.box(
                                rx.icon("log-out", size=18, color=COLORS["text_secondary"]),
                                on_click=AppState.logout,
                                cursor="pointer",
                                width="44px",
                                height="44px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                border_radius="12px",
                                border=f"1.5px solid {COLORS['border']}",
                                background="white",
                                transition=TRANSITIONS["fast"],
                                _hover={
                                    "background": "rgba(239, 68, 68, 0.08)",
                                    "border_color": "rgba(239, 68, 68, 0.3)",
                                    "color": "#DC2626",
                                },
                            ),
                            content="Uitloggen",
                        ),
                        spacing="3",
                        align="center",
                        width="100%",
                    ),
                    # Expanded: full user section
                    rx.vstack(
                        # User info row
                        rx.hstack(
                            avatar(name=user_name, size="md"),
                            rx.vstack(
                                rx.text(
                                    user_name,
                                    font_size="0.875rem",
                                    font_weight="600",
                                    color=COLORS["text_primary"],
                                    overflow="hidden",
                                    text_overflow="ellipsis",
                                    white_space="nowrap",
                                    line_height="1.3",
                                ),
                                rx.cond(
                                    user_email != "",
                                    rx.text(
                                        user_email,
                                        font_size="0.75rem",
                                        color=COLORS["text_tertiary"],
                                        overflow="hidden",
                                        text_overflow="ellipsis",
                                        white_space="nowrap",
                                        line_height="1.3",
                                    ),
                                    rx.box(
                                        rx.text(
                                            "GAST",
                                            font_size="0.625rem",
                                            color=COLORS["primary_green"],
                                            font_weight="700",
                                            letter_spacing="0.5px",
                                        ),
                                        padding="3px 8px",
                                        background=COLORS["light_green"],
                                        border_radius=RADIUS["sm"],
                                    ),
                                ),
                                spacing="0",
                                align_items="start",
                                flex="1",
                                min_width="0",
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                        ),
                        # Action buttons row 1
                        rx.hstack(
                            sidebar_action_button(
                                icon="settings",
                                label="Instellingen",
                                on_click=AuthState.toggle_settings_modal,
                            ),
                            sidebar_action_button(
                                icon="bell",
                                label="Reminders",
                                on_click=AuthState.toggle_reminder_modal,
                                icon_color=COLORS["primary_green"],
                                hover_bg=COLORS["light_green"],
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        # Action buttons row 2
                        rx.hstack(
                            sidebar_action_button(
                                icon="calendar",
                                label="Events",
                                on_click=AuthState.toggle_events_panel,
                                icon_color="#3B82F6",
                                hover_bg="rgba(59, 130, 246, 0.1)",
                            ),
                            rx.box(
                                rx.hstack(
                                    rx.cond(
                                        AuthState.dark_mode,
                                        rx.icon("sun", size=16, color="#F59E0B"),
                                        rx.icon("moon", size=16, color="#6B7280"),
                                    ),
                                    rx.text(
                                        rx.cond(AuthState.dark_mode, "Light", "Dark"),
                                        font_size="0.8125rem",
                                        color=COLORS["text_secondary"],
                                    ),
                                    spacing="2",
                                    align="center",
                                ),
                                on_click=AuthState.toggle_dark_mode,
                                cursor="pointer",
                                padding="0.625rem 0.75rem",
                                border_radius=RADIUS["lg"],
                                flex="1",
                                min_height="40px",
                                transition=TRANSITIONS["fast"],
                                _hover={"background": COLORS["light_gray"]},
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        # Logout button
                        rx.box(
                            rx.hstack(
                                rx.icon("log-out", size=16, color=COLORS["error"]),
                                rx.text(
                                    "Uitloggen",
                                    font_size="0.8125rem",
                                    color=COLORS["error"],
                                    font_weight="500",
                                ),
                                spacing="2",
                                align="center",
                                justify="center",
                            ),
                            on_click=AppState.logout,
                            cursor="pointer",
                            padding="0.625rem 0.875rem",
                            border_radius=RADIUS["lg"],
                            width="100%",
                            min_height="40px",
                            border=f"1px solid rgba(239, 68, 68, 0.2)",
                            transition=TRANSITIONS["fast"],
                            _hover={
                                "background": f"rgba(239, 68, 68, 0.08)",
                                "border_color": COLORS["error"],
                            },
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),
                padding="1rem",
                border_top=f"1px solid {COLORS['border_light']}",
                width="100%",
                background=COLORS["white"],
            ),
            
            spacing="0",
            height="100%",
            width="100%",
        ),
        # ============================================================
        # SIDEBAR CONTAINER STYLES
        # ============================================================
        width=rx.cond(
            is_collapsed,
            ["300px", "300px", SIDEBAR_CONFIG["width_collapsed"]],
            ["300px", "300px", SIDEBAR_CONFIG["width_expanded"]]
        ),
        min_width=rx.cond(
            is_collapsed,
            ["300px", "300px", SIDEBAR_CONFIG["width_collapsed"]],
            ["300px", "300px", SIDEBAR_CONFIG["width_expanded"]]
        ),
        background=COLORS["white"],
        border_right=f"1px solid {COLORS['border_light']}",
        height="100vh",
        position="fixed",
        top="0",
        flex_shrink="0",
        # Mobile: slide in/out
        left=rx.cond(is_open, "0", "-100%"),
        z_index=[SIDEBAR_CONFIG["z_index_mobile"], SIDEBAR_CONFIG["z_index_mobile"], "auto"],
        transition=f"all {TRANSITIONS['normal']}",
        box_shadow=rx.cond(
            is_open,
            SHADOWS["lg"],
            "none"
        ),
        overflow="hidden",
        # Desktop: always visible
        **{
            "@media (min-width: 1024px)": {
                "left": "0 !important",
                "position": "relative",
                "box_shadow": "none",
            }
        }
    )

