import React from "react";
import "./ProviderLogin.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const ProviderLogin = () => {

  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const navigate = useNavigate();
  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/main')
  }

  return (
    <div>
      <div>
      <h1 id="doctext">Welcome Back Doctor!</h1>
      </div>
        <form onSubmit={handleSubmit}>
        <label id="email">email</label>
      <input type="text" placeholder="Enter your email" value={email} onChange={(e) => {setEmail(e.target.value)}}/>
      <label id="pass">password</label>
      <input type="password" placeholder="Enter your password" value={password} onChange={(e) => {setPassword(e.target.value)}}/>
      <button id="login">Login</button>
        </form>
    </div>
  );
};
