import { render, screen, within, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi, describe, it, expect, beforeEach } from "vitest";
import { KanbanBoard } from "@/components/KanbanBoard";
import * as api from "@/lib/api";

vi.mock("@/lib/api", () => ({
  fetchBoard: vi.fn(),
  updateBoard: vi.fn(),
  deleteBoard: vi.fn(),
  APIError: Error,
}));

const mockBoard = {
  columns: [
    { id: "col-backlog", title: "Backlog", cardIds: ["card-1", "card-2"] },
    { id: "col-discovery", title: "Discovery", cardIds: ["card-3"] },
    { id: "col-progress", title: "In Progress", cardIds: ["card-4", "card-5"] },
    { id: "col-review", title: "Review", cardIds: ["card-6"] },
    { id: "col-done", title: "Done", cardIds: ["card-7", "card-8"] },
  ],
  cards: {
    "card-1": { id: "card-1", title: "Card 1", details: "Details 1" },
    "card-2": { id: "card-2", title: "Card 2", details: "Details 2" },
    "card-3": { id: "card-3", title: "Card 3", details: "Details 3" },
    "card-4": { id: "card-4", title: "Card 4", details: "Details 4" },
    "card-5": { id: "card-5", title: "Card 5", details: "Details 5" },
    "card-6": { id: "card-6", title: "Card 6", details: "Details 6" },
    "card-7": { id: "card-7", title: "Card 7", details: "Details 7" },
    "card-8": { id: "card-8", title: "Card 8", details: "Details 8" },
  },
};

const getFirstColumn = () => screen.getAllByTestId(/column-/i)[0];

describe("KanbanBoard", () => {
  beforeEach(() => {
    vi.mocked(api.fetchBoard).mockResolvedValue(mockBoard);
    vi.mocked(api.updateBoard).mockResolvedValue(mockBoard);
  });

  it("renders five columns", async () => {
    render(<KanbanBoard />);
    await waitFor(() => {
      expect(screen.getAllByTestId(/column-/i)).toHaveLength(5);
    });
  });

  it("renames a column", async () => {
    render(<KanbanBoard />);
    await waitFor(() => {
      expect(screen.getAllByTestId(/column-/i)).toHaveLength(5);
    });

    const column = getFirstColumn();
    const input = within(column).getByLabelText("Column title");
    await userEvent.clear(input);
    await userEvent.type(input, "New Name");

    await waitFor(() => {
      expect(vi.mocked(api.updateBoard)).toHaveBeenCalled();
    });
  });

  it("adds and removes a card", async () => {
    render(<KanbanBoard />);
    await waitFor(() => {
      expect(screen.getAllByTestId(/column-/i)).toHaveLength(5);
    });

    const column = getFirstColumn();
    const addButton = within(column).getByRole("button", {
      name: /add a card/i,
    });
    await userEvent.click(addButton);

    const titleInput = within(column).getByPlaceholderText(/card title/i);
    await userEvent.type(titleInput, "New card");
    const detailsInput = within(column).getByPlaceholderText(/details/i);
    await userEvent.type(detailsInput, "Notes");

    await userEvent.click(within(column).getByRole("button", { name: /add card/i }));

    await waitFor(() => {
      expect(within(column).getByText("New card")).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(vi.mocked(api.updateBoard)).toHaveBeenCalled();
    });
  });
});
