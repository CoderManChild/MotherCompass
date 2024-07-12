import React from "react";
import './Home.css';
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export const Home = () => {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const navigate = useNavigate();
  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/main')
  }
  return (
        <form onSubmit={handleSubmit}>
        <label id="email">email</label>
      <input type="text" placeholder="Enter your email" value={email} onChange={(e) => {setEmail(e.target.value)}}/>
      <label id="pass">password</label>
      <input type="password" placeholder="Enter your password" value={password} onChange={(e) => {setPassword(e.target.value)}}/>
      <button id="login">Login</button>
        </form>
  )
};
