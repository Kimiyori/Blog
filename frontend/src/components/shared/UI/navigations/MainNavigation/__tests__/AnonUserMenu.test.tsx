import { useState } from "react";
import AnonUserMenu from "../AnontUserMenu";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
const mockedUsedNavigate = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockedUsedNavigate,
}));

beforeEach(() => mockedUsedNavigate.mockReset());
const TestAnonUserMenu = () => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  return (
    <>
      <button type="button" onClick={handleMenu}>
        Trigger Button
      </button>
      <AnonUserMenu anchorEl={anchorEl} handleClose={handleClose} />
    </>
  );
};

describe("rendering", () => {
  test("initial state", async () => {
    render(<TestAnonUserMenu />);
    expect(screen.getByRole("menu", { hidden: true })).toBeInTheDocument();
    expect(screen.getByRole("presentation", { hidden: true })).toHaveClass(
      "MuiModal-hidden"
    );
    expect(screen.getByText(/Sign Up/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign In/i)).toBeInTheDocument();
    expect(screen.getAllByRole("menuitem", { hidden: true }).length).toBe(2);
  });
  test("state acter trigger menu", async () => {
    render(<TestAnonUserMenu />);
    fireEvent.click(screen.getByText(/Trigger Button/i));
    expect(
      screen.queryByRole("presentation", { hidden: true })
    ).not.toHaveClass("MuiModal-hidden");
  });
});
describe("callbacks", () => {
  test("click to 'sign in' link", async () => {
    render(<TestAnonUserMenu />);
    fireEvent.click(screen.getByText(/Sign In/i));
    await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(1));
    await waitFor(() =>
      expect(mockedUsedNavigate).toHaveBeenCalledWith("/login")
    );
  });
  test("click to 'sign up' link", async () => {
    render(<TestAnonUserMenu />);
    fireEvent.click(screen.getByText(/Sign Up/i));
    await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(1));
    await waitFor(() =>
      expect(mockedUsedNavigate).toHaveBeenCalledWith("/register")
    );
  });
});
