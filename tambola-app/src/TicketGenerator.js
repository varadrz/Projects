import React, { useState } from "react";

// Ticket generation helper (simplified)
function generateTicket() {
  // Each col: numbers, then shuffled, then filled into ticket with blank logic.
  const grid = Array(3).fill().map(() => Array(9).fill(""));
  // Prepare number pools
  const numPools = [];
  for (let c = 0; c < 9; c++) {
    const start = c * 10 + 1;
    const end = c === 8 ? 90 : (c + 1) * 10;
    const pool = [];
    for (let n = start; n <= end; n++) pool.push(n);
    // Shuffle
    numPools.push(pool.sort(()=>Math.random()-0.5));
  }
  // Fill 5 numbers per row (total 15 on ticket)
  for (let r = 0; r < 3; r++) {
    let numsIdx = [...Array(9).keys()].sort(() => Math.random() - 0.5).slice(0, 5);
    numsIdx.forEach(c => {
      grid[r][c] = numPools[c].pop() || "";
    });
  }
  return grid;
}

function TicketGenerator() {
  const [tickets, setTickets] = useState([]);
  const generateTickets = (n) => {
    const t = [];
    for (let i = 0; i < n; i++) t.push(generateTicket());
    setTickets(t);
  };

  return (
    <div>
      <h2>Your Tambola Tickets</h2>
      <button onClick={() => generateTickets(6)}>Generate 6 Tickets</button>
      <div className="ticket-list">
        {tickets.map((ticket, idx) => (
          <table key={idx} className="ticket">
            <tbody>
            {ticket.map((row, ridx) => (
              <tr key={ridx}>
                {row.map((cell, cidx) => (
                  <td key={cidx} className={cell ? "filled" : "blank"}>{cell}</td>
                ))}
              </tr>
            ))}
            </tbody>
          </table>
        ))}
      </div>
    </div>
  );
}

export default TicketGenerator;
