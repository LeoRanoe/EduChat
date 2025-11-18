"""Landing page with authentication - Dutch Surinamese Education Focus."""

import reflex as rx
from educhat.state.auth_state import AuthState
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
        
        # Navigation bar
        rx.box(
            rx.box(
                rx.hstack(
                    rx.icon("graduation-cap", size=28, color=COLORS["primary_green"]),
                    rx.heading(
                        "EduChat",
                        size="6",
                        color=COLORS["primary_green"],
                        font_weight="700",
                    ),
                    spacing="2",
                ),
                rx.hstack(
                    rx.button(
                        "Inloggen",
                        background="transparent",
                        color=COLORS["text_primary"],
                        border="none",
                        cursor="pointer",
                        font_weight="600",
                        font_size="15px",
                        padding="8px 16px",
                        transition="all 0.2s ease",
                        _hover={"color": COLORS["primary_green"]},
                        on_click=AuthState.toggle_auth_modal,
                    ),
                    rx.button(
                        "Start Nu",
                        background=COLORS["primary_green"],
                        color="white",
                        border="none",
                        border_radius="8px",
                        cursor="pointer",
                        font_weight="600",
                        font_size="15px",
                        padding="10px 24px",
                        transition="all 0.2s ease",
                        _hover={
                            "background": COLORS["dark_green"],
                            "transform": "translateY(-2px)",
                        },
                        on_click=AuthState.toggle_auth_modal,
                    ),
                    spacing="3",
                ),
                display="flex",
                justify_content="space-between",
                align_items="center",
                width="100%",
            ),
            background="white",
            padding="16px 32px",
            border_bottom=f"1px solid {COLORS['border']}",
            position="sticky",
            top="0",
            z_index="100",
            box_shadow="0 2px 8px rgba(0, 0, 0, 0.04)",
        ),
        
        # Hero section
        rx.box(
            rx.box(
                # Left content
                rx.box(
                    rx.heading(
                        "Jouw AI Assistent voor Surinaams Onderwijs",
                        size="9",
                        color=COLORS["text_primary"],
                        margin_bottom="20px",
                        animation="fadeInLeft 0.8s ease-out",
                        font_weight="700",
                        line_height="1.2",
                    ),
                    rx.heading(
                        "Vind de Juiste Opleiding in Suriname",
                        size="7",
                        color=COLORS["primary_green"],
                        margin_bottom="32px",
                        animation="fadeInLeft 0.8s ease-out 0.1s backwards",
                    ),
                    rx.text(
                        "Krijg direct antwoord op al je vragen over opleidingen, inschrijvingen, toelatingseisen en deadlines in Suriname. EduChat helpt je de beste studiekeuze te maken.",
                        font_size="18px",
                        color=COLORS["text_secondary"],
                        line_height="1.8",
                        margin_bottom="32px",
                        animation="fadeIn 0.8s ease-out 0.2s backwards",
                        max_width="500px",
                    ),
                    
                    # CTA buttons
                    rx.box(
                        rx.button(
                            rx.hstack(
                                rx.icon("message-circle", size=20),
                                rx.text("Begin Chat"),
                                spacing="2",
                            ),
                            padding="16px 32px",
                            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                            color="white",
                            border="none",
                            border_radius="10px",
                            cursor="pointer",
                            font_weight="600",
                            font_size="16px",
                            transition="all 0.3s ease",
                            box_shadow="0 8px 24px rgba(34, 139, 34, 0.3)",
                            _hover={
                                "transform": "translateY(-4px)",
                                "box_shadow": "0 12px 32px rgba(34, 139, 34, 0.4)",
                            },
                            on_click=AuthState.toggle_auth_modal,
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("play", size=20),
                                rx.text("Probeer als Gast"),
                                spacing="2",
                            ),
                            padding="16px 32px",
                            background="white",
                            color=COLORS["primary_green"],
                            border=f"2px solid {COLORS['primary_green']}",
                            border_radius="10px",
                            cursor="pointer",
                            font_weight="600",
                            font_size="16px",
                            transition="all 0.3s ease",
                            _hover={
                                "background": f"rgba(34, 139, 34, 0.05)",
                                "transform": "translateY(-4px)",
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
                        rx.hstack(
                            check_circle_svg(16),
                            rx.text(
                                "Gratis te gebruiken",
                                font_size="14px",
                                color=COLORS["text_secondary"],
                            ),
                            spacing="2",
                        ),
                        rx.hstack(
                            check_circle_svg(16),
                            rx.text(
                                "24/7 beschikbaar",
                                font_size="14px",
                                color=COLORS["text_secondary"],
                            ),
                            spacing="2",
                        ),
                        rx.hstack(
                            check_circle_svg(16),
                            rx.text(
                                "Focus op Suriname",
                                font_size="14px",
                                color=COLORS["text_secondary"],
                            ),
                            spacing="2",
                        ),
                        display="flex",
                        flex_wrap="wrap",
                        gap="24px",
                        margin_top="32px",
                        animation="fadeIn 0.8s ease-out 0.4s backwards",
                    ),
                    
                    flex="1",
                    display="flex",
                    flex_direction="column",
                    justify_content="center",
                ),
                
                # Right side - Interactive demo with SVG
                rx.box(
                    rx.box(
                        # SVG illustratie
                        rx.box(
                            education_illustration_svg(),
                            width="100%",
                            max_width="400px",
                            animation="fadeIn 1s ease-out 0.5s backwards",
                        ),
                        # Chat bubble preview
                        rx.box(
                            rx.box(
                                rx.text(
                                    "Welke opleidingen biedt MINOV aan?",
                                    font_size="13px",
                                    color=COLORS["text_primary"],
                                    font_weight="500",
                                ),
                                background=COLORS["light_green"],
                                padding="12px 16px",
                                border_radius="12px 12px 2px 12px",
                                box_shadow="0 4px 12px rgba(0, 0, 0, 0.08)",
                                margin_bottom="8px",
                                max_width="80%",
                                margin_left="auto",
                                animation="slideInRight 0.6s ease-out 0.7s backwards",
                            ),
                            rx.box(
                                rx.hstack(
                                    rx.icon("sparkles", size=14, color=COLORS["primary_green"]),
                                    rx.text(
                                        "MINOV biedt diverse technische opleidingen...",
                                        font_size="13px",
                                        color=COLORS["text_secondary"],
                                    ),
                                    spacing="2",
                                    align="start",
                                ),
                                background="white",
                                padding="12px 16px",
                                border_radius="12px 12px 12px 2px",
                                border=f"1px solid {COLORS['border']}",
                                box_shadow="0 2px 8px rgba(0, 0, 0, 0.06)",
                                max_width="85%",
                                animation="slideInLeft 0.6s ease-out 0.9s backwards",
                            ),
                            display="flex",
                            flex_direction="column",
                            gap="8px",
                            margin_top="24px",
                        ),
                        background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_gray']} 100%)",
                        padding="32px",
                        border_radius="20px",
                        box_shadow="0 20px 60px rgba(0, 0, 0, 0.08)",
                        border=f"1px solid {COLORS['border']}",
                        overflow="hidden",
                    ),
                    flex="1",
                    display=["none", "none", "flex"],
                    align_items="center",
                    justify_content="center",
                ),
                
                display="flex",
                gap="64px",
                align_items="center",
                flex_wrap="wrap",
                max_width="1400px",
                margin="0 auto",
            ),
            
            padding="80px 32px 120px 32px",
            background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_gray']} 100%)",
            min_height="100vh",
            display="flex",
            align_items="center",
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
        
        # How it works section
        rx.box(
            rx.box(
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
                    margin_bottom="64px",
                    max_width="600px",
                    margin_x="auto",
                ),
                
                # Steps
                rx.box(
                    step_item(
                        number="1",
                        title="Stel je Vraag",
                        description="Typ je vraag over opleidingen, inschrijvingen of toelatingseisen",
                        icon="message-square-plus",
                    ),
                    rx.box(
                        rx.icon("arrow-right", size=32, color=COLORS["primary_green"]),
                        display=["none", "flex"],
                        align_items="center",
                        justify_content="center",
                    ),
                    step_item(
                        number="2",
                        title="Krijg Direct Antwoord",
                        description="Ontvang een duidelijk antwoord met alle informatie die je nodig hebt",
                        icon="lightbulb",
                    ),
                    rx.box(
                        rx.icon("arrow-right", size=32, color=COLORS["primary_green"]),
                        display=["none", "flex"],
                        align_items="center",
                        justify_content="center",
                    ),
                    step_item(
                        number="3",
                        title="Maak je Keuze",
                        description="Gebruik de informatie om de beste studiekeuze te maken",
                        icon="check-circle",
                    ),
                    
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    gap="24px",
                    flex_wrap="wrap",
                    max_width="1200px",
                    margin="0 auto",
                ),
                
                max_width="1400px",
                margin="0 auto",
            ),
            
            padding="120px 32px",
            background="white",
        ),
        
        # Benefits section
        rx.box(
            rx.box(
                # Left side
                rx.box(
                    rx.heading(
                        "Waarom Studenten voor EduChat Kiezen",
                        size="8",
                        color=COLORS["text_primary"],
                        margin_bottom="32px",
                        font_weight="700",
                    ),
                    benefit_item("school", "Informatie over alle onderwijsinstellingen in Suriname"),
                    benefit_item("clipboard-list", "Duidelijke uitleg over toelatingseisen en procedures"),
                    benefit_item("calendar", "Actuele deadlines en belangrijke data"),
                    benefit_item("message-circle", "Antwoorden in het Nederlands, makkelijk te begrijpen"),
                    benefit_item("target", "Persoonlijk studiekeuzeadvies op basis van jouw interesses"),
                    benefit_item("coins", "Volledig gratis, geen verborgen kosten"),
                    
                    flex="1",
                ),
                
                # Right side - illustration
                rx.box(
                    # Decoratieve SVG achtergrond
                    rx.html(
                        f'''<svg width="100%" height="100%" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.1;">
                            <circle cx="50" cy="50" r="40" fill="{COLORS['primary_green']}"/>
                            <circle cx="250" cy="100" r="60" fill="{COLORS['primary_green']}"/>
                            <circle cx="150" cy="250" r="50" fill="{COLORS['primary_green']}"/>
                            <path d="M100,150 Q150,100 200,150 T300,150" stroke="{COLORS['primary_green']}" stroke-width="3" fill="none" opacity="0.5"/>
                        </svg>''',
                        position="absolute",
                        top="0",
                        left="0",
                        width="100%",
                        height="100%",
                        pointer_events="none",
                    ),
                    # Centrale icoon
                    rx.box(
                        rx.html(
                            f'''<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <!-- Vlag van Suriname kleuren hint -->
                                <circle cx="50" cy="50" r="45" fill="{COLORS['primary_green']}" opacity="0.15"/>
                                <path d="M50,20 L60,35 L77,35 L64,46 L69,62 L50,50 L31,62 L36,46 L23,35 L40,35 Z" fill="{COLORS['primary_green']}"/>
                                <circle cx="50" cy="50" r="8" fill="{COLORS['dark_green']}"/>
                            </svg>''',
                        ),
                        margin_bottom="24px",
                    ),
                    rx.box(
                        rx.heading(
                            "Speciaal voor Surinaamse Studenten",
                            size="6",
                            color=COLORS["primary_green"],
                            font_weight="700",
                            margin_bottom="16px",
                            text_align="center",
                        ),
                        rx.text(
                            "Jouw gids door het Surinaamse onderwijssysteem",
                            font_size="16px",
                            color=COLORS["text_secondary"],
                            text_align="center",
                        ),
                        text_align="center",
                    ),
                    background="white",
                    padding="64px",
                    border_radius="16px",
                    box_shadow="0 12px 40px rgba(0, 0, 0, 0.08)",
                    position="relative",
                    display="flex",
                    flex_direction="column",
                    align_items="center",
                    justify_content="center",
                    min_height="300px",
                    flex="1",
                    overflow="hidden",
                ),
                
                display="flex",
                gap="64px",
                align_items="center",
                flex_wrap="wrap",
                max_width="1400px",
                margin="0 auto",
            ),
            
            padding="120px 32px",
            background=f"rgba(34, 139, 34, 0.05)",
        ),
        
        # CTA section
        rx.box(
            rx.box(
                rx.heading(
                    "Klaar om te Beginnen?",
                    size="8",
                    color="white",
                    text_align="center",
                    margin_bottom="24px",
                    font_weight="700",
                ),
                rx.text(
                    "Start nu met EduChat en krijg alle antwoorden die je nodig hebt voor je studiekeuze in Suriname",
                    font_size="20px",
                    color="rgba(255, 255, 255, 0.9)",
                    text_align="center",
                    max_width="600px",
                    margin_x="auto",
                    margin_bottom="48px",
                ),
                
                rx.button(
                    rx.hstack(
                        rx.icon("message-circle", size=20),
                        rx.text("Begin Nu Gratis"),
                        spacing="2",
                    ),
                    padding="18px 48px",
                    background="white",
                    color=COLORS["primary_green"],
                    border="none",
                    border_radius="10px",
                    cursor="pointer",
                    font_weight="700",
                    font_size="18px",
                    transition="all 0.3s ease",
                    box_shadow="0 8px 24px rgba(0, 0, 0, 0.2)",
                    _hover={
                        "transform": "translateY(-4px)",
                        "box_shadow": "0 12px 36px rgba(0, 0, 0, 0.3)",
                    },
                    on_click=AuthState.toggle_auth_modal,
                    display="block",
                    margin_x="auto",
                ),
                
                max_width="800px",
                margin="0 auto",
                text_align="center",
            ),
            
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            padding="100px 32px",
        ),
        
        width="100vw",
        min_height="100vh",
        overflow_x="hidden",
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

