import { createApi } from "@reduxjs/toolkit/query/react";
import { setUser } from "../features/userSlice";
import { IUser, IGenericResponse } from "features/userSlice";
import { RegisterInput } from "pages/Register/Register.page";
import customFetchBase from "./customFetchBase";

export type UpdateUser = { image?: File; email?: string; password?: string };
type UpdateUserResponse = { image?: string; email?: string };
export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: customFetchBase,
  tagTypes: ["User"],
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
    getMe: builder.query<IUser, null>({
      query() {
        return {
          url: "users/me",
          credentials: "include",
        };
      },
      async onQueryStarted(args, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          dispatch(setUser(data));
        } catch (error) {}
      },
    }),
    getUser: builder.query<IUser, string>({
      query(username) {
        return {
          url: `users/${username}`,
        };
      },
    }),
    updateUser: builder.mutation<
      UpdateUserResponse,
      { username: string; body: UpdateUser }
    >({
      query({ username, body }) {
        let form = new FormData();
        body.image &&
          form.append("image", body.image as File, body?.image?.name as string);
        body.password && form.append("password", body.password as string);
        body.email && form.append("email", body.email as string);
        return {
          url: `users/${username}`,
          method: "PATCH",
          body: form,
          credentials: "include",
        };
      },
    }),
  }),
});
export const {
  useGetUserQuery,
  useGetMeQuery,
  useRegisterUserMutation,
  useUpdateUserMutation,
} = userApi;
