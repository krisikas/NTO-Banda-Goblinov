// ээээээ хз зачем написал на JS мб чисто попробывать
const map = document.getElementById('map');
for (let y = 0; y < 10; y++) {
  const row = document.createElement('div');
  row.classList.add('setka-row')
  for (let x = 0; x < 10; x++) {
    const cell = document.createElement('div');
    cell.classList.add('setka-kletka');
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






// ===== Socket =====

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
  addVrez(data);
});


// координаты дрона вроде 0 баллов
function updateDronePosition(x, y) {
  document.getElementById('drone-x').textContent = `x: ${y.toFixed(3)}`;
  document.getElementById('drone-y').textContent = `y: ${-x.toFixed(3)}`;
}


// /
let vrezCount = 0
function addVrez(tubes) {
  const list = document.getElementById('vrez-list');
  // console.log(vrezCount.cnt, tubes, tubes.length)
  for(; vrezCount < tubes.length; vrezCount++) {
    drawVrez(tubes[vrezCount].x, tubes[vrezCount].y, tubes[vrezCount].angle)

    const item = document.createElement('li');
    item.textContent = `${vrezCount+1}. x: ${tubes[vrezCount].x.toFixed(3)}, y: ${tubes[vrezCount].y.toFixed(3)}, angle: ${tubes[vrezCount].angle.toFixed(3)}`;
    item.style.marginBottom = '8px';
    item.style.fontSize = '0.95em';
    list.appendChild(item);
  }
}

function drawVrez (x, y, angle) {
  const cx = 100*(x)
  const cy = 100*(y+4)
  const bDeg = angle * 180 / Math.PI

  const DVrez = document.createElement('div');
  DVrez.style.position = 'absolute';
  DVrez.style.left = cx + 'px';
  DVrez.style.bottom = cy + 'px';
  DVrez.style.transform = `rotate(${bDeg}deg)`;
  DVrez.classList.add('vrez')
  document.getElementById('map').appendChild(DVrez);
}
