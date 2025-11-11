# Responsive Design Implementation

## Overview
EduChat now features a fully responsive design that adapts to mobile, tablet, and desktop screen sizes using CSS media queries.

## Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1023px  
- **Desktop**: ≥ 1024px

## Key Features

### Mobile (<768px)
- **Sidebar**: Off-screen by default, slides in from left when hamburger menu clicked
- **Navigation**: Hamburger menu button in top header
- **Layout**: Single column, full width
- **Typography**: Slightly smaller fonts (0.875rem base)
- **Spacing**: Reduced padding (1rem)
- **Messages**: Max width 90% for better readability

### Tablet (768px-1023px)
- **Sidebar**: Off-screen by default, can be toggled
- **Navigation**: Hamburger menu available
- **Layout**: Single column with more breathing room
- **Typography**: Standard fonts
- **Spacing**: Medium padding (1.25rem)

### Desktop (≥1024px)
- **Sidebar**: Always visible, fixed 280px width
- **Navigation**: No hamburger menu (sidebar always visible)
- **Layout**: Two column (sidebar + chat)
- **Typography**: Full-size fonts (1rem-1.125rem)
- **Spacing**: Maximum padding (1.5rem-2rem)
- **Max Width**: Content capped at 1200px for readability

## Components Updated

### 1. Main Layout (`pages/index.py`)
- Added `mobile_header` component with hamburger menu
- Added `sidebar_overlay` for mobile backdrop
- Sidebar controlled by `AppState.sidebar_open` state
- Mobile header hidden on desktop using media queries

### 2. Sidebar (`components/chat/sidebar.py`)
- Fixed position on mobile (slides in/out)
- Relative position on desktop (always visible)
- Controlled by `is_open` prop for mobile toggle
- Box shadow on mobile when open

### 3. Chat Container (`components/chat/chat_container.py`)
- Zero margin on mobile (full width)
- 280px left margin on desktop (accounts for sidebar)
- Max width 1200px on desktop

### 4. Message Bubbles (`components/chat/message_bubble.py`)
- Smaller fonts on mobile (0.875rem)
- Reduced padding on mobile (0.75rem 1rem)
- Max width 90% on mobile vs 600px on desktop
- Action icons wrap on mobile

### 5. Chat Input (`components/chat/chat_input.py`)
- Reduced padding on mobile (1rem)
- Smaller font on mobile (0.875rem)
- Maintains full functionality across all sizes

### 6. Onboarding Page (`pages/onboarding.py`)
- Single column on mobile (quiz only)
- Split view on desktop (quiz + welcome panel)
- Welcome panel hidden on mobile/tablet
- Full width quiz panel on mobile

### 7. Mobile Navigation (`components/shared/mobile_nav.py`)
- `hamburger_button`: Animated 3-line to X icon
- `mobile_header`: Top bar with logo and menu button
- `sidebar_overlay`: Dark backdrop when sidebar open

## State Management

### AppState (`state/app_state.py`)
Added mobile UI state:
```python
sidebar_open: bool = False  # Mobile sidebar toggle state

def toggle_sidebar(self):
    """Toggle sidebar visibility (for mobile)."""
    self.sidebar_open = not self.sidebar_open

def close_sidebar(self):
    """Close sidebar (for mobile)."""
    self.sidebar_open = False
```

## Utility Module

### `utils/responsive.py`
Contains helper functions and breakpoint constants:
- `BREAKPOINTS` dictionary
- `mobile_only()`, `tablet_up()`, `desktop_only()` display helpers
- `responsive_width()`, `responsive_padding()`, `responsive_font_size()` helpers
- `sidebar_responsive()`, `chat_responsive()` layout utilities

## CSS Media Queries Pattern

Since Reflex doesn't support responsive arrays directly, we use CSS media queries:

```python
rx.box(
    content,
    width="100%",  # Mobile default
    **{
        "@media (min-width: 1024px)": {  # Desktop override
            "width": "50%",
        }
    }
)
```

## Testing Recommendations

1. **Chrome DevTools**: Use device toolbar to test breakpoints
2. **Mobile Devices**: Test on actual iOS/Android devices
3. **Tablet Devices**: Test on iPad/Android tablets
4. **Browser Resize**: Manually resize browser window to verify transitions

## Known Limitations

1. Reflex's responsive prop arrays (`[mobile, tablet, desktop]`) don't work with all prop types
2. Media queries must be passed as `**kwargs` dict
3. Some Reflex components may not support all CSS properties in media queries

## Future Enhancements

1. Touch gestures for sidebar (swipe to open/close)
2. Responsive data tables
3. Mobile-optimized forms
4. Progressive Web App (PWA) features
5. Adaptive images based on screen size
