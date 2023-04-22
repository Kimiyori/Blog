import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "components/shared/UI/navigations/MainNavigation/MainNavigation";
import "styles/layout/main_layout.scss";
export default function MainLayout() {
  return (
    <>
      <div className="main_layout">
        <Navbar />
        <nav></nav>
        <section>
          <Outlet />
        </section>
        <aside></aside>
        {/* <footer></footer> */}
      </div>
    </>
  );
}
