import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import MainLayout from "components/shared/UI/layouts/MainLayout";
import RegisterPage from "pages/Register/Register.page";
import LoginPage from "pages/Login/Login.page";
import HomePage from "pages/home.page";
import UnauthorizePage from "pages/unauthorize.page";
import RequireUser from "components/features/requireUser";
import AdminPage from "pages/admin.page";
import UserForbid from "components/features/userForbid";
import ProfilePage from "pages/UserProfile/profile.page";
import UserSettingsPage from "pages/settings.page";
import { ThemeProvider } from "features/theme-context";

function App() {
  return (
    <>
      <ToastContainer />
      <ThemeProvider>
        <Router>
          <Routes>
            <Route path="/" element={<MainLayout />}>
              <Route index element={<HomePage />} />
              <Route path="/users/:username" element={<ProfilePage />} />
              <Route element={<UserForbid />}>
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/login" element={<LoginPage />} />
              </Route>
              <Route element={<RequireUser allowedRoles={["user"]} />}>
                <Route path="admin" element={<AdminPage />} />
                <Route
                  path="/users/:username/settings"
                  element={<UserSettingsPage />}
                />
              </Route>
              <Route path="unauthorized" element={<UnauthorizePage />} />
            </Route>
          </Routes>
        </Router>
      </ThemeProvider>
    </>
  );
}

export default App;
