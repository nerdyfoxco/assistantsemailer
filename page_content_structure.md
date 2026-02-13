# Page Content Structure: Fyxer (Evolved UI)

Based on the "Deployment Readiness Contract" and "Vertical Slice" definitions.

## Screen 1: Connect Inbox (Landing / Onboarding)
**Goal**: User authorizes Gmail access.
- **Hero Section**:
    - **Headline**: "We draft replies. You approve."
    - **Subtext**: "Connect your personal Gmail to get AI-drafted replies for important emails."
- **Primary Action**:
    - **Button**: "Connect Gmail" (Triggers OAuth flow).
- **Compliance/Trust**:
    - **Disclaimer**: "We only read metadata and draft replies. No emails are sent without your explicit approval."

## Screen 2: Inbox (Decision Queue)
**Goal**: Show only what needs attention.
- **Layout**: List View (Clean, No Folders).
- **Item Component**:
    - **Sender Name**: (e.g., "John Doe").
    - **Subject Line**: (e.g., "Project Update?").
    - **Status Badge**: "Reply Needed" (Red/Accent Color).
    - **Timestamp**: (e.g., "2h ago").
- **Constraints**:
    - No "FYI" emails.
    - No "Newsletters".
    - Only "Actionable" items visible.

## Screen 3: Reply Workspace (Active Workflow)
**Goal**: Review, Edit, Send.
- **Layout**: Split View (Left/Right).
- **Left Panel (Context)**:
    - **Original Email Thread**: Full body content, scrollable.
- **Right Panel (Action)**:
    - **Draft Editor**: Pre-filled with AI-generated response.
    - **Controls**:
        - **Button**: "Send" (Primary).
        - **Button**: "Edit" (Secondary input field).
        - **Button**: "Discard/Close" (Destructive).
