import { Avatar, Divider, IconButton, Menu, MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "styles/components/_navigation.scss";
import { useEffect } from "react";
import { useLogoutUserMutation } from "api/authApi";
import { IUser } from "features/userSlice";
export default function AuthUserMenu({
  user,
  anchorEl,
  handleClose,
}: {
  user: IUser;
  anchorEl: HTMLElement | null;
  handleClose: () => void;
}) {
  const navigate = useNavigate();
  const [logoutUser, { isSuccess }] = useLogoutUserMutation();
  const onLogoutHandler = async () => {
    logoutUser();
  };
  useEffect(() => {
    if (isSuccess) {
      navigate("/");
    }
  }, [isSuccess, navigate]);
  return (
    <>
      <Menu
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left",
        }}
        keepMounted
        disablePortal
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
          <IconButton>
            <Avatar
              alt="User menu avatar"
              src={"http://127.0.0.1:81/files/" + user.image}
            />
          </IconButton>
        </MenuItem>
        <MenuItem
          onClick={() => {
            navigate(`/users/${user.username}`);
            handleClose();
          }}
        >
          {user?.username}
        </MenuItem>
        <Divider flexItem />
        <MenuItem
          onClick={() => {
            navigate(`/users/${user.username}/settings`);
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
    </>
  );
}
