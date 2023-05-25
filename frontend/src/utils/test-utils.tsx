import React, { PropsWithChildren } from "react";
import { render } from "@testing-library/react";
import type { RenderOptions } from "@testing-library/react";
import type { PreloadedState } from "@reduxjs/toolkit";
import { Provider } from "react-redux";
import { faker } from "@faker-js/faker";
import { AppStore, RootState, setupStore } from "../app/store";
import { IUser } from "features/userSlice";
// As a basic setup, import your same slice reducers

// This type interface extends the default options for render from RTL, as well
// as allows the user to specify other things such as initialState, store.
interface ExtendedRenderOptions extends Omit<RenderOptions, "queries"> {
  preloadedState?: PreloadedState<RootState>;
  store?: AppStore;
}

export function renderWithProviders(
  ui: React.ReactElement,
  {
    preloadedState = {},
    // Automatically create a store instance if no store was passed in
    store = setupStore(preloadedState),
    ...renderOptions
  }: ExtendedRenderOptions = {}
) {
  function Wrapper({ children }: PropsWithChildren<{}>): JSX.Element {
    return <Provider store={store}>{children}</Provider>;
  }
  return { store, ...render(ui, { wrapper: Wrapper, ...renderOptions }) };
}

export function createRandomUser(): IUser {
  return {
    _id: faker.string.uuid(),
    image: faker.image.avatar(),
    email: faker.internet.email(),
    username: faker.internet.userName(),
    createdAt:  faker.date.anytime().toJSON(),
    updatedAt: faker.date.anytime().toJSON(),
    type: faker.helpers.arrayElement(["admin", "user"]),
  };
}
