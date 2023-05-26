import { Stack } from "@mui/material";
import "styles/pages/user_settings.scss";
import ChangePassword from "components/features/settings/ChangePassword";
import ChangeEmail from "components/features/settings/ChangeEmail";
import ChangeColorTheme from "components/features/settings/ChangeColorTheme";
const UserSettingsPage = () => {
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
