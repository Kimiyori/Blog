import { screen } from "@testing-library/react";
import {
  createRandomUser,
  renderWithProviders,
} from "utils/test-utils";
import Navbar from "../MainNavigation";

const mockedUsedNavigate = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockedUsedNavigate,
}));

const USER_DATA = createRandomUser();

beforeEach(() => mockedUsedNavigate.mockReset());

describe("rendering", () => {
  test("initial state", async () => {
    renderWithProviders(<Navbar />);
    expect(screen.getByText(/SAERY BLOG/i)).toBeInTheDocument();
  });
  test("initial state anon user", async () => {
    renderWithProviders(<Navbar />);
    expect(screen.getByTestId(/PersonIcon/i)).toBeInTheDocument();
    expect(screen.getByRole("menu", { hidden: true })).toBeInTheDocument();
    expect(screen.getByRole("presentation", { hidden: true })).toHaveClass(
      "MuiModal-hidden"
    );
    expect(screen.getByText(/Sign Up/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign In/i)).toBeInTheDocument();
    expect(screen.getAllByRole("menuitem", { hidden: true }).length).toBe(2);
  });
  test("initial state auth user", async () => {
    renderWithProviders(<Navbar />, {
      preloadedState: {
        userState: { user: USER_DATA },
      },
    });
    expect(screen.getByRole("menu", { hidden: true })).toBeInTheDocument();
    expect(screen.getByRole("presentation", { hidden: true })).toHaveClass(
      "MuiModal-hidden"
    );
    expect(screen.getByAltText(/User header menu avatar/i)).toBeInTheDocument();
    const headerImage = screen.getByAltText(
      /User menu avatar/i
    ) as HTMLImageElement;
    expect(headerImage).toBeInTheDocument();
    expect(headerImage.src).toContain(
      "http://127.0.0.1:81/files/" + USER_DATA.image
    );
    expect(screen.getByText(USER_DATA.username)).toBeInTheDocument();
    expect(screen.getByText(/Settings/i)).toBeInTheDocument();
    expect(screen.getByText(/Logout/i)).toBeInTheDocument();
    expect(screen.getAllByRole("menuitem", { hidden: true }).length).toBe(4);
  });
});
