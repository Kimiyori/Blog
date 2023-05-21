import {
  AppBar,
  Avatar,
  Box,
  IconButton,
  Toolbar,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAppSelector } from "app/store";
import "styles/components/_navigation.scss";
import AuthUserMenu from "./AuthtUserMenu";
import AnonUserMenu from "./AnontUserMenu";
import { useState } from "react";

export default function Navbar() {
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.userState.user);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography
            className="main-title"
            variant="h6"
            onClick={() => navigate("/")}
            sx={{ cursor: "pointer" }}
          >
            SAERY BLOG
          </Typography>
          <Box sx={{ ml: "auto" }}>
            <IconButton onClick={handleMenu}>
              <Avatar
                alt="User header menu avatar"
                src={user ? "http://127.0.0.1:81/files/" + user.image : ""}
              />
            </IconButton>
            {user ? (
              <AuthUserMenu
                user={user}
                anchorEl={anchorEl}
                handleClose={handleClose}
              />
            ) : (
              <AnonUserMenu anchorEl={anchorEl} handleClose={handleClose} />
            )}
          </Box>
        </Toolbar>
      </AppBar>
    </>
  );
}
