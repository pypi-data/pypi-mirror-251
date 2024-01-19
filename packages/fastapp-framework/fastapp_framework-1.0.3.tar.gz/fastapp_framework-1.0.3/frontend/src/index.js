import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import App from './pages/App';
import Login from './pages/login/LoginView';
import AdminView from './pages/admin/AdminView';
import About from './pages/About';
import ResetPassword from './pages/ResetPassword';
import NotFound from './pages/NotFound';

import './components/popup.css'


const router = createBrowserRouter([
  {
    path: "/",
    element: <App />
  },
  {
    path: "/login",
    element: <Login />
  },
  {
    path: "/admin",
    element: <AdminView />
  },
  {
    path: "/about",
    element: <About />
  },
  {
    path: "/reset-password",
    element: <ResetPassword />
  },  
  {
    path: "*",
    element: <NotFound />
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);