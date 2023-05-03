import { Avatar, Divider, IconButton, Menu, MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAppSelector } from "app/store";
import "styles/components/_navigation.scss";

export default function UserNavMenu({
  anchorEl,
  handleClose,
  onLogoutHandler,
}: {
  anchorEl: HTMLElement | null;
  handleClose: () => void;
  onLogoutHandler: () => Promise<void>;
}) {
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.userState.user);

  const AnonUser = () => {
    return (
      <Menu
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
    );
  };
  const AuthUser = () => {
    return (
      <Menu
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
            navigate(`/users/${user?.username}`);
            handleClose();
          }}
        >
          <IconButton
          >
            <Avatar
              alt="Remy Sharp"
              src={"http://127.0.0.1:81/files/" + user?.image}
            />
          </IconButton>
        </MenuItem>
        <MenuItem
          onClick={() => {
            navigate(`/users/${user?.username}`);
            handleClose();
          }}
        >
          {user?.username}
        </MenuItem>
        <Divider flexItem />
        <MenuItem
          onClick={() => {
            navigate(`/users/${user?.username}/settings`);
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
    );
  };
  return <>{!user ? <AnonUser /> : <AuthUser />}</>;
}
