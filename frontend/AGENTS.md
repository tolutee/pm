# Frontend Code Description

## Overview
The frontend is a Next.js 16 application built with React 19, TypeScript, and Tailwind CSS. It implements a Kanban board with drag-and-drop functionality using @dnd-kit. The app now integrates with a FastAPI backend for persistent data storage and includes user authentication.

## Key Components

### AuthGate (`src/components/AuthGate.tsx`)
- Top-level authentication component
- Manages login/logout state
- Redirects between LoginPage and KanbanBoard

### LoginPage (`src/components/LoginPage.tsx`)
- User login form with hardcoded credentials
- Validates "user"/"password"
- Stores authentication in localStorage

### KanbanBoard (`src/components/KanbanBoard.tsx`)
- Main component that manages the entire board state
- Loads data from backend API on mount
- Persists changes to backend
- Uses @dnd-kit for drag and drop operations
- Handles column renaming, card addition, deletion, and movement
- Renders columns and drag overlay

### KanbanColumn (`src/components/KanbanColumn.tsx`)
- Represents a single column in the Kanban board
- Droppable area for cards
- Shows column title (editable), card count, and contains cards
- Includes NewCardForm for adding cards

### KanbanCard (`src/components/KanbanCard.tsx`)
- Individual card component with title and details
- Sortable using @dnd-kit
- Has delete button

### KanbanCardPreview (`src/components/KanbanCardPreview.tsx`)
- Drag overlay preview for cards during drag operations

### NewCardForm (`src/components/NewCardForm.tsx`)
- Form for adding new cards to a column
- Toggles between collapsed and expanded state

## API Integration (`src/lib/api.ts`)
- REST API client for backend communication
- Functions: fetchBoard, updateBoard, deleteBoard, getMe
- Handles authentication headers (X-Username, X-Password)
- Error handling with custom APIError class

## Authentication (`src/lib/auth.ts`)
- Client-side authentication state management
- Uses localStorage for persistence
- Validates hardcoded credentials
- Functions: isAuthenticated, setAuthenticated, clearAuthentication

## Data Structure (`src/lib/kanban.ts`)
- Defines TypeScript types: Card, Column, BoardData
- Provides initial sample data
- Includes utility functions: createId, moveCard

## Testing
- Unit tests with Vitest in `src/lib/kanban.test.ts`, `src/lib/auth.test.ts`, `src/lib/api.test.ts`, and `src/components/KanbanBoard.test.tsx`
- E2E tests with Playwright in `tests/kanban.spec.ts`
- Test setup in `src/test/setup.ts`

## Build Configuration
- Static export enabled (`output: 'export'`)
- Served by FastAPI backend
- No client-side routing (all routes served from /)

## Styling
- Uses Tailwind CSS with custom CSS variables for colors
- Responsive design with backdrop blur effects
- Custom shadows and gradients

## Build and Scripts
- `npm run build`: Production static export
- `npm run test`: Run unit tests
- `npm run test:e2e`: Run e2e tests
- `npm run test:all`: Run all tests (unit + e2e)