import { PropsWithChildren, createContext, useState } from "react";
export type TypeColorTheme = {
  theme: "dark" | "light";
  setTheme: (theme: "dark" | "light") => void;
};
export const ThemeContext = createContext<TypeColorTheme>({
  theme: "light",
  setTheme: (theme: "dark" | "light") => {},
});

export const ThemeProvider = ({ children }: PropsWithChildren) => {
  const isBrowserDefaulDark = () =>
    window.matchMedia("(prefers-color-scheme: dark)").matches;

  const getDefaultTheme = (): "dark" | "light" => {
    const localStorageTheme = localStorage.getItem("default-theme") as
      | "dark"
      | "light"
      | null;
    const browserDefault = isBrowserDefaulDark() ? "dark" : "light";
    return localStorageTheme || browserDefault;
  };

  const [theme, setTheme] = useState(getDefaultTheme());
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <div className={`theme-${theme}`}>{children}</div>
    </ThemeContext.Provider>
  );
};
