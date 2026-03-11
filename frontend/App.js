import React, { useState } from "react";

function App() {

  const [file, setFile] = useState(null)
  const [email, setEmail] = useState("")
  const [message, setMessage] = useState("")

  const uploadFile = async () => {

    const formData = new FormData()
    formData.append("file", file)
    formData.append("email", email)

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData
    })

    const data = await res.json()

    setMessage(data.summary)
  }

  return (

    <div style={{padding:"40px"}}>

      <h2>Sales Insight Automator</h2>

      <input
        type="file"
        onChange={(e)=>setFile(e.target.files[0])}
      />

      <br/><br/>

      <input
        type="email"
        placeholder="Enter Email"
        onChange={(e)=>setEmail(e.target.value)}
      />

      <br/><br/>

      <button onClick={uploadFile}>
        Generate Summary
      </button>

      <p>{message}</p>

    </div>

  )
}

export default App