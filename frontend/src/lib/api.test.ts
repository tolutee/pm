import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { fetchBoard, updateBoard, deleteBoard, APIError } from "@/lib/api";

describe("API client", () => {
  beforeEach(() => {
    localStorage.setItem("username", "user");
    localStorage.setItem("password", "password");
    global.fetch = vi.fn();
  });

  afterEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  it("fetchBoard sends correct headers", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ columns: [], cards: {} }),
    });

    await fetchBoard();

    expect(global.fetch).toHaveBeenCalledWith(
      "/api/board",
      expect.objectContaining({
        headers: expect.objectContaining({
          "X-Username": "user",
          "X-Password": "password",
        }),
      })
    );
  });

  it("updateBoard sends PUT with board data", async () => {
    const board = { columns: [], cards: {} };
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => board,
    });

    await updateBoard(board);

    expect(global.fetch).toHaveBeenCalledWith(
      "/api/board",
      expect.objectContaining({
        method: "PUT",
        headers: expect.objectContaining({
          "Content-Type": "application/json",
        }),
        body: JSON.stringify(board),
      })
    );
  });

  it("throws APIError on failed response", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 401,
      json: async () => ({ detail: "Invalid credentials" }),
    });

    await expect(fetchBoard()).rejects.toThrow(APIError);
  });

  it("deleteBoard sends DELETE request", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ status: "deleted" }),
    });

    await deleteBoard();

    expect(global.fetch).toHaveBeenCalledWith(
      "/api/board",
      expect.objectContaining({
        method: "DELETE",
      })
    );
  });
});
