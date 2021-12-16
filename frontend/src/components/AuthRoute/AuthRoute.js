import React from "react";
import { Redirect, Route } from "react-router";

export default function AuthRoute( props ){
    const { token, type, path, rolesAllowed } = props;
    const { isLoggedIn, role } = token;

    if (!isLoggedIn && type === "PRIVATE") {
        return <Redirect to="/" />;
    } else if (isLoggedIn && path === "/login") {
        return <Redirect to="/dashboard" />;
    } else if (type === "PRIVATE" && isLoggedIn) {
        let accessIsDenied = true;
        for (let i = 0; i < rolesAllowed.length; i ++) {
            if (rolesAllowed[i] === role) {
                accessIsDenied = false;
                break;
            }
        }

        if (accessIsDenied) {
            return <Redirect to="/" />;
        }
    }

    return <Route {...props} />;
}