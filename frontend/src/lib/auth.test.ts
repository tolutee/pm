import { beforeEach, describe, expect, it } from "vitest";
import {
  clearAuthentication,
  isAuthenticated,
  setAuthenticated,
  validateCredentials,
} from "@/lib/auth";

describe("auth utilities", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("validates hardcoded credentials", () => {
    expect(validateCredentials("user", "password")).toBe(true);
    expect(validateCredentials("user", "wrong")).toBe(false);
    expect(validateCredentials("admin", "password")).toBe(false);
  });

  it("stores and reads authentication state", () => {
    expect(isAuthenticated()).toBe(false);
    setAuthenticated("user", "password");
    expect(isAuthenticated()).toBe(true);
    clearAuthentication();
    expect(isAuthenticated()).toBe(false);
  });
});
