"use client";

import { useState, type FormEvent } from "react";
import { validateCredentials } from "@/lib/auth";

type LoginPageProps = {
  onLogin: () => void;
};

export const LoginPage = ({ onLogin }: LoginPageProps) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (validateCredentials(username, password)) {
      setError("");
      onLogin();
      return;
    }

    setError("Invalid credentials. Use user / password.");
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-[radial-gradient(circle,_rgba(32,157,215,0.12)_0%,_transparent_55%)] p-6">
      <div className="w-full max-w-md rounded-[32px] border border-[var(--stroke)] bg-white/95 p-8 shadow-[var(--shadow)]">
        <div className="mb-8">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[var(--gray-text)]">
            Welcome back
          </p>
          <h1 className="mt-3 text-3xl font-semibold text-[var(--navy-dark)]">
            Sign in to Kanban Studio
          </h1>
          <p className="mt-3 text-sm leading-6 text-[var(--gray-text)]">
            Use the hardcoded credentials to access the board.
          </p>
        </div>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <label className="block text-sm font-semibold text-[var(--navy-dark)]">
            Username
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-[var(--stroke)] bg-white px-4 py-3 text-sm outline-none transition focus:border-[var(--primary-blue)]"
              autoComplete="username"
              aria-label="Username"
            />
          </label>

          <label className="block text-sm font-semibold text-[var(--navy-dark)]">
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-[var(--stroke)] bg-white px-4 py-3 text-sm outline-none transition focus:border-[var(--primary-blue)]"
              autoComplete="current-password"
              aria-label="Password"
            />
          </label>

          {error ? (
            <p className="rounded-2xl bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </p>
          ) : null}

          <button
            type="submit"
            className="w-full rounded-full bg-[var(--secondary-purple)] px-5 py-3 text-sm font-semibold uppercase tracking-[0.18em] text-white transition hover:brightness-110"
          >
            Sign in
          </button>
        </form>
      </div>
    </main>
  );
};
