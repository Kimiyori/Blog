import { useAppSelector } from "app/store";
import {
  useGetUserQuery,
  useUpdateUserMutation,
  UpdateUser,
} from "api/userApi";
import {
  Box,
  Button,
  Divider,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";
import { object, string, TypeOf } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import FormInput from "components/shared/Entity/FormInput";
import { LoadingButton } from "@mui/lab";
import { useContext, useEffect } from "react";
import { ThemeContext } from "features/theme-context";

const ChangeColorTheme = () => {
  const { theme, setTheme } = useContext(ThemeContext);

  const handleThemeChange = () => {
    const isCurrentDark = theme === "dark";
    setTheme(isCurrentDark ? "light" : "dark");
    localStorage.setItem("default-theme", isCurrentDark ? "light" : "dark");
  };

  return (
    <>
      <Box className="settings-block">
        <Box className="settings-block__label">
          <Typography variant="h6">Change color theme</Typography>
          <Switch
            checked={theme === "light"}
            onChange={handleThemeChange}
            inputProps={{ "aria-label": "controlled" }}
          />
        </Box>
      </Box>
    </>
  );
};

export default ChangeColorTheme;
