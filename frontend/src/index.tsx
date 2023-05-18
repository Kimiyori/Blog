import React from "react";
import { createRoot } from "react-dom/client";
import { StyledEngineProvider } from "@mui/material/styles";
import { CookiesProvider } from "react-cookie";
import { Provider } from "react-redux";
import { setupStore } from "./app/store";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import AuthMiddleware from "components/features/AuthMiddleware";

const container = document.getElementById("root")!;
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <Provider store={setupStore()}>
      <CookiesProvider>
        <AuthMiddleware>
          <StyledEngineProvider injectFirst>
            <App />
          </StyledEngineProvider>
        </AuthMiddleware>
      </CookiesProvider>
    </Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
