import { createContext } from "react";
export type TypeColorTheme = {
  theme: "dark" | "light";
  setTheme: (theme: "dark" | "light") => void;
};
export const ThemeContext = createContext<TypeColorTheme>({
  theme: "light",
  setTheme: (theme: "dark" | "light") => {},
});
