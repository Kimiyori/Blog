import {
  AppBar,
  Avatar,
  Box,
  Divider,
  IconButton,
  Toolbar,
  Menu,
  MenuItem,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAppSelector } from "app/store";
import { useLogoutUserMutation } from "api/authApi";
import { useEffect } from "react";
import { toast } from "react-toastify";
import React from "react";
import "styles/components/_navigation.scss";

export default function Navbar() {
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.userState.user);
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [logoutUser, { isLoading, isSuccess, error, isError }] =
    useLogoutUserMutation();

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
  useEffect(() => {
    if (isSuccess) {
      // window.location.href = '/login';
      navigate("/login");
    }

    if (isError) {
      toast.error((error as any).data.message, {
        position: "top-right",
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLoading]);
  const onLogoutHandler = async () => {
    logoutUser();
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography
            variant="h6"
            onClick={() => navigate("/")}
            sx={{ cursor: "pointer" }}
          >
            SAERY BLOG
          </Typography>
          <Box display="flex" sx={{ ml: "auto" }}>
            <IconButton
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              sx={{ p: 0 }}
            >
              <Avatar alt="Remy Sharp" src="/static/images/avatar/2.jpg" />
            </IconButton>
            {!user ? (
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: "bottom",
                  horizontal: "left",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "left",
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem
                  onClick={() => {
                    navigate("/register");
                    handleClose();
                  }}
                >
                  Sign Up
                </MenuItem>
                <MenuItem
                  onClick={() => {
                    navigate("/login");
                    handleClose();
                  }}
                >
                  Sign In
                </MenuItem>
              </Menu>
            ) : (
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: "bottom",
                  horizontal: "left",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "left",
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem
                  onClick={() => {
                    navigate(`/users/${user.username}`);
                    handleClose();
                  }}
                >
                  <IconButton
                    aria-label="account of current user"
                    aria-controls="menu-appbar"
                    aria-haspopup="true"
                    onClick={handleMenu}
                    sx={{ p: 0 }}
                  >
                    <Avatar alt="Remy Sharp" />
                  </IconButton>
                </MenuItem>
                <MenuItem
                  onClick={() => {
                    navigate(`/users/${user.username}`);
                    handleClose();
                  }}
                >
                  {user.username}
                </MenuItem>
                <Divider flexItem />
                <MenuItem
                  onClick={() => {
                    navigate(`/settings`);
                    handleClose();
                  }}
                >
                  Settings
                </MenuItem>
                <MenuItem
                  onClick={() => {
                    onLogoutHandler();
                    handleClose();
                  }}
                >
                  Logout
                </MenuItem>
              </Menu>
            )}
          </Box>
        </Toolbar>
      </AppBar>
    </>
  );
}
