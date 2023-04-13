import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import { ToastContainer } from "react-toastify";
import MainLayout from "components/shared/UI/layouts/MainLayout";
import RegisterPage from "pages/register.page";
import LoginPage from "pages/login.page";
import HomePage from "pages/home.page";
import UnauthorizePage from "pages/unauthorize.page";
import RequireUser from "components/features/requireUser";
import AdminPage from "pages/admin.page";
function App() {
  return (
    <>
      <ToastContainer />
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<HomePage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route element={<RequireUser allowedRoles={["user"]} />}>
              <Route path="admin" element={<AdminPage />} />
            </Route>
            <Route path="unauthorized" element={<UnauthorizePage />} />
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
