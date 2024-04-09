import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Routing from "./Routing";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <div className="container mx-auto">
      <Routing />
    </div>
  </React.StrictMode>
);
