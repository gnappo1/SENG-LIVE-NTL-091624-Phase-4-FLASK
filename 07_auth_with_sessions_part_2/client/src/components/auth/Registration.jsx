import { useState, useEffect } from "react";
import { object, string } from "yup";
import { Formik } from "formik";
import styled from "styled-components";
import toast from "react-hot-toast";
import { useOutletContext, useNavigate } from "react-router-dom";

const signupSchema = object({
  username: string("username has to be a string")
    .max(25, "username must be 25 characters max")
    .required("username is required"),
  email: string("email has to be a string")
    .email("email must be valid")
    .max(80, "email must be 80 characters max")
    .required("email is required"),
  password: string("password has to be a string")
    .min(8, "password has to be at least 8 characters long")
    .max(25, "password must be 25 characters long max")
    .required("password is required"),
});

const signinSchema = object({
  email: string("email has to be a string")
    .email("email must be valid")
    .max(80, "email must be 80 characters max")
    .required("email is required"),
  password: string("password has to be a string")
    .min(10, "password has to be at least 10 characters long")
    .max(20, "password must be 20 characters long max")
    .required("password is required"),
});

const Registration = () => {
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate();

  return (
    <div>
      <h2>Please Log in or Sign Up</h2>
      <h3>{isLogin ? "Not a Member?" : "Already a member?"}</h3>
      <button onClick={() => setIsLogin((current) => !current)}>
        {isLogin ? "Register Now!" : "Login!"}
      </button>
      <Form>
        {!isLogin && (
          <>
            <label htmlFor="username">Username</label>
            <input type="text" name="username" />
          </>
        )}
        <label htmlFor="email">Email</label>
        <input type="email" name="email" />
        <label htmlFor="password">Password</label>
        <input type="password" name="password" />

        <input type="submit" value={isLogin ? "Login!" : "Create Account!"} />
      </Form>
    </div>
  );
};

export default Registration;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 400px;
  margin: auto;
  font-family: Arial;
  font-size: 30px;
  input[type="submit"] {
    background-color: #42ddf5;
    color: white;
    height: 40px;
    font-family: Arial;
    font-size: 30px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
`;
