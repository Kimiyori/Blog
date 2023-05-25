import { createRandomUser, renderWithProviders } from "utils/test-utils";
import ChangePassword from "../ChangePassword";
import { fireEvent, screen, waitFor } from "@testing-library/react";
import { baseUrl } from "api/customFetchBase";
import { setupServer } from "msw/lib/node";
import { rest } from "msw";
import { ToastContainer } from "react-toastify";

const USER_DATA = createRandomUser();
describe("rendering", () => {
  test("correct renders", async () => {
    renderWithProviders(<ChangePassword />, {
      preloadedState: {
        userState: { user: USER_DATA },
      },
    });
    expect(screen.getByText(/Change password/i)).toBeInTheDocument();
    expect(screen.getByText(/Save/i)).toBeInTheDocument();
  });
});
describe("callbacks", () => {
  const server = setupServer();

  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  test("successful change password", async () => {
    server.use(
      rest.patch(`${baseUrl}/users`, (req, res, ctx) => {
        return res(ctx.json({ email: "new_email@gmail.com" }));
      })
    );
    const { store } = renderWithProviders(
      <>
        <ToastContainer />
        <ChangePassword />
      </>,
      {
        preloadedState: {
          userState: { user: USER_DATA },
        },
      }
    );
    const inputs = screen.getAllByTestId(
      "auth-data-input"
    ) as HTMLInputElement[];
    fireEvent.change(inputs[0], { target: { value: "newpassword" } });
    fireEvent.change(inputs[1], { target: { value: "newpassword" } });
    const button = screen.getByRole("button");
    fireEvent.click(button);
    expect(
      await screen.findByText("You have successfully changed your password")
    ).toBeInTheDocument();
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
        <ChangePassword />
      </>,
      {
        preloadedState: {
          userState: { user: USER_DATA },
        },
      }
    );
    const inputs = screen.getAllByTestId(
      "auth-data-input"
    ) as HTMLInputElement[];
    fireEvent.change(inputs[0], { target: { value: "newpassword" } });
    fireEvent.change(inputs[1], { target: { value: "newpassword" } });
    const button = screen.getByRole("button");
    fireEvent.click(button);
    expect(await screen.findByText("Server error")).toBeInTheDocument();
  });
});
