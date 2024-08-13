import { useEffect, useState } from 'react'

function App() {
  const[query,setquery]=useState()
  const[reply,setreply]=useState("")
  const[loading,setloading]=useState(false)
  const handlechange=(e:any)=>{
    setquery(e.target.value)
  }
  const handlesubmit=()=>{
    setloading(true)
    call()
    setloading(false)
  }
  const call=async ()=>{
    const response= await fetch('http://127.0.0.1:8000/query',{
      method:'Post',
      headers:{
        'Content-Type':'application/json'
      },
      body:JSON.stringify({'query':query})
    })
    const r=await response.json()
    console.log(r)
    setreply(r)
  }
  return (
    <>
    <input onChange={handlechange}/>
    <button onClick={handlesubmit}>Submit</button>
    <p>{reply}</p>
    </>
  )
}

export default App
