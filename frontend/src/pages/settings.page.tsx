import { useAppSelector } from "app/store";
import { useGetUserQuery } from "api/userApi";
import {
  Box,
  Button,
  Divider,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import "styles/pages/user_settings.scss";
import ChangePassword from "components/features/settings/ChangePassword";
import ChangeEmail from "components/features/settings/ChangeEmail";
import ChangeColorTheme from "components/features/settings/ChangeColorTheme";
const UserSettingsPage = () => {
  const user = useAppSelector((state) => state.userState.user);
  return (
    <>
      <Stack>
        <ChangePassword />
        <ChangeEmail />
        <ChangeColorTheme />
      </Stack>
    </>
  );
};

export default UserSettingsPage;
