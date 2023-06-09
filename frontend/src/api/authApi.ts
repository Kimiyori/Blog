import { createApi } from "@reduxjs/toolkit/query/react";
import { LoginInput } from "pages/Login/Login.page";
import { logout } from "features/userSlice";
import { userApi } from "api/userApi";
import customFetchBase from "./customFetchBase";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: customFetchBase,
  endpoints: (builder) => ({
    loginUser: builder.mutation<
      { access_token: string; token_type: string },
      LoginInput
    >({
      query(data) {
        const form = new FormData();
        form.append("username", data.username);
        form.append("password", data.password);
        return {
          url: "auth/token",
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams(form as any), // eslint-disable-line
          credentials: "include",
        };
      },
      async onQueryStarted(args, { dispatch, queryFulfilled }) {
        await queryFulfilled;
        await dispatch(
          userApi.endpoints.getMe.initiate(null, { forceRefetch: true })
        );
      },
    }),
    logoutUser: builder.mutation<void, void>({
      query() {
        return {
          url: "auth/logout",
          credentials: "include",
        };
      },
      async onQueryStarted(args, { dispatch, queryFulfilled }) {
        await queryFulfilled;
        dispatch(logout());
      },
    }),
  }),
});

export const { useLoginUserMutation, useLogoutUserMutation } = authApi;
