import { render, screen } from "@testing-library/react";
import ChangeColorTheme from "../ChangeColorTheme";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { ThemeContext, ThemeProvider } from "features/theme-context";
export const mockLocalStorage = () => {
  const setItemMock = jest.fn();
  const getItemMock = jest.fn();

  beforeEach(() => {
    Storage.prototype.setItem = setItemMock;
    Storage.prototype.getItem = getItemMock;
  });

  afterEach(() => {
    setItemMock.mockRestore();
    getItemMock.mockRestore();
  });

  return { setItemMock, getItemMock };
};
export default global.matchMedia =
  global.matchMedia ||
  function (query) {
    return {
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(), // deprecated
      removeListener: jest.fn(), // deprecated
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    };
  };
const {  setItemMock } = mockLocalStorage();
describe("rendering", () => {
  test("correct rendering", async () => {
    render(<ChangeColorTheme />);
    expect(screen.getByText(/Change color theme/i)).toBeInTheDocument();
    expect(screen.getByRole("checkbox")).toBeInTheDocument();
  });
  test("initial state", async () => {
    render(<ChangeColorTheme />);
    expect(screen.queryByRole("checkbox")).not.toBeChecked()
  });
});
describe("callbacks", () => {
  test("switch checkbox to dark", async () => {
    render(
      <ThemeProvider>
        <ChangeColorTheme />
      </ThemeProvider>
    );
    await userEvent.click(screen.getByRole("checkbox"));
    expect(screen.getByRole("checkbox")).toBeChecked();
    expect(setItemMock).toHaveBeenCalledWith("default-theme", 'dark');
  });
  test("switch checkbox from dark to light", async () => {
    render(
      <ThemeProvider>
        <ChangeColorTheme />
      </ThemeProvider>
    );
    await userEvent.click(screen.getByRole("checkbox"));
    await userEvent.click(screen.getByRole("checkbox"));
    expect(screen.queryByRole("checkbox")).not.toBeChecked()
    expect(setItemMock).toHaveBeenCalledWith("default-theme", 'light');
  });
});
