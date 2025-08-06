const ticketContainer = document.getElementById("tickets");
const submitCountBtn = document.getElementById("submitCount");
const generateBtn = document.getElementById("generateTickets");
const nameInputs = document.getElementById("nameInputs");
const pickBtn = document.getElementById("pick");
const currentDisplay = document.getElementById("current");
const historyGrid = document.getElementById("historyGrid");
const allPickedMsg = document.getElementById("done");
const congratsBanner = document.getElementById("congrats");
const gameControls = document.getElementById("gameControls");

let players = [];
let tickets = [];
let numberPool = Array.from({ length: 90 }, (_, i) => i + 1);
let calledNumbers = [];
let wins = {
  earlyFive: null,
  topLine: null,
  middleLine: null,
  bottomLine: null,
  fullHouse: null
};

submitCountBtn.addEventListener("click", () => {
  const count = parseInt(document.getElementById("playerCount").value);
  nameInputs.innerHTML = "";
  ticketContainer.innerHTML = "";
  document.getElementById("gameControls").style.display = "none";

  if (!count || count < 1 || count > 6) return;

  for (let i = 0; i < count; i++) {
    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = `Player ${i + 1} Name`;
    input.required = true;
    nameInputs.appendChild(input);
  }

  generateBtn.style.display = "inline-block";
});

generateBtn.addEventListener("click", () => {
  const inputs = nameInputs.querySelectorAll("input");
  players = Array.from(inputs).map(input => input.value.trim() || "Player");
  ticketContainer.innerHTML = "";
  tickets = [];
  numberPool = Array.from({ length: 90 }, (_, i) => i + 1);
  calledNumbers = [];
  historyGrid.innerHTML = "";
  currentDisplay.textContent = "";
  allPickedMsg.style.display = "none";
  wins = {
    earlyFive: null,
    topLine: null,
    middleLine: null,
    bottomLine: null,
    fullHouse: null
  };

  players.forEach((name, index) => {
    const ticket = generateTicket();
    tickets.push({ name, ticket, marks: 0, top: false, mid: false, bot: false });
    const wrapper = document.createElement("div");
    wrapper.className = "ticket-wrapper";
    const label = document.createElement("div");
    label.className = "ticket-label";
    label.textContent = name;
    const table = buildTicketUI(ticket, index);
    wrapper.appendChild(table);
    wrapper.appendChild(label);
    ticketContainer.appendChild(wrapper);
  });

  pickBtn.disabled = false;
  gameControls.style.display = "block";
});

// Ticket generation
function generateTicket() {
  const ticket = Array.from({ length: 3 }, () => Array(9).fill(""));
  let usedCols = Array.from({ length: 9 }, () => []);

  for (let row = 0; row < 3; row++) {
    const cols = shuffle([...Array(9).keys()]).slice(0, 5).sort((a, b) => a - b);
    cols.forEach(col => {
      let num;
      do {
        num = col === 0 ? getRandom(1, 9) : getRandom(col * 10, col * 10 + 9);
      } while (usedCols[col].includes(num));
      usedCols[col].push(num);
      ticket[row][col] = num;
    });
  }
  return ticket;
}

function buildTicketUI(ticket, ticketIndex) {
  const table = document.createElement("table");
  table.className = "ticket";

  ticket.forEach((row, rowIndex) => {
    const tr = document.createElement("tr");
    row.forEach((cell, colIndex) => {
      const td = document.createElement("td");
      if (cell === "") {
        td.className = "blank";
      } else {
        td.textContent = cell;
        td.setAttribute("data-number", cell);
        td.setAttribute("data-player", ticketIndex);
        td.setAttribute("data-row", rowIndex);
      }
      tr.appendChild(td);
    });
    table.appendChild(tr);
  });

  return table;
}

pickBtn.addEventListener("click", pickNumber);

function pickNumber() {
  if (numberPool.length === 0) {
    allPickedMsg.style.display = "block";
    return;
  }

  const i = Math.floor(Math.random() * numberPool.length);
  const number = numberPool.splice(i, 1)[0];
  calledNumbers.push(number);

  currentDisplay.textContent = number;

  // 🗣 Speak the number
  speakNumber(number);

  const cells = document.querySelectorAll(`[data-number="${number}"]`);
  cells.forEach(cell => {
    cell.classList.add("crossed");
    const playerIndex = parseInt(cell.getAttribute("data-player"));
    const row = parseInt(cell.getAttribute("data-row"));
    checkWin(playerIndex, row);
  });

  const numSpan = document.createElement("span");
  numSpan.textContent = number;
  historyGrid.appendChild(numSpan);

  if (numberPool.length === 0) {
    pickBtn.disabled = true;
    allPickedMsg.style.display = "block";
  }
}

function checkWin(playerIndex, row) {
  const t = tickets[playerIndex];
  const cells = document.querySelectorAll(`[data-player="${playerIndex}"]`);
  let markCount = 0;
  const rowHits = [[], [], []];

  cells.forEach(cell => {
    const r = parseInt(cell.getAttribute("data-row"));
    const crossed = cell.classList.contains("crossed");
    if (crossed) {
      markCount++;
      rowHits[r].push(cell);
    }
  });

  // Early Five
  if (!wins.earlyFive && markCount >= 5) {
    wins.earlyFive = t.name;
    showBadge(playerIndex, "Early Five Winner 🎉");
  }

  // Horizontal Lines
  ["top", "mid", "bot"].forEach((line, i) => {
    if (!t[line] && rowHits[i].length === 5) {
      t[line] = true;
      if (!wins[line + "Line"]) {
        wins[line + "Line"] = t.name;
        showBadge(playerIndex, `${capitalize(line)} Line Winner 🏆`);
      }
    }
  });

  // Full House
  if (!wins.fullHouse && markCount === 15) {
    wins.fullHouse = t.name;
    showCongrats(t.name);
    pickBtn.disabled = true;
  }
}

function showBadge(index, text) {
  const wrappers = document.querySelectorAll(".ticket-wrapper");
  const badge = document.createElement("div");
  badge.className = "win-badge";
  badge.textContent = text;
  wrappers[index].appendChild(badge);
}

function showCongrats(name) {
  congratsBanner.textContent = `🎉 Congratulations ${name}! You won Full House! 🎉`;
  congratsBanner.style.display = "block";
}

// 🔊 Voice Announcer
function speakNumber(number) {
  if ('speechSynthesis' in window) {
    const msg = new SpeechSynthesisUtterance(number.toString());
    msg.pitch = 1;
    msg.rate = 1;
    msg.lang = 'en-IN'; // Indian accent, or use 'en-US' for American
    window.speechSynthesis.cancel(); // clear any ongoing speech
    window.speechSynthesis.speak(msg);
  }
}

// Utility functions
function shuffle(arr) {
  return arr.sort(() => Math.random() - 0.5);
}

function getRandom(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}
