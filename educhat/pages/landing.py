"""Landing page with authentication - Dutch Surinamese Education Focus."""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.state.app_state import AppState
from educhat.components.auth import auth_modal
from educhat.styles.theme import COLORS


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
    return rx.html(
        f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="{color}" opacity="0.1"/>
            <path d="M9 12l2 2 4-4" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2"/>
        </svg>'''
    )


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
                        rx.icon("graduation-cap", size=32, color=COLORS["primary_green"]),
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
                            color=COLORS["primary_green"],
                            font_weight="800",
                            margin_bottom="2px",
                        ),
                        rx.text(
                            "Surinaams Onderwijs AI",
                            font_size="11px",
                            color=COLORS["text_secondary"],
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
                            rx.text("Inloggen", display=["none", "block", "block"]),
                            spacing="2",
                            align="center",
                        ),
                        background="transparent",
                        color=COLORS["text_primary"],
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
                    rx.button(
                        rx.hstack(
                            rx.icon("sparkles", size=18),
                            rx.text("Start Nu"),
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
            background="rgba(255, 255, 255, 0.95)",
            backdrop_filter="blur(12px)",
            padding="20px 32px",
            border_bottom=f"1px solid rgba(16, 163, 127, 0.1)",
            position="sticky",
            top="0",
            z_index="100",
            box_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
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
                        rx.icon("zap", size=16, color=COLORS["primary_green"]),
                        rx.text("AI-Powered Studiegids", font_size="13px", font_weight="700", color=COLORS["primary_green"]),
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
                        "Jouw AI Assistent voor Surinaams Onderwijs",
                        size="9",
                        color=COLORS["text_primary"],
                        margin_bottom="24px",
                        animation="fadeInLeft 0.8s ease-out",
                        font_weight="800",
                        line_height="1.15",
                        letter_spacing="-0.02em",
                    ),
                    rx.heading(
                        "Vind de Juiste Opleiding in Suriname",
                        size="7",
                        background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                        background_clip="text",
                        color="transparent",
                        margin_bottom="24px",
                        animation="fadeInLeft 0.8s ease-out 0.1s backwards",
                        font_weight="700",
                    ),
                    rx.text(
                        "Krijg direct antwoord op al je vragen over opleidingen, inschrijvingen, toelatingseisen en deadlines in Suriname. EduChat helpt je de beste studiekeuze te maken.",
                        font_size="18px",
                        color=COLORS["text_secondary"],
                        line_height="1.7",
                        margin_bottom="40px",
                        animation="fadeIn 0.8s ease-out 0.2s backwards",
                        max_width="580px",
                    ),
                    
                    # CTA buttons
                    rx.box(
                        rx.button(
                            rx.hstack(
                                rx.icon("sparkles", size=22),
                                rx.text("Begin Chat", font_size="17px", font_weight="700"),
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
                                rx.text("Probeer als Gast", font_size="16px"),
                                spacing="2",
                            ),
                            padding="18px 36px",
                            background="white",
                            color=COLORS["primary_green"],
                            border=f"2px solid {COLORS['primary_green']}",
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
                                check_circle_svg(18, COLORS["primary_green"]),
                                rx.text(
                                    "Gratis te gebruiken",
                                    font_size="15px",
                                    color=COLORS["text_secondary"],
                                    font_weight="600",
                                ),
                                display="flex",
                                align_items="center",
                                gap="10px",
                            ),
                            rx.box(
                                check_circle_svg(18, COLORS["primary_green"]),
                                rx.text(
                                    "24/7 beschikbaar",
                                    font_size="15px",
                                    color=COLORS["text_secondary"],
                                    font_weight="600",
                                ),
                                display="flex",
                                align_items="center",
                                gap="10px",
                            ),
                            rx.box(
                                check_circle_svg(18, COLORS["primary_green"]),
                                rx.text(
                                    "Focus op Suriname",
                                    font_size="15px",
                                    color=COLORS["text_secondary"],
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
                        background="white",
                        border_radius="16px",
                        box_shadow="0 8px 28px rgba(0, 0, 0, 0.08)",
                        border=f"1px solid rgba(16, 163, 127, 0.1)",
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
                            max_width="350px",
                            margin_x="auto",
                            animation="fadeIn 1s ease-out 0.5s backwards",
                        ),
                        
                        # Chat bubble preview with enhanced styling
                        rx.box(
                            rx.box(
                                rx.box(
                                    rx.text(
                                        "Welke opleidingen biedt MINOV aan?",
                                        font_size="14px",
                                        color=COLORS["text_primary"],
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
                                        rx.icon("sparkles", size=16, color=COLORS["primary_green"]),
                                        rx.text(
                                            "MINOV biedt diverse technische opleidingen...",
                                            font_size="14px",
                                            color=COLORS["text_secondary"],
                                            font_weight="500",
                                        ),
                                        spacing="2",
                                        align="start",
                                    ),
                                    padding="14px 20px",
                                    background="white",
                                    border_radius="16px 16px 16px 4px",
                                    border=f"2px solid {COLORS['border']}",
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
                                rx.box(width="8px", height="8px", background=COLORS["primary_green"], border_radius="50%", animation="pulse 1.4s ease-in-out infinite"),
                                rx.box(width="8px", height="8px", background=COLORS["primary_green"], border_radius="50%", animation="pulse 1.4s ease-in-out 0.2s infinite"),
                                rx.box(width="8px", height="8px", background=COLORS["primary_green"], border_radius="50%", animation="pulse 1.4s ease-in-out 0.4s infinite"),
                                display="flex",
                                gap="6px",
                            ),
                            padding="12px 20px",
                            background="white",
                            border_radius="16px",
                            border=f"1px solid {COLORS['border']}",
                            box_shadow="0 2px 12px rgba(0, 0, 0, 0.06)",
                            width="fit-content",
                            margin_top="12px",
                            animation="fadeIn 0.6s ease-out 1.1s backwards",
                        ),
                        
                        background="white",
                        padding="40px",
                        border_radius="24px",
                        box_shadow="0 20px 60px rgba(0, 0, 0, 0.12)",
                        border=f"2px solid rgba(16, 163, 127, 0.1)",
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
            background=f"linear-gradient(180deg, rgba(16, 163, 127, 0.02) 0%, white 100%)",
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
                    "Alles wat je Nodig Hebt voor je Studiekeuze",
                    size="8",
                    color=COLORS["text_primary"],
                    text_align="center",
                    margin_bottom="16px",
                    font_weight="700",
                ),
                rx.text(
                    "Complete ondersteuning voor het Surinaamse onderwijssysteem",
                    font_size="18px",
                    color=COLORS["text_secondary"],
                    text_align="center",
                    margin_bottom="64px",
                    max_width="600px",
                    margin_x="auto",
                ),
                
                # Features grid
                rx.box(
                    feature_card(
                        icon="school",
                        title="Opleidingen Vinden",
                        description="Ontdek alle beschikbare opleidingen bij MINOV, universiteiten en andere instellingen in Suriname",
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="clipboard-list",
                        title="Toelatingseisen",
                        description="Krijg duidelijke informatie over toelatingseisen, benodigde documenten en inschrijvingsprocedures",
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="calendar",
                        title="Deadlines & Data",
                        description="Blijf op de hoogte van belangrijke deadlines voor inschrijvingen en aanmeldingen",
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="message-circle",
                        title="Directe Antwoorden",
                        description="Stel je vraag in het Nederlands en krijg meteen een helder antwoord van onze AI",
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="compass",
                        title="Studiekeuzebegeleiding",
                        description="Persoonlijk advies om de opleiding te vinden die bij jou past",
                        accent_color=COLORS["primary_green"],
                    ),
                    feature_card(
                        icon="shield",
                        title="Veilig & Privé",
                        description="Jouw gegevens zijn veilig en al je gesprekken blijven privé",
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
            background="white",
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
                    rx.icon("zap", size=18, color=COLORS["primary_green"], margin_right="8px"),
                    rx.text(
                        "Supersnel en Makkelijk",
                        font_size="14px",
                        font_weight="600",
                        color=COLORS["primary_green"],
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
                    "Zo Werkt EduChat",
                    size="8",
                    color=COLORS["text_primary"],
                    text_align="center",
                    margin_bottom="16px",
                    font_weight="700",
                ),
                rx.text(
                    "In drie eenvoudige stappen naar de juiste studiekeuze",
                    font_size="18px",
                    color=COLORS["text_secondary"],
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
                            title="Stel je Vraag",
                            description="Typ je vraag over opleidingen, toelatingseisen, inschrijvingen of studiefinanciering",
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
                            title="Krijg Direct Antwoord",
                            description="Ontvang binnen seconden een helder en compleet antwoord met alle benodigde informatie",
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
                            title="Maak je Keuze",
                            description="Gebruik de informatie om een weloverwogen studiekeuze te maken en je toekomst vorm te geven",
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
                        rx.icon("users", size=20, color=COLORS["primary_green"]),
                        rx.text("100+ Tevreden Studenten", font_size="14px", font_weight="600", color=COLORS["text_primary"]),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="12px 20px",
                        background="white",
                        border_radius="50px",
                        box_shadow="0 4px 12px rgba(0, 0, 0, 0.08)",
                    ),
                    rx.box(
                        rx.icon("clock", size=20, color=COLORS["primary_green"]),
                        rx.text("< 5 seconden reactietijd", font_size="14px", font_weight="600", color=COLORS["text_primary"]),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="12px 20px",
                        background="white",
                        border_radius="50px",
                        box_shadow="0 4px 12px rgba(0, 0, 0, 0.08)",
                    ),
                    rx.box(
                        rx.icon("shield-check", size=20, color=COLORS["primary_green"]),
                        rx.text("100% Betrouwbare Info", font_size="14px", font_weight="600", color=COLORS["text_primary"]),
                        display="flex",
                        align_items="center",
                        gap="8px",
                        padding="12px 20px",
                        background="white",
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
            background=f"linear-gradient(180deg, white 0%, {COLORS['light_gray']} 100%)",
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
                        rx.icon("sparkles", size=16, color=COLORS["primary_green"]),
                        rx.text("Waarom EduChat?", font_size="14px", font_weight="600", color=COLORS["primary_green"]),
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
                        color=COLORS["text_primary"],
                        margin_bottom="16px",
                        font_weight="800",
                        text_align="center",
                        line_height="1.2",
                    ),
                    rx.text(
                        "Speciaal ontwikkeld voor Surinaamse studenten met alle informatie die je nodig hebt",
                        font_size="18px",
                        color=COLORS["text_secondary"],
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
                                color=COLORS["text_primary"],
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Informatie over alle onderwijsinstellingen in Suriname, van universiteiten tot vakscholen",
                                font_size="15px",
                                color=COLORS["text_secondary"],
                                line_height="1.7",
                            ),
                        ),
                        background="white",
                        padding="40px",
                        border_radius="20px",
                        box_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
                        border=f"1px solid rgba(16, 163, 127, 0.1)",
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
                                color=COLORS["text_primary"],
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Begrijpelijke informatie over toelatingseisen, procedures en wat je moet verwachten",
                                font_size="15px",
                                color=COLORS["text_secondary"],
                                line_height="1.7",
                            ),
                        ),
                        background="white",
                        padding="40px",
                        border_radius="20px",
                        box_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
                        border=f"1px solid rgba(16, 163, 127, 0.1)",
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
                                color=COLORS["text_primary"],
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Mis geen belangrijke data met onze actuele informatie over inschrijvingen en deadlines",
                                font_size="15px",
                                color=COLORS["text_secondary"],
                                line_height="1.7",
                            ),
                        ),
                        background="white",
                        padding="40px",
                        border_radius="20px",
                        box_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
                        border=f"1px solid rgba(16, 163, 127, 0.1)",
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
                                color=COLORS["text_primary"],
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Antwoorden in helder Nederlands, makkelijk te begrijpen voor iedereen",
                                font_size="15px",
                                color=COLORS["text_secondary"],
                                line_height="1.7",
                            ),
                        ),
                        background="white",
                        padding="40px",
                        border_radius="20px",
                        box_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
                        border=f"1px solid rgba(16, 163, 127, 0.1)",
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
                                color=COLORS["text_primary"],
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Studiekeuzeadvies op maat, afgestemd op jouw interesses en doelen",
                                font_size="15px",
                                color=COLORS["text_secondary"],
                                line_height="1.7",
                            ),
                        ),
                        background="white",
                        padding="40px",
                        border_radius="20px",
                        box_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
                        border=f"1px solid rgba(16, 163, 127, 0.1)",
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
                                color=COLORS["text_primary"],
                                margin_bottom="12px",
                                font_weight="700",
                            ),
                            rx.text(
                                "Volledig gratis te gebruiken, geen verborgen kosten of verrassingen",
                                font_size="15px",
                                color=COLORS["text_secondary"],
                                line_height="1.7",
                            ),
                        ),
                        background="white",
                        padding="40px",
                        border_radius="20px",
                        box_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
                        border=f"1px solid rgba(16, 163, 127, 0.1)",
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
                                color=COLORS["primary_green"],
                                font_weight="700",
                                margin_bottom="8px",
                            ),
                            rx.text(
                                "Jouw persoonlijke gids door het Surinaamse onderwijssysteem",
                                font_size="16px",
                                color=COLORS["text_secondary"],
                            ),
                        ),
                        display="flex",
                        align_items="center",
                        gap="24px",
                    ),
                    background="white",
                    padding="32px 48px",
                    border_radius="20px",
                    box_shadow="0 8px 32px rgba(16, 163, 127, 0.12)",
                    border=f"2px solid {COLORS['primary_green']}",
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
            background=f"linear-gradient(180deg, {COLORS['light_gray']} 0%, white 100%)",
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
                    rx.icon("rocket", size=18, color="white"),
                    rx.text("Start Je Studiereis Vandaag", font_size="14px", font_weight="600", color="white"),
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
                    "Klaar om te Beginnen?",
                    size="9",
                    color="white",
                    text_align="center",
                    margin_bottom="20px",
                    font_weight="800",
                    line_height="1.2",
                ),
                rx.text(
                    "Start nu met EduChat en krijg alle antwoorden die je nodig hebt voor je studiekeuze in Suriname",
                    font_size="20px",
                    color="rgba(255, 255, 255, 0.95)",
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
                            rx.icon("sparkles", size=22),
                            rx.text("Begin Nu Gratis", font_size="18px", font_weight="700"),
                            rx.icon("arrow-right", size=20),
                            spacing="3",
                            align="center",
                        ),
                        padding="20px 56px",
                        background="white",
                        color=COLORS["primary_green"],
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
                        rx.heading("100+", size="6", color="white", font_weight="700", margin_bottom="4px"),
                        rx.text("Tevreden Studenten", font_size="14px", color="rgba(255, 255, 255, 0.8)"),
                        text_align="center",
                    ),
                    rx.box(
                        width="1px",
                        height="40px",
                        background="rgba(255, 255, 255, 0.2)",
                        display=["none", "block", "block"],
                    ),
                    rx.box(
                        rx.heading("<5 sec", size="6", color="white", font_weight="700", margin_bottom="4px"),
                        rx.text("Gemiddelde Reactietijd", font_size="14px", color="rgba(255, 255, 255, 0.8)"),
                        text_align="center",
                    ),
                    rx.box(
                        width="1px",
                        height="40px",
                        background="rgba(255, 255, 255, 0.2)",
                        display=["none", "block", "block"],
                    ),
                    rx.box(
                        rx.heading("24/7", size="6", color="white", font_weight="700", margin_bottom="4px"),
                        rx.text("Altijd Beschikbaar", font_size="14px", color="rgba(255, 255, 255, 0.8)"),
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
                    rx.icon("shield-check", size=18, color="rgba(255, 255, 255, 0.9)"),
                    rx.text(
                        "100% Gratis • Geen Registratie Vereist • Direct Beginnen",
                        font_size="14px",
                        color="rgba(255, 255, 255, 0.9)",
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
                color=COLORS["text_primary"],
                margin_bottom="12px",
                font_weight="600",
            ),
            rx.text(
                description,
                color=COLORS["text_secondary"],
                font_size="15px",
                line_height="1.7",
            ),
        ),
        background="white",
        padding="32px",
        border_radius="14px",
        border=f"1px solid {COLORS['border_light']}",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.05)",
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
                color=COLORS["text_primary"],
                margin_bottom="16px",
                font_weight="700",
                text_align="center",
            ),
            
            # Description
            rx.text(
                description,
                color=COLORS["text_secondary"],
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
        background="white",
        padding="48px 32px",
        border_radius="24px",
        border="2px solid transparent",
        width=["100%", "100%", "350px"],
        min_height="420px",
        position="relative",
        overflow="hidden",
        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
        box_shadow="0 8px 24px rgba(0, 0, 0, 0.08)",
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
                color=COLORS["text_primary"],
                margin_bottom="12px",
                font_weight="600",
            ),
            rx.text(
                description,
                color=COLORS["text_secondary"],
                font_size="15px",
                text_align="center",
                line_height="1.6",
            ),
            text_align="center",
            position="relative",
        ),
        background="white",
        padding="32px",
        border_radius="14px",
        border=f"1px solid {COLORS['border_light']}",
        max_width="300px",
        transition="all 0.3s ease",
        position="relative",
        overflow="hidden",
        _hover={
            "box_shadow": "0 12px 32px rgba(0, 0, 0, 0.1)",
            "transform": "translateY(-4px)",
            "border_color": COLORS["primary_green"],
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
                    color=COLORS["primary_green"],
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
                color=COLORS["text_primary"],
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
    """SVG illustratie voor onderwijs."""
    return rx.html(
        f'''<svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Achtergrond cirkel -->
            <circle cx="200" cy="150" r="120" fill="{COLORS['light_green']}" opacity="0.3"/>
            
            <!-- Boek -->
            <rect x="140" y="140" width="120" height="80" rx="4" fill="{COLORS['primary_green']}" opacity="0.2"/>
            <rect x="145" y="145" width="110" height="70" rx="3" fill="white"/>
            <line x1="200" y1="145" x2="200" y2="215" stroke="{COLORS['primary_green']}" stroke-width="2"/>
            <line x1="160" y1="165" x2="190" y2="165" stroke="{COLORS['primary_green']}" stroke-width="2" opacity="0.5"/>
            <line x1="160" y1="180" x2="190" y2="180" stroke="{COLORS['primary_green']}" stroke-width="2" opacity="0.5"/>
            <line x1="210" y1="165" x2="240" y2="165" stroke="{COLORS['primary_green']}" stroke-width="2" opacity="0.5"/>
            <line x1="210" y1="180" x2="240" y2="180" stroke="{COLORS['primary_green']}" stroke-width="2" opacity="0.5"/>
            
            <!-- Afstudeerhoed -->
            <polygon points="200,100 240,115 200,120 160,115" fill="{COLORS['primary_green']}"/>
            <rect x="195" y="120" width="10" height="20" fill="{COLORS['primary_green']}"/>
            <circle cx="200" cy="95" r="3" fill="{COLORS['dark_green']}"/>
            <line x1="200" y1="95" x2="200" y2="100" stroke="{COLORS['dark_green']}" stroke-width="2"/>
            
            <!-- Decoratieve elementen -->
            <circle cx="280" cy="100" r="8" fill="{COLORS['primary_green']}" opacity="0.3"/>
            <circle cx="120" cy="180" r="6" fill="{COLORS['primary_green']}" opacity="0.3"/>
            <circle cx="290" cy="200" r="10" fill="{COLORS['primary_green']}" opacity="0.2"/>
            
            <!-- Chat bubbel -->
            <circle cx="280" cy="160" r="25" fill="{COLORS['primary_green']}" opacity="0.9"/>
            <circle cx="275" cy="155" r="3" fill="white"/>
            <circle cx="280" cy="155" r="3" fill="white"/>
            <circle cx="285" cy="155" r="3" fill="white"/>
        </svg>'''
    )

