import { useState } from "react";
import { fireEvent, screen, waitFor, within } from "@testing-library/react";
import { createRandomUser, renderWithProviders } from "utils/test-utils";
import AuthUserMenu from "../AuthtUserMenu";
import { baseUrl } from "api/customFetchBase";
import { setupServer } from "msw/lib/node";
import { rest } from "msw";
const mockedUsedNavigate = jest.fn();

const USER_DATA = createRandomUser();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockedUsedNavigate,
}));

beforeEach(() => mockedUsedNavigate.mockReset());
const TestAuthUserMenu = () => {
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
      <AuthUserMenu
        user={USER_DATA}
        anchorEl={anchorEl}
        handleClose={handleClose}
      />
    </>
  );
};

describe("rendering", () => {
  test("initial state", async () => {
    renderWithProviders(<TestAuthUserMenu />);
    expect(screen.getByRole("menu", { hidden: true })).toBeInTheDocument();
    expect(screen.getByRole("presentation", { hidden: true })).toHaveClass(
      "MuiModal-hidden"
    );
    expect(screen.getByAltText(/User menu avatar/i)).toBeInTheDocument();
    expect(screen.getByText(USER_DATA.username)).toBeInTheDocument();
    expect(screen.getByText(/Settings/i)).toBeInTheDocument();
    expect(screen.getByText(/Logout/i)).toBeInTheDocument();
    expect(screen.getAllByRole("menuitem", { hidden: true }).length).toBe(4);
  });
  test("state after trigger menu", async () => {
    renderWithProviders(<TestAuthUserMenu />);
    fireEvent.click(screen.getByText(/Trigger Button/i));
    expect(
      screen.queryByRole("presentation", { hidden: true })
    ).not.toHaveClass("MuiModal-hidden");
  });
});
describe("callbacks", () => {
  test("click to logout button", async () => {
    const server = setupServer(
      rest.get(`${baseUrl}/auth/logout`, (req, res, ctx) => {
        return res(ctx.status(200));
      })
    );
    server.listen();
    renderWithProviders(<TestAuthUserMenu />);
    fireEvent.click(screen.getByText(/Logout/i));
    await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(1));
    await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledWith("/"));
  });
  test("click to settings", async () => {
    renderWithProviders(<TestAuthUserMenu />);
    fireEvent.click(screen.getByText(/Settings/i));
    await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(1));
    await waitFor(() =>
      expect(mockedUsedNavigate).toHaveBeenCalledWith(
        `/users/${USER_DATA.username}/settings`
      )
    );
  });
  test("click to username", async () => {
    renderWithProviders(<TestAuthUserMenu />);
    fireEvent.click(screen.getByText(USER_DATA.username));
    await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(1));
    await waitFor(() =>
      expect(mockedUsedNavigate).toHaveBeenCalledWith(
        `/users/${USER_DATA.username}`
      )
    );
  });
  test("click to avatar", async () => {
    renderWithProviders(<TestAuthUserMenu />);
    const button = within(screen.getByRole("menu", { hidden: true })).getByRole(
      "button",
      { hidden: true }
    );
    fireEvent.click(button);
    await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(1));
    await waitFor(() =>
      expect(mockedUsedNavigate).toHaveBeenCalledWith(
        `/users/${USER_DATA.username}`
      )
    );
  });
});
