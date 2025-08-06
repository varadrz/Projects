import React, { useState } from "react";
import TicketGenerator from "./TicketGenerator";
import NumberPicker from "./NumberPicker";
import './styles.css';

function App() {
  return (
    <div className="app">
      <h1>Smart & Vibrant Tambola</h1>
      <TicketGenerator />
      <NumberPicker />
    </div>
  );
}

export default App;
