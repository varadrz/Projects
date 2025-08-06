import React, { useState } from "react";

function numToWords(num) {
  // For 1–90; full mapping recommended
  const ones = [
    "", "one","two","three","four","five","six","seven","eight","nine","ten",
    "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"
  ];
  const tens = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"];
  if(num < 20) return ones[num];
  if(num % 10 === 0) return tens[Math.floor(num/10)];
  if(num < 100) return tens[Math.floor(num/10)] + "-" + ones[num%10];
  return String(num);
}

function speakNumber(num) {
  const msg = new window.SpeechSynthesisUtterance(numToWords(num));
  window.speechSynthesis.speak(msg);
}

function NumberPicker() {
  const [picked, setPicked] = useState([]);
  const [current, setCurrent] = useState(null);

  const pickNumber = () => {
    if(picked.length === 90) return;
    let n;
    do {
      n = Math.floor(Math.random()*90) + 1;
    } while (picked.includes(n));
    setPicked([...picked, n]);
    setCurrent(n);
    speakNumber(n);
  };

  return (
    <div className="picker-container">
      <h2>Number Picker</h2>
      <button onClick={pickNumber} disabled={picked.length===90}>
        Pick Next Number
      </button>
      {current && (
        <div className="current-number animate-pop">
          {current}
        </div>
      )}
      <div>
        <h3>History:</h3>
        <div className="history-grid">
          {picked.map((n, idx) => (
            <span key={idx}>{n}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default NumberPicker;
