import { useState } from 'react';

// to store and access the jwt token
export default function useToken() {
  const getToken = () => {
    const role = sessionStorage.getItem('role');
    const isLoggedIn = sessionStorage.getItem('isLoggedIn');
    const username = sessionStorage.getItem('username');
    return {
        "role": role,
        "isLoggedIn": isLoggedIn === "true",
        "username": username,
    }
  };
  const [token, setToken] = useState(getToken());

  const saveToken = userToken => {
    if (userToken){
      sessionStorage.setItem('role', userToken.role);
      sessionStorage.setItem('isLoggedIn', userToken.isLoggedIn);
      sessionStorage.setItem('username', userToken.username);
      setToken({
        "role": userToken.role,
        "isLoggedIn": userToken.isLoggedIn,
        "username": userToken.username,
      });
    }
  };

  return {
    setToken: saveToken,
    token
  }
}