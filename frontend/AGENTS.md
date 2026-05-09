# Frontend Code Description

## Overview
The frontend is a Next.js 16 application built with React 19, TypeScript, and Tailwind CSS. It implements a Kanban board with drag-and-drop functionality using @dnd-kit. The app is currently a pure frontend demo without backend integration.

## Key Components

### KanbanBoard (`src/components/KanbanBoard.tsx`)
- Main component that manages the entire board state
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

## Data Structure (`src/lib/kanban.ts`)
- Defines TypeScript types: Card, Column, BoardData
- Provides initial sample data
- Includes utility functions: createId, moveCard

## Testing
- Unit tests with Vitest in `src/lib/kanban.test.ts` and `src/components/KanbanBoard.test.tsx`
- E2E tests with Playwright in `tests/kanban.spec.ts`
- Test setup in `src/test/setup.ts`

## Styling
- Uses Tailwind CSS with custom CSS variables for colors
- Responsive design with backdrop blur effects
- Custom shadows and gradients

## Build and Scripts
- `npm run dev`: Development server
- `npm run build`: Production build
- `npm run test:all`: Run all tests (unit + e2e)
- Uses Vite for testing and building