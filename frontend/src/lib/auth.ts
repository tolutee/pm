const AUTH_KEY = "pm-mvp-auth";
const USERNAME_KEY = "username";
const PASSWORD_KEY = "password";

export const validateCredentials = (username: string, password: string) => {
  return username === "user" && password === "password";
};

export const isAuthenticated = () => {
  if (typeof window === "undefined") {
    return false;
  }

  return window.localStorage.getItem(AUTH_KEY) === "true";
};

export const setAuthenticated = (username: string, password: string) => {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(AUTH_KEY, "true");
  window.localStorage.setItem(USERNAME_KEY, username);
  window.localStorage.setItem(PASSWORD_KEY, password);
};

export const clearAuthentication = () => {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.removeItem(AUTH_KEY);
  window.localStorage.removeItem(USERNAME_KEY);
  window.localStorage.removeItem(PASSWORD_KEY);
};
