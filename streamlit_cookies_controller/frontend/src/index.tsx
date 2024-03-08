/*
author: Nathan Chen
date  : 08-Mar-2024
*/


import React from "react";
import { createRoot } from "react-dom/client";
import CookieController from "./cookies_controller";


const container = document.getElementById('root');
const root = createRoot(container!);

root.render(
    <React.StrictMode>
        <CookieController/>
    </React.StrictMode>
);