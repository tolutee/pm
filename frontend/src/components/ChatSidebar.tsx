"use client";

import { useEffect, useRef, useState } from "react";
import { fetchBoard, sendChat } from "@/lib/api";
import { type BoardData } from "@/lib/kanban";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type ChatSidebarProps = {
  onBoardUpdate: (board: BoardData) => void;
};

export const ChatSidebar = ({ onBoardUpdate }: ChatSidebarProps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView?.({ behavior: "smooth" });
  }, [messages, isLoading]);

  const send = async () => {
    const text = input.trim();
    if (!text || isLoading) return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setIsLoading(true);
    try {
      const response = await sendChat(text);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.message },
      ]);
      if (response.operations.length > 0) {
        const updatedBoard = await fetchBoard();
        onBoardUpdate(updatedBoard);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Something went wrong. Please try again." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="sticky top-12 flex h-[calc(100vh-5rem)] w-80 shrink-0 flex-col rounded-[32px] border border-[var(--stroke)] bg-white/80 shadow-[var(--shadow)] backdrop-blur">
      <div className="border-b border-[var(--stroke)] px-6 py-5">
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-[var(--gray-text)]">
          AI Assistant
        </p>
        <h2 className="mt-1 font-display text-lg font-semibold text-[var(--navy-dark)]">
          Chat with your board
        </h2>
      </div>

      <div className="flex flex-1 flex-col gap-3 overflow-y-auto px-4 py-4">
        {messages.length === 0 && (
          <p className="mt-4 text-center text-sm text-[var(--gray-text)]">
            Ask me to create, move, or update cards.
          </p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-[var(--secondary-purple)] text-white"
                  : "bg-[var(--surface)] text-[var(--navy-dark)]"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="rounded-2xl bg-[var(--surface)] px-4 py-2.5">
              <span className="text-sm text-[var(--gray-text)]">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="border-t border-[var(--stroke)] px-4 py-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder="Ask the AI..."
            disabled={isLoading}
            className="flex-1 rounded-xl border border-[var(--stroke)] bg-[var(--surface)] px-4 py-2.5 text-sm text-[var(--navy-dark)] placeholder:text-[var(--gray-text)] focus:outline-none focus:ring-2 focus:ring-[var(--primary-blue)] disabled:opacity-50"
          />
          <button
            onClick={send}
            disabled={isLoading || !input.trim()}
            className="rounded-xl bg-[var(--secondary-purple)] px-4 py-2.5 text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-40"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
