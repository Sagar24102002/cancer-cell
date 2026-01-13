import React, {useEffect, useState} from 'react'

export default function PatientsList(){
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    fetch('http://localhost:8000/api/patients/')
      .then(res=>res.json())
      .then(data=>{ setPatients(data); setLoading(false) })
      .catch(err=>{ console.error(err); setLoading(false) })
  },[])

  if(loading) return <div>Loading patients...</div>

  return (
    <div>
      {patients.length===0 && <div>No patients found.</div>}
      <ul>
        {patients.map(p => (
          <li key={p.id}>{p.first_name} {p.last_name} — {p.diagnosis || 'No diagnosis'}</li>
        ))}
      </ul>
    </div>
  )
}
