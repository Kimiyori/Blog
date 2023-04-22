import { useCookies } from "react-cookie";
import { Navigate, Outlet, useLocation } from "react-router-dom";
const UserForbid = () => {
  const [cookies] = useCookies(["logged_in"]);
  const location = useLocation();

  return cookies.logged_in ? (
    <Navigate to="/" state={{ from: location }} replace />
  ) : (
    <Outlet />
  );
};

export default UserForbid;
