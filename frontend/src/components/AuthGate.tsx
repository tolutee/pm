"use client";

import { useEffect, useState } from "react";
import { KanbanBoard } from "@/components/KanbanBoard";
import { LoginPage } from "@/components/LoginPage";
import {
  clearAuthentication,
  isAuthenticated,
  setAuthenticated,
} from "@/lib/auth";

export const AuthGate = () => {
  const [authenticated, setAuthenticatedState] = useState<boolean | null>(null);

  useEffect(() => {
    setAuthenticatedState(isAuthenticated());
  }, []);

  const handleLogin = (username: string, password: string) => {
    setAuthenticated(username, password);
    setAuthenticatedState(true);
  };

  const handleLogout = () => {
    clearAuthentication();
    setAuthenticatedState(false);
  };

  if (authenticated === null) {
    return null;
  }

  return authenticated ? (
    <KanbanBoard onLogout={handleLogout} />
  ) : (
    <LoginPage onLogin={handleLogin} />
  );
};
