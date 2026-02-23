"""Landing page with authentication - Dutch Surinamese Education Focus."""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.state.app_state import AppState
from educhat.components.auth import auth_modal
from educhat.components.shared.institution_logos import compact_logos_row
from educhat.styles.theme import COLORS, T
from educhat.utils.translations import t


# Static color values for SVG elements (which can't use CSS variables)
PRIMARY_HEX = "#10A37F"
PRIMARY_HOVER_HEX = "#0D8F6F"


def tx(key: str) -> rx.Var:
    """Reactive translation helper for landing page.
    
    Returns a reactive var that updates when language changes.
    """
    return rx.cond(
        AuthState.is_dutch,
        t(key, "nl"),
        t(key, "en"),
    )


def svg_icon(path: str, size: int = 24, color: str = None) -> rx.Component:
    """Create an inline SVG icon."""
    if color is None:
        color = COLORS["primary_green"]
    
    return rx.html(
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="{path}" fill="{color}"/></svg>'
    )


def check_circle_svg(size: int = 20, color: str = None) -> rx.Component:
    """Check circle SVG icon."""
    if color is None:
        color = COLORS["primary_green"]
    # Use currentColor inside the SVG and set the wrapper's color style.
    # This allows passing either a hex value (e.g. '#10A37F') or a CSS variable (e.g. 'var(--color-primary)').
    svg = f'''<span style="display:inline-block; color:{color}; line-height:0;">
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.12"/>
            <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
        </svg>
    </span>'''
    return rx.html(svg)


def landing() -> rx.Component:
    """Landing page voor Surinaams onderwijs."""
    
    return rx.box(
        # Auth modal
        auth_modal(),
        
        # Navigation bar - Enhanced
        rx.box(
            rx.box(
                # Logo section with animation
                rx.box(
                    rx.box(
                        rx.icon("graduation-cap", size=32, color=T.primary),
                        width="48px",
                        height="48px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(13, 138, 107, 0.15) 100%)",
                        border_radius="12px",
                        transition="all 0.3s ease",
                        _hover={
                            "transform": "rotate(-5deg) scale(1.05)",
                            "box_shadow": f"0 4px 16px rgba(16, 163, 127, 0.2)",
                        },
                    ),
                    rx.box(
                        rx.heading(
                            "EduChat",
                            size="6",
                            color=T.primary,
                            font_weight="800",
                            margin_bottom="2px",
                        ),
                        rx.text(
                            tx("landing_subtitle"),
                            font_size="11px",
                            color=T.text_secondary,
                            font_weight="600",
                            letter_spacing="0.5px",
                        ),
                    ),
                    display="flex",
                    align_items="center",
                    gap="12px",
                    cursor="pointer",
                    transition="all 0.3s ease",
                    _hover={"opacity": "0.8"},
                ),
                
                # Navigation buttons
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("log-in", size=18),
                            rx.text(tx("login"), display=["none", "block", "block"]),
                            spacing="2",
                            align="center",
                        ),
                        background="transparent",
                        color=T.text_primary,
                        border="none",
                        cursor="pointer",
                        font_weight="600",
                        font_size="15px",
                        padding="10px 20px",
                        border_radius="10px",
                        transition="all 0.3s ease",
                        _hover={
                            "color": COLORS["primary_green"],
                            "background": f"rgba(16, 163, 127, 0.08)",
                            "transform": "translateY(-2px)",
                        },
                        on_click=AuthState.toggle_auth_modal,
                    ),
                    # Language toggle
                    rx.button(
                        rx.cond(
                            AuthState.is_dutch,
                            rx.text("EN", font_weight="600"),
                            rx.text("NL", font_weight="600"),
                        ),
                        background="transparent",
                        color=T.text_primary,
                        border="none",
                        cursor="pointer",
                        padding="10px 16px",
                        border_radius="10px",
                        transition="all 0.3s ease",
                        title="Switch language / Taal wisselen",
                        _hover={
                            "background": f"rgba(16, 163, 127, 0.08)",
                            "transform": "translateY(-2px)",
                        },
                        on_click=AuthState.toggle_language,
                    ),
                    # Dark mode toggle
                    rx.button(
                        rx.icon("moon", size=18),
                        background="transparent",
                        color=T.text_primary,
                        border="none",
                        cursor="pointer",
                        padding="10px 16px",
                        border_radius="10px",
                        transition="all 0.3s ease",
                        title="Toggle dark mode",
                        _hover={
                            "background": f"rgba(16, 163, 127, 0.08)",
                            "transform": "translateY(-2px)",
                        },
                        on_click=rx.toggle_color_mode,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("sparkles", size=18),
                            rx.text(tx("start_now")),
                            spacing="2",
                            align="center",
                        ),
                        background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                        color="white",
                        border="none",
                        border_radius="12px",
                        cursor="pointer",
                        font_weight="700",
                        font_size="15px",
                        padding="12px 28px",
                        transition="all 0.3s ease",
                        box_shadow=f"0 4px 16px rgba(16, 163, 127, 0.3)",
                        _hover={
                            "transform": "translateY(-3px)",
                            "box_shadow": f"0 8px 24px rgba(16, 163, 127, 0.4)",
                        },
                        on_click=AuthState.toggle_auth_modal,
                    ),
                    spacing="3",
                ),
                
                display="flex",
                justify_content="space-between",
                align_items="center",
                width="100%",
                max_width="1400px",
                margin="0 auto",
            ),
            background="var(--navbar-bg)",
            backdrop_filter="blur(12px)",
            padding="20px 32px",
            border_bottom="1px solid var(--navbar-border)",
            position="sticky",
            top="0",
            z_index="100",
            box_shadow="var(--shadow-sm)",
            animation="slideDown 0.5s ease-out",
        ),
        
        # Hero section - Enhanced
        rx.box(
            # Animated background patterns
            rx.html(
                f'''<svg width="100%" height="100%" viewBox="0 0 1200 800" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.04; pointer-events: none;">
                    <circle cx="200" cy="150" r="150" fill="{COLORS['primary_green']}">
                        <animate attributeName="r" values="150;180;150" dur="6s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="1000" cy="600" r="200" fill="{COLORS['primary_green']}">
                        <animate attributeName="r" values="200;230;200" dur="7s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="800" cy="100" r="100" fill="{COLORS['primary_green']}">
                        <animate attributeName="r" values="100;130;100" dur="5s" repeatCount="indefinite"/>
                    </circle>
                    <path d="M0,400 Q300,300 600,400 T1200,400" stroke="{COLORS['primary_green']}" stroke-width="3" fill="none" opacity="0.3">
                        <animate attributeName="d" 
                            values="M0,400 Q300,300 600,400 T1200,400;
                                    M0,400 Q300,350 600,400 T1200,400;
                                    M0,400 Q300,300 600,400 T1200,400" 
                            dur="8s" repeatCount="indefinite"/>
                    </path>
                </svg>''',
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                pointer_events="none",
            ),
            
            rx.box(
                # Left content
                rx.box(
                    # Premium badge
                    rx.box(
                        rx.icon("zap", size=16, color=T.primary),
                        rx.text(tx("ai_powered_badge"), font_size="13px", font_weight="700", color=T.primary),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="8px 20px",
                        background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(13, 138, 107, 0.15) 100%)",
                        border_radius="50px",
                        border=f"2px solid {COLORS['primary_green']}",
                        margin_bottom="24px",
                        width="fit-content",
                        animation="scaleIn 0.6s ease-out",
                        box_shadow=f"0 4px 16px rgba(16, 163, 127, 0.15)",
                    ),
                    
                    rx.heading(
                        tx("welcome_to"),
                        rx.text(
                            " EduChat",
                            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                            background_clip="text",
                            color="transparent",
                            as_="span",
                        ),
                        size="9",
                        color=T.text_primary,
                        margin_bottom="20px",
                        animation="fadeInLeft 0.8s ease-out",
                        font_weight="800",
                        line_height="1.15",
                        letter_spacing="-0.02em",
                    ),
                    rx.text(
                        tx("hero_description_1"),
                        font_size="17px",
                        color=T.text_secondary,
                        line_height="1.7",
                        margin_bottom="24px",
                        animation="fadeIn 0.8s ease-out 0.2s backwards",
                        max_width="580px",
                        font_weight="450",
                    ),
                    rx.text(
                        tx("hero_description_2"),
                        font_size="17px",
                        color=T.text_secondary,
                        line_height="1.7",
                        margin_bottom="36px",
                        animation="fadeIn 0.8s ease-out 0.3s backwards",
                        max_width="580px",
                        font_weight="450",
                    ),
                    
                    # CTA buttons
                    rx.box(
                        rx.button(
                            rx.hstack(
                                rx.icon("sparkles", size=22),
                                rx.text(tx("start_chat"), font_size="17px", font_weight="700"),
                                rx.icon("arrow-right", size=20),
                                spacing="2",
                                align="center",
                            ),
                            padding="18px 40px",
                            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                            color="white",
                            border="none",
                            border_radius="14px",
                            cursor="pointer",
                            font_weight="700",
                            font_size="17px",
                            transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                            box_shadow=f"0 8px 28px rgba(16, 163, 127, 0.35)",
                            _hover={
                                "transform": "translateY(-4px) scale(1.02)",
                                "box_shadow": f"0 12px 40px rgba(16, 163, 127, 0.45)",
                            },
                            on_click=AuthState.toggle_auth_modal,
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("circle-play", size=20),
                                rx.text(tx("try_as_guest"), font_size="16px"),
                                spacing="2",
                            ),
                            padding="18px 36px",
                            background=T.bg_card,
                            color=T.primary,
                            border=f"2px solid {T.primary}",
                            border_radius="14px",
                            cursor="pointer",
                            font_weight="600",
                            font_size="16px",
                            transition="all 0.3s ease",
                            box_shadow="0 4px 16px rgba(0, 0, 0, 0.08)",
                            _hover={
                                "background": f"rgba(16, 163, 127, 0.08)",
                                "transform": "translateY(-4px)",
                                "box_shadow": "0 8px 24px rgba(16, 163, 127, 0.15)",
                            },
                            on_click=AuthState.continue_as_guest,
                        ),
                        display="flex",
                        gap="16px",
                        flex_wrap="wrap",
                        animation="fadeInUp 0.8s ease-out 0.3s backwards",
                    ),
                    
                    # Trust badges
                    rx.box(
                        rx.box(
                            rx.box(
                                check_circle_svg(18, T.primary),
                                rx.text(
                                    tx("free_to_use"),
                                    font_size="15px",
                                    color=T.text_secondary,
                                    font_weight="600",
                                ),
                                display="flex",
                                align_items="center",
                                gap="10px",
                            ),
                            rx.box(
                                check_circle_svg(18, T.primary),
                                rx.text(
                                    tx("available_24_7"),
                                    font_size="15px",
                                    color=T.text_secondary,
                                    font_weight="600",
                                ),
                                display="flex",
                                align_items="center",
                                gap="10px",
                            ),
                            rx.box(
                                check_circle_svg(18, T.primary),
                                rx.text(
                                    tx("focus_suriname"),
                                    font_size="15px",
                                    color=T.text_secondary,
                                    font_weight="600",
                                ),
                                display="flex",
                                align_items="center",
                                gap="10px",
                            ),
                            display="flex",
                            flex_wrap="wrap",
                            gap="28px",
                        ),
                        padding="24px 32px",
                        background=T.bg_card,
                        border_radius="16px",
                        box_shadow=T.shadow_md,
                        border=f"1px solid {T.border_light}",
                        margin_top="48px",
                        animation="fadeIn 0.8s ease-out 0.4s backwards",
                        width="fit-content",
                    ),
                    
                    flex="1",
                    display="flex",
                    flex_direction="column",
                    justify_content="center",
                ),
                
                # Right side - Interactive demo with enhanced design
                rx.box(
                    rx.box(
                        # Decorative background
                        rx.html(
                            f'''<svg width="100%" height="100%" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.06;">
                                <circle cx="350" cy="50" r="80" fill="{COLORS['primary_green']}">
                                    <animate attributeName="r" values="80;100;80" dur="4s" repeatCount="indefinite"/>
                                </circle>
                                <circle cx="50" cy="350" r="100" fill="{COLORS['primary_green']}">
                                    <animate attributeName="r" values="100;120;100" dur="5s" repeatCount="indefinite"/>
                                </circle>
                            </svg>''',
                            position="absolute",
                            top="0",
                            left="0",
                            width="100%",
                            height="100%",
                            pointer_events="none",
                        ),
                        
                        # SVG illustratie
                        rx.box(
                            education_illustration_svg(),
                            width="100%",
                            max_width="450px",
                            height="400px",
                            margin_x="auto",
                            animation="fadeIn 1s ease-out 0.5s backwards",
                        ),
                        
                        # Chat bubble preview with enhanced styling
                        rx.box(
                            rx.box(
                                rx.box(
                                    rx.text(
                                        tx("chat_preview_question"),
                                        font_size="14px",
                                        color=T.text_primary,
                                        font_weight="600",
                                    ),
                                    padding="14px 20px",
                                    background=f"linear-gradient(135deg, {COLORS['light_green']} 0%, rgba(16, 163, 127, 0.15) 100%)",
                                    border_radius="16px 16px 4px 16px",
                                    box_shadow=f"0 4px 16px rgba(16, 163, 127, 0.15)",
                                    margin_bottom="12px",
                                    max_width="85%",
                                    margin_left="auto",
                                    animation="slideInRight 0.6s ease-out 0.7s backwards",
                                    border=f"1px solid rgba(16, 163, 127, 0.2)",
                                ),
                            ),
                            rx.box(
                                rx.box(
                                    rx.hstack(
                                        rx.icon("sparkles", size=16, color=T.primary),
                                        rx.text(
                                            tx("chat_preview_answer"),
                                            font_size="14px",
                                            color=T.text_secondary,
                                            font_weight="500",
                                        ),
                                        spacing="2",
                                        align="start",
                                    ),
                                    padding="14px 20px",
                                    background=T.bg_card,
                                    border_radius="16px 16px 16px 4px",
                                    border=f"2px solid {T.border}",
                                    box_shadow="0 4px 16px rgba(0, 0, 0, 0.08)",
                                    max_width="90%",
                                    animation="slideInLeft 0.6s ease-out 0.9s backwards",
                                ),
                            ),
                            display="flex",
                            flex_direction="column",
                            gap="12px",
                            margin_top="32px",
                        ),
                        
                        # Typing indicator
                        rx.box(
                            rx.box(
                                rx.box(width="8px", height="8px", background=T.primary, border_radius="50%", animation="pulse 1.4s ease-in-out infinite"),
                                rx.box(width="8px", height="8px", background=T.primary, border_radius="50%", animation="pulse 1.4s ease-in-out 0.2s infinite"),
                                rx.box(width="8px", height="8px", background=T.primary, border_radius="50%", animation="pulse 1.4s ease-in-out 0.4s infinite"),
                                display="flex",
                                gap="6px",
                            ),
                            padding="12px 20px",
                            background=T.bg_card,
                            border_radius="16px",
                            border=f"1px solid {T.border}",
                            box_shadow="0 2px 12px rgba(0, 0, 0, 0.06)",
                            width="fit-content",
                            margin_top="12px",
                            animation="fadeIn 0.6s ease-out 1.1s backwards",
                        ),
                        
                        background=T.bg_card,
                        padding="40px",
                        border_radius="24px",
                        box_shadow=T.shadow_xl,
                        border=f"2px solid {T.border_light}",
                        overflow="hidden",
                        position="relative",
                    ),
                    flex="1",
                    display=["none", "none", "flex"],
                    align_items="center",
                    justify_content="center",
                ),
                
                display="flex",
                gap="80px",
                align_items="center",
                flex_wrap="wrap",
                max_width="1400px",
                margin="0 auto",
                position="relative",
                z_index="1",
            ),
            
            padding="100px 32px 140px 32px",
            background=T.bg_primary,
            min_height="calc(100vh - 88px)",
            display="flex",
            align_items="center",
            position="relative",
            overflow="hidden",
        ),
        
        # Features section
        rx.box(
            rx.box(
                rx.heading(
                    tx("features_title"),
                    size="8",
                    color=T.text_primary,
                    text_align="center",
                    margin_bottom="16px",
                    font_weight="700",
                ),
                rx.text(
                    tx("features_subtitle"),
                    font_size="18px",
                    color=T.text_secondary,
                    text_align="center",
                    margin_bottom="64px",
                    max_width="600px",
                    margin_x="auto",
                ),
                
                # Features grid
                rx.box(
                    feature_card(
                        icon="school",
                        title=tx("feature_find_programs"),
                        description=tx("feature_find_programs_desc"),
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="clipboard-list",
                        title=tx("feature_requirements"),
                        description=tx("feature_requirements_desc"),
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="calendar",
                        title=tx("feature_deadlines"),
                        description=tx("feature_deadlines_desc"),
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="message-circle",
                        title=tx("feature_direct_answers"),
                        description=tx("feature_direct_answers_desc"),
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="compass",
                        title=tx("feature_guidance"),
                        description=tx("feature_guidance_desc"),
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="shield",
                        title=tx("feature_privacy"),
                        description=tx("feature_privacy_desc"),
                        accent_color=COLORS["primary_green"],
                    ),
                    
                    display="grid",
                    grid_template_columns=["1fr", "repeat(2, 1fr)", "repeat(3, 1fr)"],
                    gap="28px",
                    max_width="1400px",
                    margin="0 auto",
                ),
                
                max_width="1400px",
                margin="0 auto",
            ),
            
            padding="120px 32px",
            background=T.bg_secondary,
        ),
        
        # How it works section - Enhanced
        rx.box(
            # Decorative background patterns
            rx.html(
                f'''<svg width="100%" height="100%" viewBox="0 0 1200 600" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.03; pointer-events: none;">
                    <circle cx="100" cy="100" r="80" fill="{COLORS['primary_green']}"/>
                    <circle cx="1100" cy="150" r="100" fill="{COLORS['primary_green']}"/>
                    <circle cx="200" cy="500" r="60" fill="{COLORS['primary_green']}"/>
                    <circle cx="1000" cy="480" r="70" fill="{COLORS['primary_green']}"/>
                    <path d="M0,300 Q300,200 600,300 T1200,300" stroke="{COLORS['primary_green']}" stroke-width="2" opacity="0.3"/>
                </svg>''',
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
            ),
            
            rx.box(
                # Badge label
                rx.box(
                    rx.icon("zap", size=18, color=T.primary, margin_right="8px"),
                    rx.text(
                        tx("superfast_badge"),
                        font_size="14px",
                        font_weight="600",
                        color=T.primary,
                    ),
                    display="flex",
                    align_items="center",
                    background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(16, 163, 127, 0.05) 100%)",
                    padding="10px 20px",
                    border_radius="50px",
                    border=f"1px solid {COLORS['primary_green']}",
                    margin_bottom="24px",
                    width="fit-content",
                    margin_x="auto",
                ),
                
                rx.heading(
                    tx("how_it_works"),
                    size="8",
                    color=T.text_primary,
                    text_align="center",
                    margin_bottom="16px",
                    font_weight="700",
                ),
                rx.text(
                    tx("how_it_works_subtitle"),
                    font_size="18px",
                    color=T.text_secondary,
                    text_align="center",
                    margin_bottom="80px",
                    max_width="600px",
                    margin_x="auto",
                    line_height="1.7",
                ),
                
                # Steps with enhanced design
                rx.box(
                    # Step 1
                    rx.box(
                        enhanced_step_card(
                            number="1",
                            title=tx("step1_title"),
                            description=tx("step1_desc"),
                            icon="message-square-plus",
                            color="#10a37f",
                        ),
                        position="relative",
                    ),
                    
                    # Animated connector line
                    rx.box(
                        rx.html(
                            f'''<svg width="100%" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <defs>
                                    <linearGradient id="lineGradient1" x1="0%" y1="0%" x2="100%" y2="0%">
                                        <stop offset="0%" style="stop-color:{COLORS['primary_green']};stop-opacity:0.3" />
                                        <stop offset="100%" style="stop-color:{COLORS['primary_green']};stop-opacity:1" />
                                    </linearGradient>
                                </defs>
                                <path d="M0,50 L100,50" stroke="url(#lineGradient1)" stroke-width="3" stroke-dasharray="5,5">
                                    <animate attributeName="stroke-dashoffset" from="0" to="10" dur="1s" repeatCount="indefinite"/>
                                </path>
                                <circle cx="95" cy="50" r="4" fill="{COLORS['primary_green']}">
                                    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" repeatCount="indefinite"/>
                                </circle>
                            </svg>''',
                        ),
                        display=["none", "none", "block"],
                        width="120px",
                        height="100px",
                    ),
                    
                    # Step 2
                    rx.box(
                        enhanced_step_card(
                            number="2",
                            title=tx("step2_title"),
                            description=tx("step2_desc"),
                            icon="sparkles",
                            color="#0d8a6b",
                        ),
                        position="relative",
                    ),
                    
                    # Animated connector line
                    rx.box(
                        rx.html(
                            f'''<svg width="100%" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <defs>
                                    <linearGradient id="lineGradient2" x1="0%" y1="0%" x2="100%" y2="0%">
                                        <stop offset="0%" style="stop-color:{COLORS['dark_green']};stop-opacity:1" />
                                        <stop offset="100%" style="stop-color:{COLORS['primary_green']};stop-opacity:0.3" />
                                    </linearGradient>
                                </defs>
                                <path d="M0,50 L100,50" stroke="url(#lineGradient2)" stroke-width="3" stroke-dasharray="5,5">
                                    <animate attributeName="stroke-dashoffset" from="0" to="10" dur="1s" repeatCount="indefinite"/>
                                </path>
                                <circle cx="95" cy="50" r="4" fill="{COLORS['primary_green']}">
                                    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
                                </circle>
                            </svg>''',
                        ),
                        display=["none", "none", "block"],
                        width="120px",
                        height="100px",
                    ),
                    
                    # Step 3
                    rx.box(
                        enhanced_step_card(
                            number="3",
                            title=tx("step3_title"),
                            description=tx("step3_desc"),
                            icon="graduation-cap",
                            color="#0a7052",
                        ),
                        position="relative",
                    ),
                    
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    gap="0px",
                    flex_wrap="wrap",
                    max_width="1300px",
                    margin="0 auto",
                ),
                
                # Trust indicators
                rx.box(
                    rx.box(
                        rx.icon("users", size=20, color=T.primary),
                        rx.text("100+ Tevreden Studenten", font_size="14px", font_weight="600", color=T.text_primary),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="12px 20px",
                        background=T.bg_card,
                        border_radius="50px",
                        box_shadow=T.shadow_sm,
                    ),
                    rx.box(
                        rx.icon("clock", size=20, color=T.primary),
                        rx.text("< 5 seconden reactietijd", font_size="14px", font_weight="600", color=T.text_primary),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="12px 20px",
                        background=T.bg_card,
                        border_radius="50px",
                        box_shadow=T.shadow_sm,
                    ),
                    rx.box(
                        rx.icon("shield-check", size=20, color=T.primary),
                        rx.text("100% Betrouwbare Info", font_size="14px", font_weight="600", color=T.text_primary),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="12px 20px",
                        background=T.bg_card,
                        border_radius="50px",
                        box_shadow="0 4px 12px rgba(0, 0, 0, 0.08)",
                    ),
                    display="flex",
                    gap="16px",
                    justify_content="center",
                    flex_wrap="wrap",
                    margin_top="80px",
                ),
                
                max_width="1400px",
                margin="0 auto",
                position="relative",
                z_index="1",
            ),
            
            padding="120px 32px",
            background=T.bg_tertiary,
            position="relative",
            overflow="hidden",
        ),
        
        # Partner Institutions Section - Dedicated
        rx.box(
            # Animated background decoration
            rx.box(
                rx.box(
                    position="absolute",
                    top="-100px",
                    right="-100px",
                    width="400px",
                    height="400px",
                    background=f"radial-gradient(circle, {COLORS['primary_light']} 0%, transparent 70%)",
                    opacity="0.3",
                    pointer_events="none",
                ),
                rx.box(
                    position="absolute",
                    bottom="-100px",
                    left="-100px",
                    width="350px",
                    height="350px",
                    background=f"radial-gradient(circle, {COLORS['primary_light']} 0%, transparent 70%)",
                    opacity="0.25",
                    pointer_events="none",
                ),
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                overflow="hidden",
                pointer_events="none",
            ),
            
            rx.box(
                # Section header
                rx.vstack(
                    rx.box(
                        rx.icon("building-2", size=16, color=T.primary),
                        rx.text("Vertrouwde Partners", font_size="14px", font_weight="600", color=T.primary),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="8px 20px",
                        background=T.bg_card,
                        border_radius="50px",
                        border=f"2px solid {COLORS['primary_green']}",
                        box_shadow=f"0 4px 12px {T.shadow_primary}",
                        margin_bottom="20px",
                        width="fit-content",
                    ),
                    rx.heading(
                        "Onderwijsinstellingen in Suriname",
                        size="9",
                        color=T.text_primary,
                        margin_bottom="16px",
                        font_weight="800",
                        text_align="center",
                        line_height="1.2",
                    ),
                    rx.text(
                        "EduChat heeft toegang tot informatie van alle belangrijke onderwijsinstellingen",
                        font_size="18px",
                        color=T.text_secondary,
                        text_align="center",
                        max_width="600px",
                        margin_bottom="48px",
                        line_height="1.6",
                    ),
                    spacing="0",
                    align="center",
                    width="100%",
                ),
                
                # Logos with infinite scroll
                rx.box(
                    compact_logos_row(),
                    width="100%",
                    padding="50px 40px",
                    background=T.bg_card,
                    border_radius="24px",
                    box_shadow=T.shadow_xl,
                    border=f"1px solid {T.border_light}",
                ),
                
                max_width="1400px",
                margin="0 auto",
                position="relative",
                z_index="1",
            ),
            
            padding="100px 32px",
            background=T.bg_secondary,
            position="relative",
            overflow="hidden",
        ),
        
        # Benefits section - Enhanced
        rx.box(
            # Animated background patterns
            rx.html(
                f'''<svg width="100%" height="100%" viewBox="0 0 1200 800" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.03; pointer-events: none;">
                    <circle cx="100" cy="100" r="120" fill="{COLORS['primary_green']}">
                        <animate attributeName="r" values="120;140;120" dur="4s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="900" cy="150" r="80" fill="{COLORS['primary_green']}">
                        <animate attributeName="r" values="80;100;80" dur="5s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="1100" cy="600" r="150" fill="{COLORS['primary_green']}">
                        <animate attributeName="r" values="150;170;150" dur="6s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="200" cy="700" r="100" fill="{COLORS['primary_green']}">
                        <animate attributeName="r" values="100;120;100" dur="4.5s" repeatCount="indefinite"/>
                    </circle>
                </svg>''',
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                pointer_events="none",
            ),
            
            rx.box(
                # Section header with badge
                rx.box(
                    rx.box(
                        rx.icon("sparkles", size=16, color=T.primary),
                        rx.text("Waarom EduChat?", font_size="14px", font_weight="600", color=T.primary),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="8px 20px",
                        background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(13, 138, 107, 0.15) 100%)",
                        border_radius="50px",
                        border=f"2px solid {COLORS['primary_green']}",
                        margin_bottom="24px",
                        width="fit-content",
                        margin_x="auto",
                    ),
                    rx.heading(
                        "Waarom Studenten voor EduChat Kiezen",
                        size="9",
                        color=T.text_primary,
                        margin_bottom="16px",
                        font_weight="800",
                        text_align="center",
                        line_height="1.2",
                    ),
                    rx.text(
                        "Speciaal ontwikkeld voor Surinaamse studenten met alle informatie die je nodig hebt",
                        font_size="18px",
                        color=T.text_secondary,
                        text_align="center",
                        max_width="700px",
                        margin_x="auto",
                        margin_bottom="64px",
                    ),
                    width="100%",
                    display="flex",
                    flex_direction="column",
                    align_items="center",
                ),
                
                # Benefits grid
                rx.box(
                    # Benefit card 1
                    rx.box(
                        rx.box(
                            rx.box(
                                rx.icon("school", size=32, color="white"),
                                width="70px",
                                height="70px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                border_radius="16px",
                                box_shadow=f"0 8px 24px rgba(16, 163, 127, 0.3)",
                                margin_bottom="24px",
                                transition="all 0.3s ease",
                            ),
                            rx.heading(
                                "Alle Instellingen",
                                size="5",
                                color=T.text_primary,
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Informatie over alle onderwijsinstellingen in Suriname, van universiteiten tot vakscholen",
                                font_size="15px",
                                color=T.text_secondary,
                                line_height="1.7",
                            ),
                        ),
                        background=T.bg_card,
                        padding="40px",
                        border_radius="20px",
                        box_shadow=T.shadow_md,
                        border=f"1px solid {T.border_light}",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-8px)",
                            "box_shadow": "0 12px 40px rgba(16, 163, 127, 0.15)",
                            "border_color": COLORS["primary_green"],
                        },
                    ),
                    
                    # Benefit card 2
                    rx.box(
                        rx.box(
                            rx.box(
                                rx.icon("clipboard-list", size=32, color="white"),
                                width="70px",
                                height="70px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                border_radius="16px",
                                box_shadow=f"0 8px 24px rgba(16, 163, 127, 0.3)",
                                margin_bottom="24px",
                                transition="all 0.3s ease",
                            ),
                            rx.heading(
                                "Duidelijke Uitleg",
                                size="5",
                                color=T.text_primary,
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Begrijpelijke informatie over toelatingseisen, procedures en wat je moet verwachten",
                                font_size="15px",
                                color=T.text_secondary,
                                line_height="1.7",
                            ),
                        ),
                        background=T.bg_card,
                        padding="40px",
                        border_radius="20px",
                        box_shadow=T.shadow_md,
                        border=f"1px solid {T.border_light}",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-8px)",
                            "box_shadow": "0 12px 40px rgba(16, 163, 127, 0.15)",
                            "border_color": COLORS["primary_green"],
                        },
                    ),
                    
                    # Benefit card 3
                    rx.box(
                        rx.box(
                            rx.box(
                                rx.icon("calendar", size=32, color="white"),
                                width="70px",
                                height="70px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                border_radius="16px",
                                box_shadow=f"0 8px 24px rgba(16, 163, 127, 0.3)",
                                margin_bottom="24px",
                                transition="all 0.3s ease",
                            ),
                            rx.heading(
                                "Actuele Deadlines",
                                size="5",
                                color=T.text_primary,
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Mis geen belangrijke data met onze actuele informatie over inschrijvingen en deadlines",
                                font_size="15px",
                                color=T.text_secondary,
                                line_height="1.7",
                            ),
                        ),
                        background=T.bg_card,
                        padding="40px",
                        border_radius="20px",
                        box_shadow=T.shadow_md,
                        border=f"1px solid {T.border_light}",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-8px)",
                            "box_shadow": "0 12px 40px rgba(16, 163, 127, 0.15)",
                            "border_color": COLORS["primary_green"],
                        },
                    ),
                    
                    # Benefit card 4
                    rx.box(
                        rx.box(
                            rx.box(
                                rx.icon("message-circle", size=32, color="white"),
                                width="70px",
                                height="70px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                border_radius="16px",
                                box_shadow=f"0 8px 24px rgba(16, 163, 127, 0.3)",
                                margin_bottom="24px",
                                transition="all 0.3s ease",
                            ),
                            rx.heading(
                                "In Het Nederlands",
                                size="5",
                                color=T.text_primary,
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Antwoorden in helder Nederlands, makkelijk te begrijpen voor iedereen",
                                font_size="15px",
                                color=T.text_secondary,
                                line_height="1.7",
                            ),
                        ),
                        background=T.bg_card,
                        padding="40px",
                        border_radius="20px",
                        box_shadow=T.shadow_md,
                        border=f"1px solid {T.border_light}",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-8px)",
                            "box_shadow": "0 12px 40px rgba(16, 163, 127, 0.15)",
                            "border_color": COLORS["primary_green"],
                        },
                    ),
                    
                    # Benefit card 5
                    rx.box(
                        rx.box(
                            rx.box(
                                rx.icon("target", size=32, color="white"),
                                width="70px",
                                height="70px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                border_radius="16px",
                                box_shadow=f"0 8px 24px rgba(16, 163, 127, 0.3)",
                                margin_bottom="24px",
                                transition="all 0.3s ease",
                            ),
                            rx.heading(
                                "Persoonlijk Advies",
                                size="5",
                                color=T.text_primary,
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Studiekeuzeadvies op maat, afgestemd op jouw interesses en doelen",
                                font_size="15px",
                                color=T.text_secondary,
                                line_height="1.7",
                            ),
                        ),
                        background=T.bg_card,
                        padding="40px",
                        border_radius="20px",
                        box_shadow=T.shadow_md,
                        border=f"1px solid {T.border_light}",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-8px)",
                            "box_shadow": "0 12px 40px rgba(16, 163, 127, 0.15)",
                            "border_color": COLORS["primary_green"],
                        },
                    ),
                    
                    # Benefit card 6
                    rx.box(
                        rx.box(
                            rx.box(
                                rx.icon("sparkles", size=32, color="white"),
                                width="70px",
                                height="70px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                border_radius="16px",
                                box_shadow=f"0 8px 24px rgba(16, 163, 127, 0.3)",
                                margin_bottom="24px",
                                transition="all 0.3s ease",
                            ),
                            rx.heading(
                                "100% Gratis",
                                size="5",
                                color=T.text_primary,
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Volledig gratis te gebruiken, geen verborgen kosten of verrassingen",
                                font_size="15px",
                                color=T.text_secondary,
                                line_height="1.7",
                            ),
                        ),
                        background=T.bg_card,
                        padding="40px",
                        border_radius="20px",
                        box_shadow=T.shadow_md,
                        border=f"1px solid {T.border_light}",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-8px)",
                            "box_shadow": "0 12px 40px rgba(16, 163, 127, 0.15)",
                            "border_color": COLORS["primary_green"],
                        },
                    ),
                    
                    display="grid",
                    grid_template_columns=["1fr", "repeat(2, 1fr)", "repeat(3, 1fr)"],
                    gap="32px",
                    width="100%",
                ),
                
                # Special Suriname badge at bottom
                rx.box(
                    rx.box(
                        rx.html(
                            f'''<svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="50" cy="50" r="45" fill="{COLORS['primary_green']}" opacity="0.2"/>
                                <path d="M50,25 L56,38 L70,38 L59,47 L63,60 L50,50 L37,60 L41,47 L30,38 L44,38 Z" fill="{COLORS['primary_green']}"/>
                                <circle cx="50" cy="50" r="6" fill="{COLORS['dark_green']}"/>
                            </svg>''',
                        ),
                        rx.box(
                            rx.heading(
                                "Speciaal voor Surinaamse Studenten",
                                size="6",
                                color=T.primary,
                                font_weight="700",
                                margin_bottom="8px",
                            ),
                            rx.text(
                                "Jouw persoonlijke gids door het Surinaamse onderwijssysteem",
                                font_size="16px",
                                color=T.text_secondary,
                            ),
                        ),
                        display="flex",
                        align_items="center",
                        gap="24px",
                    ),
                    background=T.bg_card,
                    padding="32px 48px",
                    border_radius="20px",
                    box_shadow=T.shadow_xl,
                    border=f"2px solid {T.primary}",
                    margin_top="64px",
                    width="fit-content",
                    margin_x="auto",
                ),
                
                max_width="1400px",
                margin="0 auto",
                position="relative",
                z_index="1",
            ),
            
            padding="120px 32px",
            background=T.bg_tertiary,
            position="relative",
            overflow="hidden",
        ),
        
        # CTA section - Enhanced
        rx.box(
            # Animated background patterns
            rx.html(
                f'''<svg width="100%" height="100%" viewBox="0 0 1200 600" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.15; pointer-events: none;">
                    <!-- Floating circles -->
                    <circle cx="100" cy="100" r="60" fill="white">
                        <animate attributeName="cy" values="100;80;100" dur="3s" repeatCount="indefinite"/>
                        <animate attributeName="opacity" values="0.3;0.5;0.3" dur="3s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="300" cy="500" r="80" fill="white">
                        <animate attributeName="cy" values="500;480;500" dur="4s" repeatCount="indefinite"/>
                        <animate attributeName="opacity" values="0.2;0.4;0.2" dur="4s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="900" cy="150" r="100" fill="white">
                        <animate attributeName="cy" values="150;130;150" dur="5s" repeatCount="indefinite"/>
                        <animate attributeName="opacity" values="0.25;0.45;0.25" dur="5s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="1100" cy="450" r="70" fill="white">
                        <animate attributeName="cy" values="450;430;450" dur="3.5s" repeatCount="indefinite"/>
                        <animate attributeName="opacity" values="0.3;0.5;0.3" dur="3.5s" repeatCount="indefinite"/>
                    </circle>
                    <!-- Abstract lines -->
                    <path d="M0,300 Q300,200 600,300 T1200,300" stroke="white" stroke-width="2" fill="none" opacity="0.2">
                        <animate attributeName="d" 
                            values="M0,300 Q300,200 600,300 T1200,300;
                                    M0,300 Q300,250 600,300 T1200,300;
                                    M0,300 Q300,200 600,300 T1200,300" 
                            dur="6s" repeatCount="indefinite"/>
                    </path>
                    <path d="M0,400 Q300,300 600,400 T1200,400" stroke="white" stroke-width="2" fill="none" opacity="0.15">
                        <animate attributeName="d" 
                            values="M0,400 Q300,300 600,400 T1200,400;
                                    M0,400 Q300,350 600,400 T1200,400;
                                    M0,400 Q300,300 600,400 T1200,400" 
                            dur="7s" repeatCount="indefinite"/>
                    </path>
                </svg>''',
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                pointer_events="none",
            ),
            
            rx.box(
                # Premium badge
                rx.box(
                    rx.icon("rocket", size=18, color="White"),
                    rx.text("Start Je Studiereis Vandaag", font_size="14px", font_weight="600", color="White"),
                    display="flex",
                    align_items="center",
                    gap="8px",
                    padding="10px 24px",
                    background="rgba(255, 255, 255, 0.2)",
                    backdrop_filter="blur(10px)",
                    border_radius="50px",
                    border="2px solid rgba(255, 255, 255, 0.3)",
                    margin_bottom="32px",
                    width="fit-content",
                    margin_x="auto",
                    box_shadow="0 4px 16px rgba(0, 0, 0, 0.1)",
                ),
                
                rx.heading(
                    tx("cta_title"),
                    size="9",
                    color="white",
                    text_align="center",
                    margin_bottom="20px",
                    font_weight="800",
                    line_height="1.2",
                ),
                rx.text(
                    tx("cta_subtitle"),
                    font_size="20px",
                    color="white",
                    text_align="center",
                    max_width="700px",
                    margin_x="auto",
                    margin_bottom="48px",
                    line_height="1.6",
                ),
                
                # CTA Button with glow effect
                rx.box(
                    rx.button(
                        rx.hstack(
                            rx.icon("sparkles", size=22, color="White"),
                            rx.text(tx("start_free"), font_size="18px", font_weight="700", color="White"),
                            rx.icon("arrow-right", size=20, color="White"),
                            spacing="3",
                            align="center",
                        ),
                        padding="20px 56px",
                        background=T.bg_card,
                        color=T.primary,
                        border="none",
                        border_radius="16px",
                        cursor="pointer",
                        font_weight="700",
                        font_size="18px",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        box_shadow="0 12px 40px rgba(0, 0, 0, 0.25), 0 0 0 0 rgba(255, 255, 255, 0.5)",
                        _hover={
                            "transform": "translateY(-6px) scale(1.02)",
                            "box_shadow": "0 16px 50px rgba(0, 0, 0, 0.35), 0 0 30px rgba(255, 255, 255, 0.4)",
                        },
                        on_click=AuthState.toggle_auth_modal,
                    ),
                    margin_bottom="56px",
                ),
                
                # Stats row
                rx.box(
                    rx.box(
                        rx.heading("100+", size="6", color="White", font_weight="700", margin_bottom="4px"),
                        rx.text(tx("stat_students"), font_size="14px", color="White"),
                        text_align="center",
                    ),
                    rx.box(
                        width="1px",
                        height="40px",
                        background="rgba(255, 255, 255, 0.2)",
                        display=["none", "block", "block"],
                    ),
                    rx.box(
                        rx.heading("<5 sec", size="6", color="White", font_weight="700", margin_bottom="4px"),
                        rx.text(tx("stat_response_time"), font_size="14px", color="White"),
                        text_align="center",
                    ),
                    rx.box(
                        width="1px",
                        height="40px",
                        background="rgba(255, 255, 255, 0.2)",
                        display=["none", "block", "block"],
                    ),
                    rx.box(
                        rx.heading("24/7", size="6", color="White", font_weight="700", margin_bottom="4px"),
                        rx.text(tx("stat_available"), font_size="14px", color="White"),
                        text_align="center",
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    gap="48px",
                    flex_wrap="wrap",
                    padding="32px",
                    background="rgba(255, 255, 255, 0.1)",
                    backdrop_filter="blur(10px)",
                    border_radius="16px",
                    border="1px solid rgba(255, 255, 255, 0.2)",
                ),
                
                # Trust badge at bottom
                rx.box(
                    rx.icon("shield-check", size=18, color="White"),
                    rx.text(
                        tx("trust_badge"),
                        font_size="14px",
                        color="White",
                        font_weight="600",
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    gap="12px",
                    margin_top="40px",
                    flex_wrap="wrap",
                ),
                
                max_width="900px",
                margin="0 auto",
                text_align="center",
                position="relative",
                z_index="1",
            ),
            
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            padding="120px 32px",
            position="relative",
            overflow="hidden",
        ),
        
        width="100vw",
        min_height="100vh",
        overflow_x="hidden",
        # Check for existing session on page load
        on_mount=AppState.check_session_and_redirect,
    )


def feature_card(
    icon: str, 
    title: str, 
    description: str, 
    accent_color: str = None
) -> rx.Component:
    """Modern feature card with icon and hover effects."""
    
    if accent_color is None:
        accent_color = COLORS["primary_green"]
    
    return rx.box(
        rx.box(
            rx.box(
                rx.icon(
                    icon,
                    size=36,
                    color=accent_color,
                ),
                width="64px",
                height="64px",
                display="flex",
                align_items="center",
                justify_content="center",
                background=f"rgba({int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)}, 0.1)",
                border_radius="12px",
                margin_bottom="20px",
                transition="all 0.3s ease",
            ),
            rx.heading(
                title,
                size="5",
                color=T.text_primary,
                margin_bottom="12px",
                font_weight="600",
            ),
            rx.text(
                description,
                color=T.text_secondary,
                font_size="15px",
                line_height="1.7",
            ),
        ),
        background=T.bg_card,
        padding="32px",
        border_radius="14px",
        border=f"1px solid {T.border_light}",
        box_shadow=T.shadow_sm,
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "transform": "translateY(-8px)",
            "box_shadow": "0 12px 32px rgba(0, 0, 0, 0.1)",
            "border_color": accent_color,
        },
    )


def stat_item(value: str, label: str, icon: str) -> rx.Component:
    """Statistics item component."""
    
    return rx.box(
        rx.box(
            rx.icon(icon, size=32, color="white", margin_bottom="16px"),
            rx.heading(
                value,
                size="7",
                color="white",
                font_weight="700",
                margin_bottom="8px",
            ),
            rx.text(
                label,
                font_size="16px",
                color="rgba(255, 255, 255, 0.85)",
                text_align="center",
            ),
            text_align="center",
        ),
    )


def enhanced_step_card(number: str, title: str, description: str, icon: str, color: str) -> rx.Component:
    """Enhanced step card with modern design and animations."""
    
    return rx.box(
        # Background gradient effect
        rx.html(
            f'''<svg width="100%" height="100%" viewBox="0 0 350 400" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.08; pointer-events: none;">
                <circle cx="175" cy="100" r="100" fill="{color}">
                    <animate attributeName="r" values="100;110;100" dur="3s" repeatCount="indefinite"/>
                </circle>
                <circle cx="50" cy="300" r="40" fill="{color}" opacity="0.5">
                    <animate attributeName="cy" values="300;290;300" dur="2s" repeatCount="indefinite"/>
                </circle>
                <circle cx="300" cy="350" r="30" fill="{color}" opacity="0.5">
                    <animate attributeName="cy" values="350;340;350" dur="2.5s" repeatCount="indefinite"/>
                </circle>
            </svg>''',
            position="absolute",
            top="0",
            left="0",
            width="100%",
            height="100%",
        ),
        
        # Content
        rx.box(
            # Number badge with glow
            rx.box(
                rx.text(
                    number,
                    font_size="32px",
                    font_weight="800",
                    color="white",
                    text_align="center",
                    line_height="1",
                ),
                width="80px",
                height="80px",
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="50%",
                background=f"linear-gradient(135deg, {color} 0%, {COLORS['dark_green']} 100%)",
                box_shadow=f"0 8px 24px rgba(16, 163, 127, 0.4), 0 0 40px rgba(16, 163, 127, 0.2)",
                margin_bottom="32px",
                position="relative",
                z_index="1",
                transition="all 0.3s ease",
            ),
            
            # Icon
            rx.box(
                rx.icon(
                    tag=icon,
                    size=36,
                    color=color,
                ),
                margin_bottom="24px",
            ),
            
            # Title
            rx.heading(
                title,
                size="6",
                color=T.text_primary,
                margin_bottom="16px",
                font_weight="700",
                text_align="center",
            ),
            
            # Description
            rx.text(
                description,
                color=T.text_secondary,
                font_size="15px",
                text_align="center",
                line_height="1.7",
            ),
            
            # Decorative bottom element
            rx.box(
                rx.html(
                    f'''<svg width="60" height="4" viewBox="0 0 60 4" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="60" height="4" rx="2" fill="{color}" opacity="0.3"/>
                        <rect width="30" height="4" rx="2" fill="{color}">
                            <animate attributeName="width" values="30;45;30" dur="2s" repeatCount="indefinite"/>
                        </rect>
                    </svg>''',
                ),
                margin_top="24px",
                display="flex",
                justify_content="center",
            ),
            
            display="flex",
            flex_direction="column",
            align_items="center",
            position="relative",
            z_index="1",
        ),
        
        # Card styling
        background=T.bg_card,
        padding="48px 32px",
        border_radius="24px",
        border="2px solid transparent",
        width=["100%", "100%", "350px"],
        min_height="420px",
        position="relative",
        overflow="hidden",
        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
        box_shadow=T.shadow_md,
        _hover={
            "transform": "translateY(-8px) scale(1.02)",
            "box_shadow": f"0 20px 48px rgba(0, 0, 0, 0.15), 0 0 0 2px {color}",
            "border_color": color,
        },
    )


def step_item(number: str, title: str, description: str, icon: str) -> rx.Component:
    """Process step component with decorative SVG."""
    
    return rx.box(
        rx.box(
            # Decoratieve achtergrond cirkel
            rx.html(
                f'''<svg width="100%" height="80" viewBox="0 0 100 80" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 50%; transform: translateX(-50%);">
                    <circle cx="50" cy="30" r="35" fill="{COLORS['primary_green']}" opacity="0.05"/>
                </svg>''',
                position="absolute",
                top="0",
                left="0",
                width="100%",
                pointer_events="none",
            ),
            rx.box(
                rx.text(
                    number,
                    font_size="24px",
                    font_weight="700",
                    color="white",
                    text_align="center",
                ),
                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                width="60px",
                height="60px",
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="50%",
                margin_bottom="20px",
                font_weight="700",
                box_shadow="0 4px 12px rgba(34, 139, 34, 0.3)",
                position="relative",
                z_index="1",
            ),
            rx.heading(
                title,
                size="5",
                color=T.text_primary,
                margin_bottom="12px",
                font_weight="600",
            ),
            rx.text(
                description,
                color=T.text_secondary,
                font_size="15px",
                text_align="center",
                line_height="1.6",
            ),
            text_align="center",
            position="relative",
        ),
        background=T.bg_card,
        padding="32px",
        border_radius="14px",
        border=f"1px solid {T.border_light}",
        max_width="300px",
        transition="all 0.3s ease",
        position="relative",
        overflow="hidden",
        _hover={
            "box_shadow": "0 12px 32px rgba(0, 0, 0, 0.1)",
            "transform": "translateY(-4px)",
            "border_color": T.primary,
        },
    )


def benefit_item(icon_name: str, text: str) -> rx.Component:
    """Benefit list item with icon."""
    
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon(
                    icon_name,
                    size=20,
                    color=T.primary,
                ),
                background=f"rgba(34, 139, 34, 0.1)",
                width="40px",
                height="40px",
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="10px",
            ),
            rx.text(
                text,
                font_size="16px",
                color=T.text_primary,
                font_weight="500",
            ),
            spacing="3",
            align="center",
        ),
        margin_bottom="20px",
        transition="all 0.3s ease",
        _hover={
            "transform": "translateX(8px)",
        },
        padding="12px 0",
    )


def education_illustration_svg() -> rx.Component:
    """Modern SVG illustratie voor onderwijs met student en AI elementen."""
    return rx.html(
        f'''<svg width="100%" height="100%" viewBox="0 0 500 400" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{COLORS['primary_green']};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{COLORS['dark_green']};stop-opacity:1" />
                </linearGradient>
                <linearGradient id="grad2" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
                <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
                    <feOffset dx="0" dy="4" result="offsetblur"/>
                    <feComponentTransfer>
                        <feFuncA type="linear" slope="0.15"/>
                    </feComponentTransfer>
                    <feMerge>
                        <feMergeNode/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            
            <!-- Floating background elements -->
            <circle cx="80" cy="60" r="40" fill="url(#grad1)" opacity="0.1">
                <animate attributeName="cy" values="60;50;60" dur="4s" repeatCount="indefinite"/>
            </circle>
            <circle cx="420" cy="320" r="50" fill="url(#grad2)" opacity="0.1">
                <animate attributeName="cy" values="320;310;320" dur="5s" repeatCount="indefinite"/>
            </circle>
            <circle cx="400" cy="80" r="30" fill="{COLORS['primary_green']}" opacity="0.08">
                <animate attributeName="r" values="30;35;30" dur="3s" repeatCount="indefinite"/>
            </circle>
            
            <!-- Main computer/laptop -->
            <g filter="url(#shadow)">
                <!-- Screen -->
                <rect x="120" y="140" width="260" height="160" rx="8" fill="#2d3748"/>
                <rect x="130" y="150" width="240" height="135" rx="4" fill="#f7fafc"/>
                
                <!-- Screen content - AI interface -->
                <rect x="145" y="165" width="80" height="20" rx="4" fill="url(#grad1)" opacity="0.9"/>
                <text x="155" y="179" font-family="Arial" font-size="10" fill="white" font-weight="bold">AI Assistant</text>
                
                <!-- Chat lines -->
                <rect x="145" y="195" width="180" height="6" rx="3" fill="{COLORS['primary_green']}" opacity="0.3"/>
                <rect x="145" y="207" width="150" height="6" rx="3" fill="{COLORS['primary_green']}" opacity="0.3"/>
                <rect x="145" y="219" width="200" height="6" rx="3" fill="{COLORS['primary_green']}" opacity="0.3"/>
                <rect x="145" y="231" width="130" height="6" rx="3" fill="{COLORS['primary_green']}" opacity="0.3"/>
                
                <!-- Response bubble -->
                <rect x="145" y="245" width="160" height="30" rx="12" fill="url(#grad1)" opacity="0.15"/>
                <circle cx="158" cy="260" r="2" fill="{COLORS['primary_green']}"/>
                <circle cx="166" cy="260" r="2" fill="{COLORS['primary_green']}"/>
                <circle cx="174" cy="260" r="2" fill="{COLORS['primary_green']}"/>
                
                <!-- Keyboard base -->
                <rect x="120" y="300" width="260" height="10" rx="6" fill="#2d3748"/>
            </g>
            
            <!-- Student character -->
            <g transform="translate(330, 180)">
                <!-- Head -->
                <circle cx="0" cy="0" r="35" fill="#667eea" opacity="0.9"/>
                <!-- Face features -->
                <circle cx="-10" cy="-5" r="3" fill="white"/>
                <circle cx="10" cy="-5" r="3" fill="white"/>
                <!-- Smile -->
                <path d="M -12,8 Q 0,15 12,8" stroke="white" stroke-width="3" fill="none" stroke-linecap="round"/>
                <!-- Hair/cap -->
                <ellipse cx="0" cy="-20" rx="25" ry="18" fill="#2d3748" opacity="0.8"/>
                
                <!-- Body -->
                <ellipse cx="0" cy="60" rx="30" ry="35" fill="#667eea" opacity="0.8"/>
                
                <!-- Arm pointing to screen -->
                <path d="M -25,45 L -60,30" stroke="#667eea" stroke-width="8" stroke-linecap="round" opacity="0.8"/>
                <circle cx="-60" cy="30" r="6" fill="#667eea" opacity="0.8"/>
            </g>
            
            <!-- Floating icons around -->
            <!-- Book icon -->
            <g transform="translate(90, 250)" opacity="0.6">
                <rect x="0" y="0" width="30" height="36" rx="2" fill="{COLORS['primary_green']}"/>
                <line x1="15" y1="0" x2="15" y2="36" stroke="white" stroke-width="2"/>
                <line x1="7" y1="12" x2="13" y2="12" stroke="white" stroke-width="1.5"/>
                <line x1="17" y1="12" x2="23" y2="12" stroke="white" stroke-width="1.5"/>
                <animate attributeName="opacity" values="0.6;1;0.6" dur="3s" repeatCount="indefinite"/>
            </g>
            
            <!-- Graduation cap icon -->
            <g transform="translate(410, 140)" opacity="0.6">
                <polygon points="15,0 30,7 15,10 0,7" fill="{COLORS['dark_green']}"/>
                <rect x="12" y="10" width="6" height="12" fill="{COLORS['dark_green']}"/>
                <circle cx="15" cy="-3" r="2" fill="{COLORS['primary_green']}"/>
                <line x1="15" y1="-3" x2="15" y2="0" stroke="{COLORS['primary_green']}" stroke-width="1"/>
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2.5s" repeatCount="indefinite"/>
            </g>
            
            <!-- Star sparkles -->
            <g opacity="0.7">
                <circle cx="70" cy="120" r="3" fill="#ffd700">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" repeatCount="indefinite"/>
                </circle>
                <circle cx="440" cy="240" r="4" fill="#ffd700">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" begin="0.5s"/>
                </circle>
                <circle cx="100" cy="340" r="3" fill="#ffd700">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.8s" repeatCount="indefinite" begin="1s"/>
                </circle>
            </g>
            
            <!-- AI sparkle effect around character -->
            <g opacity="0.5">
                <circle cx="400" cy="150" r="2" fill="{COLORS['primary_green']}">
                    <animate attributeName="r" values="2;4;2" dur="2s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/>
                </circle>
                <circle cx="385" cy="200" r="2" fill="{COLORS['primary_green']}">
                    <animate attributeName="r" values="2;4;2" dur="2.2s" repeatCount="indefinite" begin="0.3s"/>
                    <animate attributeName="opacity" values="0.5;1;0.5" dur="2.2s" repeatCount="indefinite" begin="0.3s"/>
                </circle>
                <circle cx="420" cy="185" r="2" fill="{COLORS['primary_green']}">
                    <animate attributeName="r" values="2;4;2" dur="1.8s" repeatCount="indefinite" begin="0.6s"/>
                    <animate attributeName="opacity" values="0.5;1;0.5" dur="1.8s" repeatCount="indefinite" begin="0.6s"/>
                </circle>
            </g>
        </svg>'''
    )

