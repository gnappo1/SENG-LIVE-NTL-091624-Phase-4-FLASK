import  {useParams, useNavigate } from 'react-router-dom'
import {useEffect, useState} from 'react'
import styled from 'styled-components'
import { useOutletContext } from 'react-router-dom'
import toast from 'react-hot-toast'

function ProductionDetail() {
  const [production, setProduction] = useState({crew_members:[]})
  // const [error, setError] = useState(null)
  const { handleEdit, deleteProduction } = useOutletContext()

  //Student Challenge: GET One 
  const { productionId } = useParams()
  const navigate = useNavigate()

  useEffect(()=>{
    (async () => {
      const resp = await fetch(`/api/v1/productions/${productionId}`)
      const data = await resp.json()
      if (resp.ok) {
        setProduction(data)
      } else {
        toast.error(data.error)
      }
    })()
  }, [productionId])

  const handleDelete = async () => {
    const resp = await fetch(`/api/v1/productions/${productionId}`, {
      method: "DELETE"
    })
    if (resp.ok) {
      // #! what do we do now that the production has been deleted?
      toast.success(`Successfully deleted Production with id ${productionId}`)
      // #! we need to remove the deleted production from the productions state variable inside App.jsx
      deleteProduction(productionId)
      navigate("/")
    } else {
      const data = await resp.json()
      toast.error(data.error)
    }
  }

  
  const {id, title, genre, image,description, crew_members} = production 
  // if(error) return <h2>{error}</h2>
  return (
      <CardDetail id={id}>
        <h1>{title}</h1>
          <div className='wrapper'>
            <div>
              <h3>Genre:</h3>
              <p>{genre}</p>
              <h3>Description:</h3>
              <p>{description}</p>
              <h2>Cast Members</h2>
              <ul>
                {crew_members.map(cast => <li key={cast.id}>{`${cast.role} : ${cast.name}`}</li>)}
              </ul>
            </div>
            <img src={image} alt={title}/>
          </div>
      <button onClick={handleEdit} >Edit Production</button>
      <button onClick={handleDelete} >Delete Production</button>

      </CardDetail>
    )
  }
  
  export default ProductionDetail
  const CardDetail = styled.li`
    display:flex;
    flex-direction:column;
    justify-content:start;
    font-family:Arial, sans-serif;
    margin:5px;
    h1{
      font-size:60px;
      border-bottom:solid;
      border-color:#42ddf5;
    }
    .wrapper{
      display:flex;
      div{
        margin:10px;
      }
    }
    img{
      width: 300px;
    }
    button{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
    }
  `