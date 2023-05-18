import { SerializedError } from "@reduxjs/toolkit";
import { FetchBaseQueryError } from "@reduxjs/toolkit/dist/query";
import { useContext, useEffect } from "react";
import { toast } from "react-toastify";
import { ThemeContext } from "./theme-context";

const capitalizeString = (str: string) =>
  str.replace(/^./, (char: string) => char.toUpperCase());

const NotifyMessage = (
  message: string,
  isLoading: boolean,
  isSuccess: boolean,
  isError: boolean,
  error: FetchBaseQueryError | SerializedError | undefined
) => {
  const { theme } = useContext(ThemeContext);
  const notifyTime = 2000;
  const position = "bottom-right";
  useEffect(
    () => {
      if (isSuccess) {
        toast.success(capitalizeString(message), {
          position: position,
          autoClose: notifyTime,
          theme: theme,
        });
      }

      if (isError) {
        toast.error(capitalizeString((error as any).data.detail), {
          position: position,
          autoClose: notifyTime,
          theme: theme,
        });
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [isLoading]
  );
};
export default NotifyMessage;
