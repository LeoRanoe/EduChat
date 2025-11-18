"""Landing page with authentication."""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.components.auth import auth_modal
from educhat.styles.theme import COLORS


def landing() -> rx.Component:
    """Landing page that shows before authentication."""
    
    return rx.box(
        # Auth modal
        auth_modal(),
        
        # Hero section
        rx.box(
            # Logo and title
            rx.box(
                rx.heading(
                    "EduChat",
                    size="9",
                    color=COLORS["primary_green"],
                    margin_bottom="16px",
                    animation="fadeInDown 0.8s ease-out",
                ),
                rx.text(
                    "Your AI-Powered Study Assistant",
                    font_size="24px",
                    color=COLORS["text_primary"],
                    font_weight="500",
                    margin_bottom="16px",
                    animation="fadeInUp 0.8s ease-out 0.2s backwards",
                ),
                rx.text(
                    "Get instant help with your studies, homework, and exam preparation. Personalized learning with AI that understands your needs.",
                    font_size="18px",
                    color=COLORS["text_secondary"],
                    margin_bottom="48px",
                    max_width="700px",
                    text_align="center",
                    line_height="1.7",
                    animation="fadeInUp 0.8s ease-out 0.4s backwards",
                ),
                
                # CTA buttons
                rx.box(
                    rx.button(
                        rx.icon(tag="sparkles", size=20, margin_right="8px"),
                        "Get Started Free",
                        padding="16px 32px",
                        background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                        color="white",
                        border="none",
                        border_radius="12px",
                        cursor="pointer",
                        font_weight="600",
                        font_size="18px",
                        display="flex",
                        align_items="center",
                        transition="all 0.3s ease",
                        box_shadow="0 4px 20px rgba(16, 163, 127, 0.3)",
                        _hover={
                            "transform": "translateY(-3px)",
                            "box_shadow": "0 8px 30px rgba(16, 163, 127, 0.4)",
                        },
                        _active={
                            "transform": "translateY(-1px)",
                        },
                        on_click=AuthState.toggle_auth_modal,
                    ),
                    rx.button(
                        rx.icon(tag="user", size=20, margin_right="8px"),
                        "Continue as Guest",
                        padding="16px 32px",
                        background="white",
                        color=COLORS["primary_green"],
                        border=f"2px solid {COLORS['primary_green']}",
                        border_radius="12px",
                        cursor="pointer",
                        font_weight="600",
                        font_size="18px",
                        display="flex",
                        align_items="center",
                        transition="all 0.3s ease",
                        _hover={
                            "background": f"rgba(16, 163, 127, 0.05)",
                            "transform": "translateY(-3px)",
                            "box_shadow": "0 4px 20px rgba(0, 0, 0, 0.1)",
                        },
                        _active={
                            "transform": "translateY(-1px)",
                        },
                        on_click=AuthState.continue_as_guest,
                    ),
                    display="flex",
                    gap="20px",
                    flex_wrap="wrap",
                    justify_content="center",
                    animation="fadeInUp 0.8s ease-out 0.6s backwards",
                ),
                
                # Trust indicators
                rx.box(
                    rx.text(
                        rx.icon(tag="check", size=16, color=COLORS["primary_green"], margin_right="8px"),
                        "No credit card required",
                        display="flex",
                        align_items="center",
                        color=COLORS["text_secondary"],
                        font_size="14px",
                        margin_right="24px",
                    ),
                    rx.text(
                        rx.icon(tag="check", size=16, color=COLORS["primary_green"], margin_right="8px"),
                        "Free to start",
                        display="flex",
                        align_items="center",
                        color=COLORS["text_secondary"],
                        font_size="14px",
                        margin_right="24px",
                    ),
                    rx.text(
                        rx.icon(tag="check", size=16, color=COLORS["primary_green"], margin_right="8px"),
                        "24/7 Available",
                        display="flex",
                        align_items="center",
                        color=COLORS["text_secondary"],
                        font_size="14px",
                    ),
                    display="flex",
                    flex_wrap="wrap",
                    justify_content="center",
                    margin_top="32px",
                    gap="8px",
                    animation="fadeIn 1s ease-out 0.8s backwards",
                ),
                
                display="flex",
                flex_direction="column",
                align_items="center",
                text_align="center",
                max_width="900px",
                margin="0 auto",
            ),
            
            # Features section
            rx.box(
                rx.heading(
                    "Why Students Love EduChat",
                    size="8",
                    color=COLORS["text_primary"],
                    margin_bottom="16px",
                    text_align="center",
                    animation="fadeIn 1s ease-out",
                ),
                rx.text(
                    "Everything you need to excel in your studies",
                    font_size="18px",
                    color=COLORS["text_secondary"],
                    text_align="center",
                    margin_bottom="64px",
                    animation="fadeIn 1s ease-out 0.2s backwards",
                ),
                
                rx.box(
                    # Feature 1
                    feature_card(
                        icon="message-circle",
                        title="24/7 AI Assistance",
                        description="Get instant, accurate answers to your study questions anytime, anywhere. Never wait for help again.",
                        delay="0s",
                    ),
                    
                    # Feature 2
                    feature_card(
                        icon="book-open",
                        title="Personalized Learning",
                        description="Tailored explanations based on your education level and learning style. Learn at your own pace.",
                        delay="0.1s",
                    ),
                    
                    # Feature 3
                    feature_card(
                        icon="target",
                        title="Exam Preparation",
                        description="Practice with intelligent quizzes and get focused help for your exams. Boost your confidence.",
                        delay="0.2s",
                    ),
                    
                    # Feature 4
                    feature_card(
                        icon="zap",
                        title="Instant Feedback",
                        description="Receive immediate explanations and corrections. Learn from mistakes in real-time.",
                        delay="0.3s",
                    ),
                    
                    # Feature 5
                    feature_card(
                        icon="clock",
                        title="Save Time",
                        description="Get help faster than searching online. Spend more time learning, less time searching.",
                        delay="0.4s",
                    ),
                    
                    # Feature 6
                    feature_card(
                        icon="shield-check",
                        title="Safe & Private",
                        description="Your data is secure and private. Study with confidence knowing your information is protected.",
                        delay="0.5s",
                    ),
                    
                    display="grid",
                    grid_template_columns=["1fr", "1fr", "repeat(2, 1fr)", "repeat(3, 1fr)"],
                    gap="32px",
                    max_width="1400px",
                    margin="0 auto",
                ),
                
                margin_top="120px",
                padding_bottom="80px",
            ),
            
            # Benefits section
            rx.box(
                rx.box(
                    rx.box(
                        rx.heading(
                            "Study Smarter, Not Harder",
                            size="8",
                            color=COLORS["text_primary"],
                            margin_bottom="24px",
                        ),
                        rx.text(
                            "Join thousands of students who are achieving better grades with AI-powered study assistance.",
                            font_size="18px",
                            color=COLORS["text_secondary"],
                            line_height="1.7",
                            margin_bottom="32px",
                        ),
                        benefit_item("Understand complex topics faster", "lightbulb"),
                        benefit_item("Get step-by-step explanations", "list"),
                        benefit_item("Practice with unlimited questions", "repeat"),
                        benefit_item("Track your progress over time", "trending-up"),
                        
                        rx.button(
                            "Start Learning Now",
                            padding="16px 32px",
                            background=COLORS["primary_green"],
                            color="white",
                            border="none",
                            border_radius="12px",
                            cursor="pointer",
                            font_weight="600",
                            font_size="16px",
                            margin_top="32px",
                            transition="all 0.3s ease",
                            _hover={
                                "background": COLORS["dark_green"],
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 4px 20px rgba(16, 163, 127, 0.3)",
                            },
                            on_click=AuthState.toggle_auth_modal,
                        ),
                        
                        flex="1",
                    ),
                    
                    rx.box(
                        rx.box(
                            rx.icon(tag="graduation-cap", size=120, color=COLORS["primary_green"], opacity="0.1"),
                            position="absolute",
                            top="50%",
                            left="50%",
                            transform="translate(-50%, -50%)",
                        ),
                        rx.box(
                            rx.text(
                                "95%",
                                font_size="72px",
                                font_weight="700",
                                color=COLORS["primary_green"],
                                line_height="1",
                            ),
                            rx.text(
                                "Student Satisfaction",
                                font_size="18px",
                                color=COLORS["text_secondary"],
                                margin_top="12px",
                            ),
                            text_align="center",
                        ),
                        background="white",
                        padding="64px",
                        border_radius="20px",
                        box_shadow="0 10px 40px rgba(0, 0, 0, 0.08)",
                        position="relative",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        min_height="300px",
                        flex="1",
                    ),
                    
                    display="flex",
                    gap="64px",
                    max_width="1400px",
                    margin="0 auto",
                    align_items="center",
                    flex_wrap="wrap",
                ),
                
                background=COLORS["light_gray"],
                padding="80px 32px",
            ),
            
            # CTA section
            rx.box(
                rx.box(
                    rx.heading(
                        "Ready to Transform Your Learning?",
                        size="8",
                        color="white",
                        margin_bottom="24px",
                        text_align="center",
                    ),
                    rx.text(
                        "Join EduChat today and experience the future of personalized education.",
                        font_size="20px",
                        color="rgba(255, 255, 255, 0.9)",
                        margin_bottom="48px",
                        text_align="center",
                        max_width="600px",
                        margin_x="auto",
                    ),
                    rx.box(
                        rx.button(
                            "Get Started Free",
                            padding="18px 48px",
                            background="white",
                            color=COLORS["primary_green"],
                            border="none",
                            border_radius="12px",
                            cursor="pointer",
                            font_weight="700",
                            font_size="20px",
                            transition="all 0.3s ease",
                            box_shadow="0 4px 20px rgba(0, 0, 0, 0.2)",
                            _hover={
                                "transform": "translateY(-3px)",
                                "box_shadow": "0 8px 30px rgba(0, 0, 0, 0.3)",
                            },
                            on_click=AuthState.toggle_auth_modal,
                        ),
                        display="flex",
                        justify_content="center",
                    ),
                    max_width="1400px",
                    margin="0 auto",
                ),
                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                padding="80px 32px",
            ),
            
            padding="80px 32px 0 32px",
            min_height="100vh",
            background=f"linear-gradient(180deg, #ffffff 0%, {COLORS['light_gray']} 50%, #ffffff 100%)",
        ),
        
        width="100vw",
        min_height="100vh",
        overflow_x="hidden",
    )


def feature_card(icon: str, title: str, description: str, delay: str = "0s") -> rx.Component:
    """Feature card component with hover effects and animations."""
    
    return rx.box(
        rx.box(
            rx.box(
                rx.icon(
                    tag=icon,
                    size=40,
                    color="white",
                ),
                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                padding="16px",
                border_radius="12px",
                display="flex",
                align_items="center",
                justify_content="center",
                margin_bottom="24px",
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
        border_radius="16px",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.06)",
        border=f"1px solid {COLORS['border']}",
        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
        animation=f"fadeInUp 0.6s ease-out {delay} backwards",
        cursor="default",
        _hover={
            "box_shadow": "0 12px 32px rgba(0, 0, 0, 0.12)",
            "transform": "translateY(-8px)",
            "border_color": COLORS["primary_green"],
        },
    )


def benefit_item(text: str, icon: str) -> rx.Component:
    """Benefit list item with icon."""
    
    return rx.box(
        rx.box(
            rx.icon(
                tag=icon,
                size=20,
                color=COLORS["primary_green"],
            ),
            background=f"rgba(16, 163, 127, 0.1)",
            padding="8px",
            border_radius="8px",
            display="flex",
            align_items="center",
            justify_content="center",
            margin_right="16px",
        ),
        rx.text(
            text,
            font_size="16px",
            color=COLORS["text_primary"],
            font_weight="500",
        ),
        display="flex",
        align_items="center",
        margin_bottom="20px",
        transition="all 0.3s ease",
        _hover={
            "transform": "translateX(8px)",
        },
    )

