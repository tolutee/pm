const AUTH_KEY = "pm-mvp-auth";

export const validateCredentials = (username: string, password: string) => {
  return username === "user" && password === "password";
};

export const isAuthenticated = () => {
  if (typeof window === "undefined") {
    return false;
  }

  return window.localStorage.getItem(AUTH_KEY) === "true";
};

export const setAuthenticated = (value: boolean) => {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(AUTH_KEY, value ? "true" : "false");
};

export const clearAuthentication = () => {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.removeItem(AUTH_KEY);
};
