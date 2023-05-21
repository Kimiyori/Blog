import { Menu, MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "styles/components/_navigation.scss";
export default function AnonUserMenu({
  anchorEl,
  handleClose,
}: {
  anchorEl: HTMLElement | null;
  handleClose: () => void;
}) {
  const navigate = useNavigate();
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
    </>
  );
}
