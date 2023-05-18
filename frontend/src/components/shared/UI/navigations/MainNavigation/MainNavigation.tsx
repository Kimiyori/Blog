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
import { useLogoutUserMutation } from "api/authApi";
import { useEffect } from "react";
import { toast } from "react-toastify";
import React from "react";
import "styles/components/_navigation.scss";
import UserNavMenu from "./userMenu";

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
                alt="Remy Sharp"
                src={user ? "http://127.0.0.1:81/files/" + user.image : ""}
              />
            </IconButton>
            <UserNavMenu
              anchorEl={anchorEl}
              handleClose={handleClose}
              onLogoutHandler={onLogoutHandler}
            />
          </Box>
        </Toolbar>
      </AppBar>
    </>
  );
}
