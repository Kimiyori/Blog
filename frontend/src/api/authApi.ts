import { createApi } from "@reduxjs/toolkit/query/react";
import { LoginInput } from "pages/login.page";
import { RegisterInput } from "pages/register.page";
import { IGenericResponse, logout } from "features/userSlice";
import { userApi } from "api/userApi";
import customFetchBase from "./customFetchBase";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: customFetchBase,
  endpoints: (builder) => ({
    registerUser: builder.mutation<IGenericResponse, RegisterInput>({
      query(data) {
        const { passwordConfirm, ...body } = data;
        return {
          url: "users",
          method: "POST",
          body: body,
        };
      },
    }),
    loginUser: builder.mutation<
      { access_token: string; token_type: string },
      LoginInput
    >({
      query(data) {
        let form = new FormData();
        form.append("username", data.username);
        form.append("password", data.password);
        return {
          url: "users/token",
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams(form as any),
          credentials: "include",
        };
      },
      async onQueryStarted(args, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
          await dispatch(userApi.endpoints.getMe.initiate(null,{forceRefetch: true}));
        } catch (error) {}
      },
    }),
    logoutUser: builder.mutation<void, void>({
      query() {
        return {
          url: "users/logout",
          credentials: "include",
        };
      },
      async onQueryStarted(args, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
          dispatch(logout());
        } catch (error) {}
      },
    }),
  }),
});

export const {
  useLoginUserMutation,
  useRegisterUserMutation,
  useLogoutUserMutation,
} = authApi;
