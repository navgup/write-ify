
import React, { useEffect, useState } from 'react'
import axios from "axios"
import store from './store'
import "./api.css"

 export const Login = () => {

    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const handleLogin = () => {
      // Redirect the user to the Flask endpoint for Spotify authorization
      window.location.href = 'https://writify.azurewebsites.net/login';
    };
  
  
    return (
      <div>
        <button className="button" onClick={handleLogin}>Login with Spotify</button>
        {isLoggedIn && <p>Getting data from Flask...</p>}
      </div>
    );
  };
  
 
  const setAuthToken = (token) => {
    store.dispatch({type: "SET_AUTH_TOKEN", token})
  }

  export {setAuthToken}
  


