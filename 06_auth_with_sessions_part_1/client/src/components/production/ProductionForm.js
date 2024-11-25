import React, { useState } from "react";
import styled from "styled-components";
import { useNavigate, useOutletContext } from "react-router-dom";
import * as yup from "yup";
import { Formik } from "formik";
import toast from "react-hot-toast";
// 6.✅ Verify formik and yet have been added to our package.json dependencies
// import the useFormik hook or the Formik component from formik
// import * as yup for yup
const productionSchema = yup.object().shape({
  title: yup.string()
    .min(2, "Titles must be at least 2 chars long")
    .max(80, "Titles must be 80 chars long max")
    .required("Title is required"),
  genre: yup.string()
    .oneOf(["Drama", "Musical", "Opera"])
    .required("Genre has to be one of Drama, Musical, Opera"),
  budget: yup.number()
    .positive("Budget has to be a positive integer")
    .max(10000000, "Budget must be 50 chars long max")
    .required("Budget has to be a positive float under 10Millions"),
  image: yup.string()
    .test("is-url", "Images must have a valid url ending with jpg, jpeg, png", (value) => {
      const urlRegex = /(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|jpeg|png)/g;
      return urlRegex.test(value)
    })
    .required("Image is required"),
  director: yup.string()
    .required("Director is required"),
  description: yup.string()
    .min(30, "Description should be at least 10 chars")
    .max(500, "Description should be 10000 chars max")
    .required("Description is required")
})

const initialValues = {
  title: "",
  genre: "",
  budget: "",
  image: "",
  director: "",
  description: "",
  ongoing: false
}

function ProductionForm() {
  const { addProduction } = useOutletContext();

  const navigate = useNavigate();

  // 7.✅ Use yup to create client side validations

  // 9.✅ useFormik hook or <Formik> component

  return (
    <div className="App">
      <Formik
        initialValues={initialValues}
        onSubmit={async (values) => {
          const resp = await fetch("/api/v1/productions", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify({...values, budget: parseFloat(values.budget)})
          })
          const data = await resp.json()
          debugger
          if (resp.ok) {
            toast.success(`Successfully created production called ${data.title}`)
            //! add the new production to the state variable called productions
            addProduction(data)
            navigate("/")
          } else {
            toast.error(data.error)
          }
        }}
        validationSchema={productionSchema}
      >
        {({values, errors, touched, handleChange, handleSubmit, handleBlur, isSubmitting}) => (
          <Form onSubmit={handleSubmit}>
            <label>Title </label>
            <input type="text" name="title" onChange={handleChange} value={values.title} onBlur={handleBlur}/>
            {errors.title && touched.title ? <div id="error-message show">{errors.title}</div>: null}

            <label> Genre</label>
            <input type="text" name="genre" onChange={handleChange} value={values.genre} onBlur={handleBlur} />
            {errors.genre && touched.genre ? <div id="error-message show">{errors.genre}</div> : null}

            <label>Budget</label>
            <input type="text" name="budget" onChange={handleChange} value={values.budget} onBlur={handleBlur} />
            {errors.budget && touched.budget ? <div id="error-message show">{errors.budget}</div> : null}

            <label>Image</label>
            <input type="text" name="image" onChange={handleChange} value={values.image} onBlur={handleBlur} />
            {errors.image && touched.image ? <div id="error-message show">{errors.image}</div> : null}

            <label>Director</label>
            <input type="text" name="director" onChange={handleChange} value={values.director} onBlur={handleBlur} />
            {errors.director && touched.director ? <div id="error-message show">{errors.director}</div> : null}

            <label>Description</label>
            <textarea type="text" rows="4" cols="50" name="description" onChange={handleChange} value={values.description} onBlur={handleBlur} />
            {errors.description && touched.description ? <div id="error-message show">{errors.description}</div> : null}

            <input type="submit" />
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default ProductionForm;

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
