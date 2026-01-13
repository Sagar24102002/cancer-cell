import React from 'react'
import PatientsList from './components/PatientsList'

export default function App(){
  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h1>Cancer Database</h1>
      <PatientsList />
    </div>
  )
}
