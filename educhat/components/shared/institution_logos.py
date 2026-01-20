"""Institution logos component for displaying partner educational institutions."""
import reflex as rx
from educhat.styles.theme import COLORS


# Map of institution short names to logo file paths
INSTITUTION_LOGOS = {
    "adfontes": "ADfontes.png",
    "adekus": "AntondekomUni.png",
    "havo": "Havo.png",
    "lobo": "Lobo.png",
    "lyco": "Lyco.png",
    "ptc": "NEW-PTC-Logo.png",
    "unasat": "Unasat.png",
    "vanguard": "Vanguard.png",
}


def institution_logo_card(logo_path: str, alt_text: str = "Institution Logo") -> rx.Component:
    """Single institution logo card with hover effect.
    
    Args:
        logo_path: Path to the logo image
        alt_text: Alt text for accessibility
    """
    return rx.box(
        rx.image(
            src=f"/{logo_path}",
            alt=alt_text,
            width="100%",
            height="auto",
            object_fit="contain",
            loading="lazy",
        ),
        padding="12px",
        background="white",
        border_radius="12px",
        border=f"1px solid {COLORS['border_light']}",
        box_shadow="0 2px 8px rgba(0,0,0,0.04)",
        transition="all 0.3s ease",
        cursor="pointer",
        _hover={
            "box_shadow": "0 8px 24px rgba(0,0,0,0.12)",
            "transform": "translateY(-4px)",
            "border_color": COLORS["primary_light"],
        },
        height="80px",
        display="flex",
        align_items="center",
        justify_content="center",
    )


def institution_logos_grid(
    logos: list[str] = None,
    columns: int = 4,
    show_title: bool = True,
) -> rx.Component:
    """Grid of institution logos.
    
    Args:
        logos: List of logo paths. If None, uses all available logos
        columns: Number of columns in the grid
        show_title: Whether to show the section title
    """
    if logos is None:
        logos = list(INSTITUTION_LOGOS.values())
    
    return rx.vstack(
        rx.cond(
            show_title,
            rx.heading(
                "Partner Instellingen",
                font_size="1.125rem",
                font_weight="700",
                color=COLORS["text_primary"],
                margin_bottom="1rem",
                text_align="center",
            ),
            rx.fragment(),
        ),
        rx.box(
            *[
                institution_logo_card(logo_path=logo)
                for logo in logos
            ],
            display="grid",
            grid_template_columns=[
                "repeat(2, 1fr)",  # Mobile: 2 columns
                "repeat(3, 1fr)",  # Tablet: 3 columns
                f"repeat({columns}, 1fr)",  # Desktop: specified columns
            ],
            gap="16px",
            width="100%",
        ),
        spacing="4",
        width="100%",
        align="center",
    )


def institution_logos_carousel(
    logos: list[str] = None,
    on_white_background: bool = False,
) -> rx.Component:
    """Horizontal scrolling carousel of institution logos.
    
    Args:
        logos: List of logo paths. If None, uses all available logos
        on_white_background: If True, uses darker styling for white backgrounds
    """
    if logos is None:
        logos = list(INSTITUTION_LOGOS.values())
    
    text_color = COLORS["text_primary"] if on_white_background else "white"
    logo_bg = "white" if on_white_background else "rgba(255,255,255,0.1)"
    border_color = COLORS["border_light"] if on_white_background else "rgba(255,255,255,0.2)"
    
    return rx.vstack(
        rx.text(
            "Onderwijsinstellingen in Suriname",
            font_size="0.875rem",
            font_weight="600",
            color=text_color,
            opacity="0.9",
            margin_bottom="0.75rem",
            text_align="center",
        ),
        rx.box(
            rx.hstack(
                *[
                    rx.box(
                        rx.image(
                            src=f"/{logo}",
                            alt="Institution Logo",
                            width="auto",
                            height="50px",
                            object_fit="contain",
                            loading="lazy",
                        ),
                        padding="12px 20px",
                        background=logo_bg,
                        border_radius="10px",
                        border=f"1px solid {border_color}",
                        transition="all 0.3s ease",
                        flex_shrink="0",
                        _hover={
                            "transform": "scale(1.05)",
                            "box_shadow": "0 4px 12px rgba(0,0,0,0.15)",
                        },
                    )
                    for logo in logos
                ],
                spacing="3",
                overflow_x="auto",
                overflow_y="hidden",
                width="100%",
                padding_y="8px",
                css={
                    "&::-webkit-scrollbar": {
                        "height": "6px",
                    },
                    "&::-webkit-scrollbar-track": {
                        "background": "rgba(0,0,0,0.05)",
                        "border-radius": "3px",
                    },
                    "&::-webkit-scrollbar-thumb": {
                        "background": "rgba(0,0,0,0.2)",
                        "border-radius": "3px",
                    },
                    "&::-webkit-scrollbar-thumb:hover": {
                        "background": "rgba(0,0,0,0.3)",
                    },
                },
            ),
            width="100%",
        ),
        spacing="2",
        width="100%",
        align="center",
    )


def compact_logos_row(
    logos: list[str] = None,
    max_logos: int = 5,
) -> rx.Component:
    """Compact row of logos with infinite scroll animation.
    
    Args:
        logos: List of logo paths. If None, uses all available logos
        max_logos: Maximum number of logos to display (ignored for infinite scroll, uses all)
    """
    if logos is None:
        logos = list(INSTITUTION_LOGOS.values())
    
    # Duplicate logos for seamless infinite scroll
    all_logos = logos + logos
    
    return rx.box(
        rx.box(
            rx.hstack(
                *[
                    rx.box(
                        rx.image(
                            src=f"/{logo}",
                            alt="Institution",
                            height="50px",
                            width="auto",
                            object_fit="contain",
                            loading="lazy",
                            filter="grayscale(100%)",
                            opacity="0.6",
                            transition="all 0.3s ease",
                            _hover={
                                "filter": "grayscale(0%)",
                                "opacity": "1",
                                "transform": "scale(1.1)",
                            },
                        ),
                        padding="0 30px",
                        flex_shrink="0",
                    )
                    for logo in all_logos
                ],
                spacing="0",
                align="center",
            ),
            animation="scroll 40s linear infinite",
            display="flex",
            _hover={
                "animation-play-state": "paused",
            },
        ),
        overflow="hidden",
        width="100%",
        position="relative",
        mask_image="linear-gradient(to right, transparent, black 10%, black 90%, transparent)",
        webkit_mask_image="linear-gradient(to right, transparent, black 10%, black 90%, transparent)",
        css={
            "@keyframes scroll": {
                "0%": {"transform": "translateX(0)"},
                "100%": {"transform": "translateX(-50%)"},
            },
        },
    )
