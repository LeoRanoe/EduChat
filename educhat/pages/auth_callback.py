"""
OAuth Callback Page
Handles OAuth provider callbacks (Google, etc.)
"""

import reflex as rx
from educhat.state.auth_state import AuthState


class CallbackState(AuthState):
    """State for handling OAuth callback."""
    
    # Store code from URL
    oauth_code: str = ""
    oauth_error: str = ""
    
    def on_load(self):
        """Extract code from URL on page load."""
        print("[CALLBACK] Page loaded, extracting URL params...")
        
        # Use the deprecated but working router.page.params
        try:
            params = self.router.page.params
            print(f"[CALLBACK] URL params: {params}")
            
            self.oauth_code = params.get("code", "")
            self.oauth_error = params.get("error", "")
            
            print(f"[CALLBACK] Code: {self.oauth_code[:20] if self.oauth_code else 'None'}...")
            print(f"[CALLBACK] Error: {self.oauth_error if self.oauth_error else 'None'}")
        except Exception as e:
            print(f"[CALLBACK] Error extracting params: {e}")
            self.oauth_error = "param_error"
    
    def process_callback(self):
        """Process the OAuth callback after params are extracted."""
        print("[CALLBACK] Processing OAuth callback...")
        
        if self.oauth_error:
            print(f"[CALLBACK] OAuth error: {self.oauth_error}")
            self.auth_error = "Google authenticatie geannuleerd of mislukt"
            return rx.redirect("/")
        
        if self.oauth_code:
            print(f"[CALLBACK] Processing code: {self.oauth_code[:20]}...")
            # Call parent class method to handle OAuth - it yields events
            return self.handle_oauth_callback(self.oauth_code)
        else:
            print("[CALLBACK] No code found")
            self.auth_error = "Geen authenticatie code ontvangen"
            return rx.redirect("/")


def auth_callback() -> rx.Component:
    """OAuth callback page that processes the OAuth code."""
    return rx.box(
        rx.box(
            rx.spinner(size="3"),
            rx.text(
                "Authenticeren...",
                font_size="18px",
                font_weight="500",
                margin_top="20px",
            ),
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="center",
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        min_height="100vh",
        class_name="solid-panel",
        on_mount=[CallbackState.on_load, CallbackState.process_callback],
    )
