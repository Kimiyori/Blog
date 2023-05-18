import { rest } from "msw";
import { setupServer } from "msw/node";
import { fireEvent, screen, waitFor } from "@testing-library/react";
import { renderWithProviders } from "../../../utils/test-utils";
import { baseUrl } from "api/customFetchBase";
import RegisterPage from "../Register.page";
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
        <RegisterPage />
      </Router>
    );
    expect(screen.getAllByTestId("auth-data-input").length).toBe(4);
    expect(screen.getByText(/Username/i)).toBeInTheDocument();
    expect(screen.getByText("Password")).toBeInTheDocument();
    expect(screen.getByText(/Confirm Password/i)).toBeInTheDocument();
    expect(screen.getByText(/Email Address/i)).toBeInTheDocument();
  });
  test("correct renders button", async () => {
    renderWithProviders(
      <Router>
        <RegisterPage />
      </Router>
    );
    expect(screen.getByText(/Sign Up/i)).toBeInTheDocument();
  });
  test("correct renders welcome text", async () => {
    renderWithProviders(
      <Router>
        <RegisterPage />
      </Router>
    );
    expect(screen.getByText(/Welcome!/i)).toBeInTheDocument();
  });
  test("correct renders login text", async () => {
    renderWithProviders(
      <Router>
        <RegisterPage />
      </Router>
    );
    expect(screen.getByText(/Already have an account\?/i)).toBeInTheDocument();
    expect(screen.getByText(/Login here/i)).toBeInTheDocument();
  });
});
describe("callbacks", () => {
  test("login page redirect", async () => {
    const history = createMemoryHistory();

    history.push = jest.fn();
    renderWithProviders(
      <Router1 location={history.location} navigator={history}>
        <RegisterPage />
      </Router1>
    );
    const loginPageLink = screen.getByText(/Login here/i) as HTMLButtonElement;
    fireEvent.click(loginPageLink);
    expect(history.push).toHaveBeenCalledWith(
      {
        hash: "",
        pathname: "/login",
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
          <RegisterPage />
        </Router>
      );
      expect(
        screen.queryByText(/Full name is required/i)
      ).not.toBeInTheDocument();
      expect(
        screen.queryByText(/Email Address is invalid/i)
      ).not.toBeInTheDocument();
      expect(
        screen.queryByText(/Password must be more than 8 characters/i)
      ).not.toBeInTheDocument();
      expect(
        screen.queryByText(/Passwords do not match/i)
      ).not.toBeInTheDocument();
    });
    test("input login", async () => {
      renderWithProviders(
        <Router>
          <RegisterPage />
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
    test("input email", async () => {
      renderWithProviders(
        <Router>
          <RegisterPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[1], { target: { value: "wrong_email_input" } });
      const button = screen.getByRole("button");
      fireEvent.click(button);

      expect(
        await screen.findByText(/Email Address is invalid/i)
      ).toBeInTheDocument();
    });
    test("input password", async () => {
      renderWithProviders(
        <Router>
          <RegisterPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[2], { target: { value: "pass" } });
      const button = screen.getByRole("button");
      fireEvent.click(button);

      expect(
        await screen.findByText(/Password must be more than 8 characters/i)
      ).toBeInTheDocument();
    });
    test("input password confirm", async () => {
      renderWithProviders(
        <Router>
          <RegisterPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[2], { target: { value: "pass" } });

      const button = screen.getByRole("button");
      fireEvent.click(button);

      expect(
        await screen.findByText(/Please confirm your password/i)
      ).toBeInTheDocument();
    });
    test("input password doesnt match", async () => {
      renderWithProviders(
        <Router>
          <RegisterPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[2], { target: { value: "pass" } });
      fireEvent.change(inputs[3], { target: { value: "pass123" } });
      const button = screen.getByRole("button");
      fireEvent.click(button);

      expect(
        await screen.findByText(/Passwords do not match/i)
      ).toBeInTheDocument();
    });
  });
  describe("right inputs", () => {
    const handlersSuccess = [
      rest.post(`${baseUrl}/users`, (req, res, ctx) => {
        return res(ctx.json("John Smith"));
      }),
    ];

    const server = setupServer(...handlersSuccess);
    // Enable API mocking before tests.
    beforeAll(() => server.listen());
    // Reset any runtime request handlers we may add during the tests.
    afterEach(() => server.resetHandlers());

    // Disable API mocking after the tests are done.
    afterAll(() => server.close());
    test("successful register user", async () => {
      renderWithProviders(
        <Router>
          <ToastContainer />
          <RegisterPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[0], { target: { value: USER_DATA["username"] } });
      fireEvent.change(inputs[1], { target: { value: USER_DATA["email"] } });
      fireEvent.change(inputs[2], { target: { value: USER_DATA["password"] } });
      fireEvent.change(inputs[3], { target: { value: USER_DATA["password"] } });
      const button = screen.getByRole("button");
      fireEvent.click(button);
      await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(1));
      await waitFor(() =>
        expect(mockedUsedNavigate).toHaveBeenCalledWith("/login")
      );
      expect(
        await screen.findByText("User registered successfully")
      ).toBeInTheDocument();
    });
    test("server error", async () => {
      server.use(
        rest.post(`${baseUrl}/users`, (req, res, ctx) => {
          return res(
            ctx.status(409),
            ctx.json({ detail: "user or email already exist" })
          );
        })
      );
      renderWithProviders(
        <Router>
          <ToastContainer />
          <RegisterPage />
        </Router>
      );
      const inputs = screen.getAllByTestId(
        "auth-data-input"
      ) as HTMLInputElement[];
      fireEvent.change(inputs[0], { target: { value: USER_DATA["username"] } });
      fireEvent.change(inputs[1], { target: { value: USER_DATA["email"] } });
      fireEvent.change(inputs[2], { target: { value: USER_DATA["password"] } });
      fireEvent.change(inputs[3], { target: { value: USER_DATA["password"] } });
      const button = screen.getByRole("button");
      fireEvent.click(button);
      await waitFor(() => expect(mockedUsedNavigate).toHaveBeenCalledTimes(0));
      await waitFor(() =>
        expect(mockedUsedNavigate).not.toHaveBeenCalledWith("/login")
      );
      expect(
        await screen.findByText("User or email already exist")
      ).toBeInTheDocument();
    });
  });
});
