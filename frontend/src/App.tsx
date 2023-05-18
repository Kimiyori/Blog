import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
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
import { ThemeContext } from "features/theme-context";

function App() {
  // Detecting the default theme
  const isBrowserDefaulDark = () =>
    window.matchMedia("(prefers-color-scheme: dark)").matches;

  const getDefaultTheme = (): "dark" | "light" => {
    const localStorageTheme = localStorage.getItem("default-theme") as
      | "dark"
      | "light"
      | null;
    const browserDefault = isBrowserDefaulDark() ? "dark" : "light";
    return localStorageTheme || browserDefault;
  };

  const [theme, setTheme] = useState(getDefaultTheme());

  return (
    <>
      <ToastContainer />
      <ThemeContext.Provider value={{ theme, setTheme }}>
        <div className={`theme-${theme}`}>
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
        </div>
      </ThemeContext.Provider>
    </>
  );
}

export default App;
