const socket = io();
  
socket.on("connect", () => {
  console.log("Connected to Socket.IO server");
  document.getElementById('mission-status').textContent = 'подключено';
});

socket.on("pos", (data) => {
  // data = {x: float, y: float, z: float}
//   console.log("Received pos:", data);
  updateDronePosition(data.x, data.y);
});

socket.on("tubes", (data) => {
  // data = массив (какая труба, координаты от начала )
  console.log("Received tubes:", data);
  

  
  // Добавляем врезки в список
  addVrezToList(data);
});


// координаты дрона вроде 0 баллов
function updateDronePosition(x, y) {
  document.getElementById('drone-x').textContent = `x: ${x}`;
  document.getElementById('drone-y').textContent = `y: ${y}`;
}


// ээээээ хз зачем написал на JS мб чисто попробывать
const map = document.getElementById('map');
for (let y = 0; y < 10; y++) {
  const row = document.createElement('div');
  row.style.display = 'flex';
  row.style.margin = '0';
  for (let x = 0; x < 10; x++) {
    const cell = document.createElement('div');
    cell.style.width = '100px';
    cell.style.height = '100px';
    cell.style.border = '1px solid #bbb';
    cell.style.boxSizing = 'border-box';
    cell.style.background = '#ffffff';
    cell.style.margin = '0';
    row.appendChild(cell);
  }
  map.appendChild(row);
}









// книпки управления миссией 2 балла --------СЮДА и статус миссиииии
function start() {
  console.log('start');
  fetch('/api/start')
    .then(() => {
      document.querySelector('.start-btn').classList.add('active');
      document.querySelector('.stop-btn').classList.remove('active');
      document.querySelector('.kill-btn').classList.remove('active');
      document.getElementById('mission-status').textContent = 'выполняется';
    });
}

function stop() {
  console.log('stop');
  fetch('/api/stop')
    .then(() => {
      document.querySelector('.stop-btn').classList.add('active');
      document.querySelector('.start-btn').classList.remove('active');
      document.querySelector('.kill-btn').classList.remove('active');
      document.getElementById('mission-status').textContent = 'остановлено';
    });
}

function kill() {
  console.log('kill');
  fetch('/api/kill')
    .then(() => {
      document.querySelector('.kill-btn').classList.add('active');
      document.querySelector('.start-btn').classList.remove('active');
      document.querySelector('.stop-btn').classList.remove('active');
      document.getElementById('mission-status').textContent = 'аварийная остановка';
    });
}

// /
let vrezCount = 0
function addVrezToList(tubes) {
  const list = document.getElementById('vrez-list');
  // console.log(vrezCount.cnt, tubes, tubes.length)
  for(; vrezCount < tubes.length; vrezCount++) {
    const item = document.createElement('li');
    item.textContent = `${vrezCount+1}. x: ${tubes[vrezCount].x}, y: ${tubes[vrezCount].y}, angle: ${tubes[vrezCount].angle}`;
    item.style.marginBottom = '8px';
    item.style.fontSize = '0.95em';
    list.appendChild(item);
  }
}

function drawVrez (x, y, angle) {
  const cx = 100*(x+1)
  const cy = 100*(y)
  const bDeg = angle * Math.PI / 180

  const DVrez = document.createElement('div');
  DVrez.style.position = 'absolute';
  DVrez.style.left = cx + 'px';
  DVrez.style.top = cy + 'px';
  DVrez.style.width = '250px';
  DVrez.style.height = '10px';
  DVrez.style.background = "#ff0000";
  DVrez.style.borderRadius = "10px";
  DVrez.style.transformOrigin = 'left center';
  DVrez.style.transform = `rotate(${bDeg}deg)`;
  DVrez.style.zIndex = '999';
  document.getElementById('map').appendChild(DVrez);
}
    drawVrez(4, 1, 0)
