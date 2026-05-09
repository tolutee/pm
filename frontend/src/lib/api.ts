import { type BoardData } from "@/lib/kanban";

const API_BASE = "/api";

export class APIError extends Error {
  constructor(
    public status: number,
    public message: string
  ) {
    super(message);
    this.name = "APIError";
  }
}

function getAuthHeaders(): Record<string, string> {
  const username = typeof window !== "undefined" ? localStorage.getItem("username") : null;
  const password = typeof window !== "undefined" ? localStorage.getItem("password") : null;
  const headers: Record<string, string> = {};
  if (username) headers["X-Username"] = username;
  if (password) headers["X-Password"] = password;
  return headers;
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const headers = { ...getAuthHeaders(), ...options.headers };
  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new APIError(response.status, data.detail || `HTTP ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export async function fetchBoard(): Promise<BoardData> {
  return request<BoardData>("/board");
}

export async function updateBoard(board: BoardData): Promise<BoardData> {
  return request<BoardData>("/board", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(board),
  });
}

export async function deleteBoard(): Promise<{ status: string }> {
  return request<{ status: string }>("/board", {
    method: "DELETE",
  });
}

export async function getMe(): Promise<{ username: string }> {
  return request<{ username: string }>("/me");
}

export type ChatOperation = {
  operation: string;
  cardId?: string;
  title?: string;
  details?: string;
  columnId?: string;
};

export type ChatResponse = {
  message: string;
  operations: ChatOperation[];
  status: string;
};

export async function sendChat(message: string): Promise<ChatResponse> {
  return request<ChatResponse>("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
}
