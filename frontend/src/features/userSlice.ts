import { createSlice, PayloadAction } from "@reduxjs/toolkit";
export interface IUser {
  username: string;
  email: string | null;
  _id: string;
  createdAt: Date;
  updatedAt: Date;
  type: string;
}

export interface IGenericResponse {
  status: string;
  message: string;
}

interface IUserState {
  user: IUser | null;
}

const initialState: IUserState = {
  user: null,
};

export const userSlice = createSlice({
  initialState,
  name: "userSlice",
  reducers: {
    logout: () => initialState,
    setUser: (state, action: PayloadAction<IUser>) => {
      state.user = action.payload;
    },
  },
});

export default userSlice.reducer;

export const { logout, setUser } = userSlice.actions;
