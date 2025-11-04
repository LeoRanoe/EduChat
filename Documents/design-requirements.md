# 🎨 EduChat – Design Requirements Document (DRD)

**Project:** EduChat  
**Version:** 1.0  
**Date:** 4 november 2025  
**Purpose:** Define visual design specifications and UI/UX guidelines based on approved mockups

---

## 📐 Design System Overview

### Color Palette
- **Primary Green:** `#228B22` (Forest Green)
- **Primary Background:** `#FFFFFF` (White)
- **Secondary Background:** `#F5F5F5` (Light Gray)
- **Chat Bubble (User):** `#D4F1D4` (Light Green)
- **Chat Bubble (Bot):** `#FFFFFF` with subtle border
- **Text Primary:** `#2D2D2D` (Dark Gray)
- **Text Secondary:** `#666666` (Medium Gray)
- **Button Primary:** `#228B22` (Green)
- **Button Hover:** `#1A6B1A` (Darker Green)
- **Border Color:** `#E0E0E0` (Light Gray)

### Typography
- **Heading Font:** Bold, Sans-serif
- **Body Font:** Regular, Sans-serif (Recommended: Inter, Roboto, or system fonts)
- **Font Sizes:**
  - H1 (Welcome): 48px - 64px (bold)
  - H2 (Section titles): 24px - 32px (semi-bold)
  - Body text: 16px (regular)
  - Small text: 14px (regular)
  - Button text: 16px (medium)

### Spacing & Layout
- **Container Max Width:** 1200px
- **Sidebar Width:** 220px
- **Content Padding:** 24px - 32px
- **Component Spacing:** 16px - 24px
- **Border Radius:**
  - Buttons: 24px (rounded pill)
  - Input fields: 8px
  - Chat bubbles: 12px
  - Cards: 8px

---

## 🖼️ Screen Specifications

### 1. **Onboarding Screen (Quiz Interface)**

**Layout:**
- Split screen design: 50% left (quiz) / 50% right (info panel)
- Left panel: White background with logo, quiz questions, navigation
- Right panel: Green background (#228B22) with welcome message and description

**Components:**

#### Logo
- Position: Top-left corner
- Icon: Graduation cap with chat bubble
- Size: 40px x 40px

#### Quiz Content
- **Title:** "Vertel ons een beetje over jouw"
- **Subtitle:** Gray text (Lorem ipsum description)
- **Progress Bar:** Horizontal line indicator
- **Question Types:**
  - Multi-select buttons (white background, border on hover/select)
  - Dropdown selects (white with border)
  - Free text area (border on focus)

#### Button Styling (Quiz Buttons)
- Background: White
- Border: 1px solid #E0E0E0
- Padding: 8px 16px
- Border-radius: 24px
- Hover: Border color changes to green
- Selected: Background #228B22, text white

#### Navigation Buttons
- **"Overslaan"** (Skip): Outlined button, green border
- **"Terug"** (Back): Outlined button with left arrow
- **"Volgende"** (Next): Primary button with right arrow, green background

#### Right Panel (Welcome Panel)
- **Heading:** "Welkom bij EduChat" (White text, bold)
- **Description:** White text explaining the purpose
- **Illustration:** Optional (second screen shows conversation illustration)

---

### 2. **Chat Interface (Main Application)**

**Layout:**
- Sidebar (left): 220px width, light gray background
- Main chat area (right): Flexible width
- Fixed bottom: Input area

**Sidebar Components:**

#### Top Section
- Logo: Same as onboarding (40px)
- Spacing: 16px padding

#### Action Buttons
- "🖊️ Nieuw gesprek" (New Conversation)
- "🔍 Gesprek opzoeken" (Search Conversation)
- Style: Full-width, left-aligned, icon + text
- Background: Transparent, hover: light green

#### Conversation List
- Title: "Gesprekken -" (with dropdown indicator)
- List items:
  - Text preview (truncated)
  - Three-dot menu (right)
  - Active state: Light green background
  - Hover: Light gray background

#### User Profile (Bottom)
- Avatar circle (40px)
- Name: "John Doe"
- Email: "johndoe@email.com"
- Settings icon (gear)

**Chat Area:**

#### Header
- Title: "Welkom bij EduChat"
- Centered, large bold text
- Logo above title

#### Input Section
- **Container:** White rounded box with border
- **Input field:** 
  - Placeholder: "Vraag mij van alles!"
  - Border-radius: 8px
  - Min-height: 48px
  - Padding: 12px 16px
- **Buttons:**
  - "📎 Prompts" button (left): Outlined, icon + text
  - Send button (right): Circular, green background, white arrow icon
- **Footer text:** Small gray text with attribution

#### Message Bubbles

**User Messages:**
- Background: #D4F1D4 (light green)
- Position: Right-aligned
- Max-width: 70%
- Border-radius: 12px
- Padding: 12px 16px
- Word count indicator (top-right): "X/Z"

**Bot Messages:**
- Background: White
- Border: 1px solid #E0E0E0
- Position: Left-aligned
- Max-width: 80%
- Border-radius: 12px
- Padding: 16px
- **Bot identifier:** "MINOV staat voor..." (bold)
- **Action icons (bottom):**
  - Copy, Thumbs up, Thumbs down, Bookmark, Refresh, More options
  - Size: 20px, gray color, hover: green

#### Top Action Bar (Chat View)
- Icons: Share, Delete, Settings
- Position: Top-right
- Size: 24px
- Color: Green

---

## 📱 Responsive Design

### Mobile (<768px)
- Single column layout
- Sidebar becomes hamburger menu
- Full-width chat interface
- Stacked onboarding screens
- Font sizes reduced by 10-15%

### Tablet (768px - 1024px)
- Collapsible sidebar
- Adjusted split ratios (60/40 for chat)
- Maintain core layout structure

### Desktop (>1024px)
- Full layout as specified
- Maximum container width: 1200px
- Centered on larger screens

---

## 🎯 Component Specifications

### Buttons

#### Primary Button
```
Background: #228B22
Color: #FFFFFF
Padding: 12px 24px
Border-radius: 24px
Font-weight: 500
Hover: Background #1A6B1A
```

#### Secondary Button
```
Background: Transparent
Color: #228B22
Border: 1px solid #228B22
Padding: 12px 24px
Border-radius: 24px
Hover: Background #F0F9F0
```

#### Icon Button
```
Background: Transparent
Padding: 8px
Border-radius: 50%
Hover: Background #F5F5F5
```

### Input Fields
```
Background: #FFFFFF
Border: 1px solid #E0E0E0
Border-radius: 8px
Padding: 12px 16px
Font-size: 16px
Focus: Border-color #228B22, outline none
```

### Dropdowns
```
Background: #FFFFFF
Border: 1px solid #E0E0E0
Border-radius: 8px
Padding: 12px 16px
Arrow icon: Right-aligned
```

---

## ♿ Accessibility Requirements

- **Color Contrast:** Minimum WCAG AA compliance (4.5:1 for text)
- **Focus Indicators:** Visible focus states for keyboard navigation
- **ARIA Labels:** All interactive elements labeled
- **Alt Text:** All images and icons have descriptive alt text
- **Keyboard Navigation:** Full functionality without mouse
- **Screen Reader Support:** Semantic HTML structure

---

## 🎨 Illustration Style

- **Style:** Modern, flat design with simple shapes
- **Color:** Primarily green (#228B22) with accent colors (blue, yellow, beige)
- **Usage:** Welcome screens, empty states, error messages
- **Tone:** Friendly, approachable, educational

---

## 🔄 Animation & Interaction

### Transitions
- **Default duration:** 200ms
- **Easing:** ease-in-out
- **Hover states:** Scale or color change
- **Page transitions:** Fade (300ms)

### Loading States
- **Spinner:** Green circular spinner
- **Skeleton screens:** Gray placeholders for content
- **Message typing indicator:** Three animated dots

### Micro-interactions
- Button press: Slight scale down
- Message send: Slide up animation
- New message: Fade in from bottom
- Like/dislike: Scale bounce effect

---

## 📏 Grid System

- **Columns:** 12-column grid
- **Gutter:** 24px
- **Breakpoints:**
  - Mobile: 0-767px
  - Tablet: 768px-1023px
  - Desktop: 1024px+
  - Large: 1440px+

---

## ✅ Design Checklist

### Visual Consistency
- [ ] All colors match defined palette
- [ ] Typography is consistent across screens
- [ ] Spacing follows 8px grid system
- [ ] Border radius is uniform by component type

### User Experience
- [ ] Clear visual hierarchy
- [ ] Intuitive navigation flow
- [ ] Feedback for all user actions
- [ ] Error states are helpful and friendly

### Accessibility
- [ ] Sufficient color contrast
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Focus states are visible

### Responsive Design
- [ ] Mobile layout tested
- [ ] Tablet layout tested
- [ ] Desktop layout tested
- [ ] Touch targets are 44px minimum

---

## 📦 Assets Required

### Icons
- Logo (graduation cap + chat bubble)
- Navigation icons (new chat, search, settings)
- Action icons (send, like, dislike, copy, bookmark, share, delete)
- Arrow icons (back, next, send)

### Illustrations
- Welcome screen illustration (person with chat bot)
- Empty state illustrations
- Error state illustrations

### Fonts
- Primary font family (Inter or Roboto recommended)
- Font weights: Regular (400), Medium (500), Semi-bold (600), Bold (700)

---

## 🎯 Brand Guidelines

### Voice & Tone
- **Friendly:** Approachable and warm
- **Professional:** Reliable and trustworthy
- **Helpful:** Supportive and encouraging
- **Surinamese:** Culturally relevant and localized

### Messaging
- Use clear, simple Dutch
- Avoid jargon
- Be encouraging about education
- Respect Surinamese cultural context

---

**End of Design Requirements Document**
