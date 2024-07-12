import React from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ProviderSignup.css";

export const ProviderSignup = () => {
  
  const [name, setName] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/doclogin');
  }

  return (
      <div>
      <h1>Please Provide Accurate Information</h1>
      <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Enter your legal name" onChange={(e) => {setName(e.target.value)}}/>
      <input type="text" placeholder="Enter your email" onChange={(e) => {setEmail(e.target.value)}}/>
      <input type="text" placeholder="Enter your password" onChange={(e) => {setPassword(e.target.value)}}/>
      <button id="submit">Submit</button>
      </form>
    </div>
  );
};

