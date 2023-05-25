import { createApi } from "@reduxjs/toolkit/query/react";
import { setUser, updateUser } from "../features/userSlice";
import { IUser, IGenericResponse } from "features/userSlice";
import { RegisterInput } from "pages/Register/Register.page";
import customFetchBase from "./customFetchBase";

export type UpdateUserData = {
  image?: File | string;
  email?: string;
  password?: string;
};
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
      Omit<IUser, "createdAt" | "_id" | "type">,
      {
        userData?: UpdateUserData;
        userImage?: Pick<UpdateUserData, "image">;
      }
    >({
      query({ userData, userImage }) {
        // const formData = new FormData();
        // userImage &&
        //   userImage.image &&
        //   formData.append("user_image", userImage.image, userImage.image.name);
        // userData && formData.append("user_data", JSON.stringify(userData));
        return {
          url: `users`,
          method: "PATCH",
          body: JSON.stringify({user_data:userData}),
          credentials: "include",
        };
      },
      async onQueryStarted(args, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          dispatch(updateUser(data));
        } catch (error) {
          console.log(error);
        }
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
