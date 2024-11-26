import { useState, useEffect } from "react";
import { object, string } from "yup";
import { Formik } from "formik";
import styled from "styled-components";
import toast from "react-hot-toast";
import { useOutletContext, useNavigate } from "react-router-dom";

const signupSchema = object({
  username: string("username has to be a string")
    .max(20, "username must be 20 characters max")
    .required("username is required"),
  email: string("email has to be a string")
    .email("email must be valid")
    .max(80, "email must be 80 characters max")
    .required("email is required"),
  password: string("password has to be a string")
    .min(10, "password has to be at least 10 characters long")
    .max(20, "password must be 20 characters long max")
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

const initialValues = {
  username: "",
  email: "",
  password: "",
}

const Registration = () => {
  const [isLogin, setIsLogin] = useState(true);
  const { currentUser, updateUser } = useOutletContext();
  const navigate = useNavigate();

  useEffect(() => {
    if (currentUser) {
      navigate("/");
    }
  }, [currentUser, navigate]);

  return (
    <div>
      <h2>Please Log in or Sign Up</h2>
      <h3>{isLogin ? "Not a Member?" : "Already a member?"}</h3>
      <button onClick={() => setIsLogin((current) => !current)}>
        {isLogin ? "Register Now!" : "Login!"}
      </button>
      <Formik
        initialValues={initialValues}
        onSubmit={async (values) => {
          const url = isLogin ? "/api/v1/login" : "/api/v1/signup"
          const resp = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json",
            },
            body: JSON.stringify(values)
          });
          const data = await resp.json()
          if (resp.ok) { //200-299
            toast.success(
              isLogin
                ? `Welcome back ${data.username}`
                : `Welcome ${data.username}`
            );
            //! what do we do with the user???
            updateUser(data);
            navigate("/")
          } else {
            toast.error(data.error)
          }
        }}
        validationSchema={isLogin ? signinSchema : signupSchema}
      >
        {({
          handleBlur,
          handleChange,
          handleSubmit,
          values,
          errors,
          touched,
          isSubmitting,
        }) => (
          <Form onSubmit={handleSubmit}>
            {!isLogin && (
              <>
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  name="username"
                  onChange={handleChange}
                  onBlur={handleBlur}
                  value={values.username}
                />
                {errors.username && touched.username && (
                  <div className="error-message show">{errors.name}</div>
                )}
              </>
            )}
            <label htmlFor="email">Email</label>
            <input
              type="email"
              name="email"
              onChange={handleChange}
              onBlur={handleBlur}
              value={values.email}
            />
            {errors.email && touched.email && (
              <div className="error-message show">{errors.email}</div>
            )}

            <label htmlFor="password">Password</label>
            <input
              type="password"
              name="password"
              onChange={handleChange}
              onBlur={handleBlur}
              value={values.password}
            />
            {errors.password && touched.password && (
              <div className="error-message show">{errors.password}</div>
            )}

            <input
              type="submit"
              value={isLogin ? "Login!" : "Create Account!"}
            />
          </Form>
        )}
      </Formik>
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
