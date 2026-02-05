"""
OAuth Callback Page
Handles OAuth provider callbacks (Google, etc.)
"""

import reflex as rx
from educhat.state.auth_state import AuthState


class CallbackState(AuthState):
    """State for handling OAuth callback."""
    
    async def process_oauth_callback(self):
        """Extract OAuth code from URL and process callback in a single step."""
        print("[CALLBACK] Processing OAuth callback...")
        
        try:
            # Extract query parameters from URL using modern router API
            # Get the full query string and parse it
            query_dict = self.router.page.params
            
            # Handle OAuth error (user cancelled or provider error)
            if "error" in query_dict:
                error_msg = query_dict.get("error", "unknown")
                print(f"[CALLBACK] OAuth error: {error_msg}")
                self.auth_error = "Google authenticatie geannuleerd of mislukt"
                yield rx.redirect("/")
                return
            
            # Extract authorization code
            code = query_dict.get("code", "")
            
            if not code:
                print("[CALLBACK] No authorization code found in URL")
                self.auth_error = "Geen authenticatie code ontvangen"
                yield rx.redirect("/")
                return
            
            print(f"[CALLBACK] Found code: {code[:20]}...")
            
            # Process the OAuth callback using parent class method
            # handle_oauth_callback is an async generator, so we need to iterate over it
            async for event in self.handle_oauth_callback(code):
                yield event
            
        except Exception as e:
            print(f"[CALLBACK] Error processing callback: {e}")
            import traceback
            traceback.print_exc()
            self.auth_error = "Er is een fout opgetreden tijdens authenticatie"
            yield rx.redirect("/")


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
        on_mount=CallbackState.process_oauth_callback,
    )
