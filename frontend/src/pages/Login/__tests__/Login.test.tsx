import { rest } from "msw";
import { setupServer } from "msw/node";
import { fireEvent, screen, waitFor } from "@testing-library/react";
import { renderWithProviders } from "../../../utils/test-utils";
import { baseUrl } from "api/customFetchBase";
import LoginPage from "../Login.page";
import { BrowserRouter as Router, Router as Router1 } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import { createMemoryHistory } from "history";

const USER_DATA = {
  username: "teststring22",
  password: "string22",
  email: "test@gmail.com",
};

// We use msw to intercept the network request during the test,
// and return the response 'John Smith' after 150ms
// when receiving a get request to the `/api/user` endpoint

const mockedUsedNavigate = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockedUsedNavigate,
}));

beforeEach(() => mockedUsedNavigate.mockReset());

describe("rendering", () => {
  test("correct renders inputes", async () => {
    renderWithProviders(
      <Router>
        <LoginPage />
      </Router>
    );
    expect(screen.getAllByTestId("auth-data-input").length).toBe(2);
    expect(screen.getByText(/Username/i)).toBeInTheDocument();
    expect(screen.getByText("Password")).toBeInTheDocument();
  });
  test("correct renders button", async () => {
    renderWithProviders(
      <Router>
        <LoginPage />
      </Router>
    );
    expect(screen.getByText(/Login/i)).toBeInTheDocument();
  });
  test("correct renders welcome text", async () => {
    renderWithProviders(
      <Router>
        <LoginPage />
      </Router>
    );
    expect(screen.getByText(/Welcome Back!/i)).toBeInTheDocument();
  });
  test("correct renders sign up text", async () => {
    renderWithProviders(
      <Router>
        <LoginPage />
      </Router>
    );
    expect(screen.getByText(/Need an account\?/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign Up/i)).toBeInTheDocument();
  });
});
describe("callbacks", () => {
  test("login page redirect", async () => {
    const history = createMemoryHistory();

    history.push = jest.fn();
    renderWithProviders(
      <Router1 location={history.location} navigator={history}>
        <LoginPage />
      </Router1>
    );
    const loginPageLink = screen.getByText(/Sign Up/i) as HTMLButtonElement;
    fireEvent.click(loginPageLink);
    expect(history.push).toHaveBeenCalledWith(
      {
        hash: "",
        pathname: "/register",
        search: "",
      },
      undefined,
      {
        preventScrollReset: undefined,
        relative: undefined,
        replace: false,
        state: undefined,
      }
    );
  });
  describe("wrong inputs", () => {
    test("initial state", async () => {
      renderWithProviders(
        <Router>
          <LoginPage />
        </Router>
      );
      expect(
        screen.queryByText(/Full name is required/i)
      ).not.toBeInTheDocument();
      expect(
        screen.queryByText(/Password is required/i)
      ).not.toBeInTheDocument();
    });
    test("input login", async () => {
      renderWithProviders(
        <Router>
          <LoginPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[0], { target: { value: "" } });
      const button = screen.getByRole("button");
      fireEvent.click(button);
      expect(
        await screen.findByText(/Full name is required/i)
      ).toBeInTheDocument();
    });
    test("input password", async () => {
      renderWithProviders(
        <Router>
          <LoginPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[1], { target: { value: "" } });
      const button = screen.getByRole("button");
      fireEvent.click(button);

      expect(
        await screen.findByText(/Password is required/i)
      ).toBeInTheDocument();
    });
  });
  describe("right inputs", () => {
    const handlersSuccess = [
      rest.post(`${baseUrl}/auth/token`, (req, res, ctx) => {
        return res(ctx.json({ access_token: "123", refresh_token: "1234" }));
      }),
      rest.get(`${baseUrl}/users/me`, (req, res, ctx) => {
        return res(ctx.json({ username: USER_DATA.username }));
      }),
    ];

    const server = setupServer(...handlersSuccess);
    // Enable API mocking before tests.
    beforeAll(() => server.listen());
    // Reset any runtime request handlers we may add during the tests.
    afterEach(() => server.resetHandlers());

    // Disable API mocking after the tests are done.
    afterAll(() => server.close());
    test("successful sign in", async () => {
      renderWithProviders(
        <Router>
          <ToastContainer />
          <LoginPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[0], { target: { value: USER_DATA["username"] } });
      fireEvent.change(inputs[1], { target: { value: USER_DATA["password"] } });
      const button = screen.getByRole("button");
      fireEvent.click(button);
      await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(1));
      await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledWith("/"));
      expect(
        await screen.findByText("You successfully logged in")
      ).toBeInTheDocument();
    });
    test("server error", async () => {
      server.use(
        rest.post(`${baseUrl}/auth/token`, (req, res, ctx) => {
          return res(ctx.status(404), ctx.json({ detail: "Not exist" }));
        })
      );
      renderWithProviders(
        <Router>
          <ToastContainer />
          <LoginPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[0], { target: { value: USER_DATA["username"] } });
      fireEvent.change(inputs[1], { target: { value: USER_DATA["password"] } });
      const button = screen.getByRole("button");
      fireEvent.click(button);
      await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(0));
      expect(await screen.findByText("Not exist")).toBeInTheDocument();
    });
  });
});
