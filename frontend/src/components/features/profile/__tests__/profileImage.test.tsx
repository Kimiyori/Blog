import { renderWithProviders, createRandomUser } from "utils/test-utils";
import { fireEvent, screen, waitFor } from "@testing-library/react";
import ProfileImage from "../profileImage";
import Router from "react-router-dom";
import userEvent from "@testing-library/user-event";
import { baseUrl } from "api/customFetchBase";
import { rest } from "msw";
import { setupServer } from "msw/lib/node";
import { ToastContainer } from "react-toastify";

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useParams: jest.fn(),
}));
const USER_DATA = createRandomUser();
describe("rendering", () => {
  test("correct render image", async () => {
    jest.spyOn(Router, "useParams").mockReturnValue({ username: undefined });
    renderWithProviders(<ProfileImage img={USER_DATA.image} />);
    const avatar = screen.getByAltText(
      /User profile avatar/i
    ) as HTMLImageElement;
    expect(avatar).toBeInTheDocument();
    expect(avatar.src).toBe("http://127.0.0.1:81/files/" + USER_DATA.image);
  });
  describe("render upload image element", () => {
    describe("for not owner", () => {
      test("when not hover", async () => {
        jest
          .spyOn(Router, "useParams")
          .mockReturnValue({ username: undefined });
        renderWithProviders(<ProfileImage img={USER_DATA.image} />);
        expect(
          screen.queryByRole("button", { name: "upload picture" })
        ).not.toBeInTheDocument();
      });
      test("when hover", async () => {
        jest
          .spyOn(Router, "useParams")
          .mockReturnValue({ username: undefined });
        renderWithProviders(<ProfileImage img={USER_DATA.image} />);
        const avatar = screen.getByAltText(
          /User profile avatar/i
        ) as HTMLImageElement;
        userEvent.hover(avatar);
        expect(
          screen.queryByRole("button", { name: "upload picture" })
        ).not.toBeInTheDocument();
      });
    });
    describe("for owner", () => {
      test("when hover", async () => {
        jest
          .spyOn(Router, "useParams")
          .mockReturnValue({ username: USER_DATA.username });
        renderWithProviders(<ProfileImage img={USER_DATA.image} />, {
          preloadedState: {
            userState: { user: USER_DATA },
          },
        });
        const avatar = screen.getByAltText(
          /User profile avatar/i
        ) as HTMLImageElement;
        await userEvent.hover(avatar);
        expect(
          await screen.findByRole("button", { name: "upload picture" })
        ).toBeInTheDocument();
      });
      test("when not hover", async () => {
        jest
          .spyOn(Router, "useParams")
          .mockReturnValue({ username: USER_DATA.username });
        renderWithProviders(<ProfileImage img={USER_DATA.image} />, {
          preloadedState: {
            userState: { user: USER_DATA },
          },
        });
        expect(
          screen.queryByRole("button", { name: "upload picture" })
        ).not.toBeInTheDocument();
      });
    });
  });
});

describe("callbacks", () => {
  const server = setupServer();
  beforeAll(() => server.listen());

  afterEach(() => server.resetHandlers());

  afterAll(() => server.close());
  test("successful update image", async () => {
    server.use(
      rest.patch(`${baseUrl}/users`, (req, res, ctx) => {
        return res(ctx.json({ image: "hello.jpg" }));
      })
    );
    jest
      .spyOn(Router, "useParams")
      .mockReturnValue({ username: USER_DATA.username });
    const { store } = renderWithProviders(
      <>
        <ToastContainer />
        <ProfileImage img={USER_DATA.image} />
      </>,
      {
        preloadedState: {
          userState: { user: USER_DATA },
        },
      }
    );
    const file = new File(["hello"], "hello.jpg", { type: "image/jpeg" });
    const avatar = screen.getByAltText(
      /User profile avatar/i
    ) as HTMLImageElement;
    await userEvent.hover(avatar);
    const input = (await screen.findByTestId(
      /profile_image_upload/i
    )) as HTMLInputElement;
    await userEvent.upload(input, file);
    expect(
      await screen.findByText(
        "You have successfully updated your profile image"
      )
    ).toBeInTheDocument();
    await waitFor(() => {
      expect(
        (screen.getByAltText(/User profile avatar/i) as HTMLImageElement).src
      ).toStrictEqual("http://127.0.0.1:81/files/hello.jpg");
    });
    await waitFor(() =>
      expect(store.getState().userState.user?.image).toStrictEqual("hello.jpg")
    );
    expect(
      screen.queryByRole("button", { name: "upload picture" })
    ).not.toBeInTheDocument();
  });
  test("fail to update image due to server error", async () => {
    server.use(
      rest.patch(`${baseUrl}/users`, (req, res, ctx) => {
        return res(
          ctx.status(503),
          ctx.json({
            detail: `Server error`,
          })
        );
      })
    );
    jest
      .spyOn(Router, "useParams")
      .mockReturnValue({ username: USER_DATA.username });
    renderWithProviders(
      <>
        <ToastContainer />
        <ProfileImage img={USER_DATA.image} />
      </>,
      {
        preloadedState: {
          userState: { user: USER_DATA },
        },
      }
    );
    const file = new File(["hello"], "hello.jpg", { type: "image/jpeg" });
    const avatar = screen.getByAltText(
      /User profile avatar/i
    ) as HTMLImageElement;
    await userEvent.hover(avatar);
    const input = (await screen.findByTestId(
      /profile_image_upload/i
    )) as HTMLInputElement;
    await userEvent.upload(input, file);
    expect(await screen.findByText("Server error")).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "upload picture" })
    ).not.toBeInTheDocument();
  });
});
