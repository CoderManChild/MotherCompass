import React from "react";
import './Signup.css';
import {useState} from 'react';
import { useNavigate } from "react-router-dom";

export const Signup = () => {
  const [name, setName] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [age, setAge] = useState();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/');
  }

  return (
    <div>
      <h1>Please Provide the Following Information About Your Child</h1>
      <div id="form">
      <input type="text" placeholder="Enter your child's gender" />
      <input type="text" placeholder="Enter your child's expected month of birth" />
      <input type="text" placeholder="First Child Y/N" />
      </div>
      <h1>Please Provide the Following Information About Yourself</h1>

      <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Enter your name" value={name} onChange={(e) => {setName(e.target.value)}}/>
      <input type="text" placeholder="Enter your email" value={email} onChange={(e) => {setEmail(e.target.value)}} />
      <input type="text" placeholder="Enter your password" value={password} onChange={(e) => {setPassword(e.target.value)}}/>
      <input type="text" placeholder="Enter your age" value={age} onChange={(e) => {setAge(e.target.value)}}/>
      <button id="submit">Submit</button>
      </form>
    </div>
  )
};
