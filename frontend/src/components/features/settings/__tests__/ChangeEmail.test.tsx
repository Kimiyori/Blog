import { createRandomUser, renderWithProviders } from "utils/test-utils";
import ChangeEmail from "../ChangeEmail";
import { fireEvent, screen, waitFor } from "@testing-library/react";
import { baseUrl } from "api/customFetchBase";
import { setupServer } from "msw/lib/node";
import { rest } from "msw";
import { ToastContainer } from "react-toastify";

const USER_DATA = createRandomUser();
describe("rendering", () => {
  test("correct renders", async () => {
    renderWithProviders(<ChangeEmail />, {
      preloadedState: {
        userState: { user: USER_DATA },
      },
    });
    expect(screen.getByText(/Change email/i)).toBeInTheDocument();
    expect(screen.getByText(/Save/i)).toBeInTheDocument();
  });
});
describe("callbacks", () => {
  const server = setupServer();

  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  test("successful change email", async () => {
    server.use(
      rest.patch(`${baseUrl}/users`, (req, res, ctx) => {
        return res(ctx.json({ email: "new_email@gmail.com" }));
      })
    );
    const { store } = renderWithProviders(
      <>
        <ToastContainer />
        <ChangeEmail />
      </>,
      {
        preloadedState: {
          userState: { user: USER_DATA },
        },
      }
    );
    const input = screen.getByTestId("auth-data-input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "new_email@gmail.com" } });
    const button = screen.getByRole("button");
    fireEvent.click(button);
    expect(
      await screen.findByText(
        "You have successfully changed your email address"
      )
    ).toBeInTheDocument();
    await waitFor(() =>
      expect(store.getState().userState.user?.email).toStrictEqual(
        "new_email@gmail.com"
      )
    );
  });
  test("fail change email due to server error", async () => {
    server.use(
      rest.patch(`${baseUrl}/users`, (req, res, ctx) => {
        return res(ctx.status(503), ctx.json({ detail: "Server error" }));
      })
    );
    renderWithProviders(
      <>
        <ToastContainer />
        <ChangeEmail />
      </>,
      {
        preloadedState: {
          userState: { user: USER_DATA },
        },
      }
    );
    const input = screen.getByTestId("auth-data-input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "new_email@gmail.com" } });
    const button = screen.getByRole("button");
    fireEvent.click(button);
    expect(await screen.findByText("Server error")).toBeInTheDocument();
  });
});
