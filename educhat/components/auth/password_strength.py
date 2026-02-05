"""
Password Strength Indicator Component
Shows real-time password strength feedback with visual indicators.
"""

import reflex as rx
from educhat.state.auth_state import AuthState
from educhat.styles.theme import ThemeTokens as T


class PasswordStrengthState(rx.State):
    """State for password strength calculation."""
    
    @rx.var
    def password_strength(self) -> dict:
        """Calculate password strength and return detailed feedback."""
        password = self.signup_password if hasattr(self, 'signup_password') else ""
        
        if not password:
            return {
                "strength": "none",
                "score": 0,
                "label": "",
                "color": T.text_secondary,
                "width": "0%",
                "requirements": {
                    "length": False,
                    "uppercase": False,
                    "lowercase": False,
                    "number": False,
                    "special": False,
                }
            }
        
        score = 0
        requirements = {
            "length": len(password) >= 8,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "number": any(c.isdigit() for c in password),
            "special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
        }
        
        # Calculate score
        if requirements["length"]:
            score += 1
        if requirements["uppercase"]:
            score += 1
        if requirements["lowercase"]:
            score += 1
        if requirements["number"]:
            score += 1
        if requirements["special"]:
            score += 1
        
        # Extra points for longer passwords
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        # Determine strength level
        if score <= 2:
            strength = "weak"
            label = "Zwak"
            color = T.error
            width = "33%"
        elif score <= 4:
            strength = "medium"
            label = "Gemiddeld"
            color = T.warning
            width = "66%"
        else:
            strength = "strong"
            label = "Sterk"
            color = T.success
            width = "100%"
        
        return {
            "strength": strength,
            "score": score,
            "label": label,
            "color": color,
            "width": width,
            "requirements": requirements,
        }


def password_strength_indicator() -> rx.Component:
    """Password strength meter with real-time feedback."""
    
    return rx.cond(
        # Only show when password field has content
        AuthState.signup_password != "",
        rx.box(
            # Strength bar
            rx.box(
                rx.box(
                    width=PasswordStrengthState.password_strength["width"],
                    height="100%",
                    background_color=PasswordStrengthState.password_strength["color"],
                    border_radius="4px",
                    transition="all 0.3s ease",
                ),
                width="100%",
                height="4px",
                background_color=f"{T.border}50",
                border_radius="4px",
                overflow="hidden",
                margin_bottom="8px",
            ),
            
            # Strength label
            rx.box(
                rx.text(
                    "Wachtwoordsterkte: ",
                    font_size="13px",
                    color=T.text_secondary,
                    display="inline",
                ),
                rx.text(
                    PasswordStrengthState.password_strength["label"],
                    font_size="13px",
                    font_weight="600",
                    color=PasswordStrengthState.password_strength["color"],
                    display="inline",
                ),
                margin_bottom="12px",
            ),
            
            # Requirements checklist
            rx.box(
                # Length requirement
                rx.box(
                    rx.icon(
                        rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["length"],
                            "check-circle",
                            "circle"
                        ),
                        size=14,
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["length"],
                            T.success,
                            T.text_secondary
                        ),
                    ),
                    rx.text(
                        "Minimaal 8 tekens",
                        font_size="12px",
                        margin_left="6px",
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["length"],
                            T.text_primary,
                            T.text_secondary
                        ),
                    ),
                    display="flex",
                    align_items="center",
                ),
                
                # Uppercase requirement
                rx.box(
                    rx.icon(
                        rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["uppercase"],
                            "check-circle",
                            "circle"
                        ),
                        size=14,
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["uppercase"],
                            T.success,
                            T.text_secondary
                        ),
                    ),
                    rx.text(
                        "Hoofdletter (A-Z)",
                        font_size="12px",
                        margin_left="6px",
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["uppercase"],
                            T.text_primary,
                            T.text_secondary
                        ),
                    ),
                    display="flex",
                    align_items="center",
                ),
                
                # Lowercase requirement
                rx.box(
                    rx.icon(
                        rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["lowercase"],
                            "check-circle",
                            "circle"
                        ),
                        size=14,
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["lowercase"],
                            T.success,
                            T.text_secondary
                        ),
                    ),
                    rx.text(
                        "Kleine letter (a-z)",
                        font_size="12px",
                        margin_left="6px",
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["lowercase"],
                            T.text_primary,
                            T.text_secondary
                        ),
                    ),
                    display="flex",
                    align_items="center",
                ),
                
                # Number requirement
                rx.box(
                    rx.icon(
                        rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["number"],
                            "check-circle",
                            "circle"
                        ),
                        size=14,
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["number"],
                            T.success,
                            T.text_secondary
                        ),
                    ),
                    rx.text(
                        "Cijfer (0-9)",
                        font_size="12px",
                        margin_left="6px",
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["number"],
                            T.text_primary,
                            T.text_secondary
                        ),
                    ),
                    display="flex",
                    align_items="center",
                ),
                
                # Special character requirement
                rx.box(
                    rx.icon(
                        rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["special"],
                            "check-circle",
                            "circle"
                        ),
                        size=14,
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["special"],
                            T.success,
                            T.text_secondary
                        ),
                    ),
                    rx.text(
                        "Speciaal teken (!@#$...)",
                        font_size="12px",
                        margin_left="6px",
                        color=rx.cond(
                            PasswordStrengthState.password_strength["requirements"]["special"],
                            T.text_primary,
                            T.text_secondary
                        ),
                    ),
                    display="flex",
                    align_items="center",
                ),
                
                display="grid",
                grid_template_columns="1fr 1fr",
                gap="8px",
            ),
            
            padding="12px",
            background_color=f"{T.bg_secondary}50",
            border_radius="8px",
            margin_top="8px",
            animation="fadeIn 0.3s ease-out",
        ),
    )
