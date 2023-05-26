import { Box, Switch, Typography } from "@mui/material";
import { useContext } from "react";
import { ThemeContext } from "features/theme-context";

const ChangeColorTheme = () => {
  const { theme, setTheme } = useContext(ThemeContext);

  const handleThemeChange = () => {
    const isCurrentLight = theme === "light";
    setTheme(isCurrentLight ? "dark" : "light");
    localStorage.setItem("default-theme", isCurrentLight ? "dark" : "light");
  };
  return (
    <>
      <Box className="settings-block">
        <Box className="settings-block__label">
          <Typography variant="h6">Change color theme</Typography>
          <Switch
            checked={theme === "dark"}
            onChange={handleThemeChange}
            inputProps={{ "aria-label": "controlled" }}
          />
        </Box>
      </Box>
    </>
  );
};

export default ChangeColorTheme;
