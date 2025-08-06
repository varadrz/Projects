import React from 'react';
import './App.css';
import Header from './Header';

function App() {
  return (
    // BEM (BEM = Block Element Modifier) Convention
    <div className="App">
      <h1>Hello Everyone! Let's build the Amazon Store!</h1>
      <Header/>
      {/*Home*/}
    </div>
  );
}

export default App;
