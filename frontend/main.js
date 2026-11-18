const gridElement = document.getElementById("grid");
let state = null;
let timer = null;
let busy = false;

const $ = id => document.getElementById(id);
const cellKey = p => `${p[0]},${p[1]}`;

async function api(url, method = "GET", body = undefined) {
  const options = { method, headers: { "Content-Type": "application/json" } };
  if (body !== undefined) options.body = JSON.stringify(body);
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

function setStatus(text) { $("status").textContent = text; }

function render(data) {
  state = data;
  const env = data.environment;
  const staticSet = new Set(env.static_obstacles.map(cellKey));
  const pathSet = new Set((data.path || []).map(cellKey));
  const dynamicMap = new Map(data.dynamic_obstacles.map(o => [cellKey(o.position), o]));
  gridElement.innerHTML = "";

  for (let r = 0; r < env.rows; r++) {
    for (let c = 0; c < env.cols; c++) {
      const p = [r, c], key = cellKey(p);
      const cell = document.createElement("button");
      cell.className = "cell";
      cell.type = "button";
      cell.title = `(${r}, ${c})`;
      if (pathSet.has(key)) cell.classList.add("path");
      if (staticSet.has(key)) cell.classList.add("wall");
      if (dynamicMap.has(key)) {
        cell.classList.add("dynamic");
        cell.title += ` · ${dynamicMap.get(key).name}`;
      }
      if (key === cellKey(env.goal)) cell.className = "cell goal";
      if (key === cellKey(data.robot.position)) cell.className = "cell robot";
      cell.addEventListener("click", () => toggleObstacle(p));
      gridElement.appendChild(cell);
    }
  }

  $("timeStep").textContent = data.time_step;
  $("replans").textContent = data.replanning_count;
  $("pathLength").textContent = data.path_length;
  $("nodes").textContent = data.total_nodes_explored;
  $("steps").textContent = data.steps_taken;
  $("position").textContent = `(${data.robot.position.join(", ")})`;
  $("event").textContent = data.event;
  setStatus(data.robot.reached_goal ? "Goal reached" : data.running ? "Running" : data.robot.status);

  $("obstacleList").innerHTML = "";
  data.dynamic_obstacles.forEach(o => {
    const item = document.createElement("div");
    item.className = "obstacle-item";
    const name = document.createElement("span");
    name.className = "obstacle-name";
    const swatch = document.createElement("i");
    swatch.className = "obstacle-swatch";
    swatch.style.background = o.color;
    name.append(swatch, document.createTextNode(o.name));
    const pos = document.createElement("span");
    pos.textContent = `(${o.position.join(", ")})`;
    item.append(name, pos);
    $("obstacleList").appendChild(item);
  });
}

async function refresh() { render(await api("/api/state")); }

async function toggleObstacle(position) {
  if (!state) return;
  const key = cellKey(position);
  if (key === cellKey(state.environment.start) || key === cellKey(state.environment.goal) ||
      key === cellKey(state.robot.position)) return;
  try {
    const isWall = state.environment.static_obstacles.some(p => cellKey(p) === key);
    const result = isWall
      ? await api("/api/obstacle", "DELETE", { position })
      : await api("/api/obstacle", "POST", { position });
    render(result);
  } catch (e) { alert(e.message); }
}

async function tick() {
  if (busy) return;
  busy = true;
  try {
    const data = await api("/api/step", "POST");
    render(data);
    if (data.robot.reached_goal || (!data.running && data.event.includes("No safe path"))) stopTimer();
  } catch (e) {
    stopTimer();
    alert(e.message);
  } finally { busy = false; }
}

function stopTimer() {
  if (timer) clearInterval(timer);
  timer = null;
}

$("startBtn").addEventListener("click", async () => {
  try {
    const data = await api("/api/start", "POST");
    render(data);
    stopTimer();
    timer = setInterval(tick, Number($("speed").value));
  } catch (e) { alert(e.message); }
});

$("pauseBtn").addEventListener("click", async () => {
  stopTimer();
  render(await api("/api/pause", "POST"));
  setStatus("Paused");
});

$("stepBtn").addEventListener("click", async () => {
  stopTimer();
  await tick();
});

$("resetBtn").addEventListener("click", async () => {
  stopTimer();
  try { render(await api("/api/reset", "POST", {})); }
  catch (e) { alert(e.message); }
});

$("speed").addEventListener("input", () => {
  $("speedValue").textContent = `${$("speed").value} ms`;
  if (timer) {
    stopTimer();
    timer = setInterval(tick, Number($("speed").value));
  }
});

$("applyBtn").addEventListener("click", async () => {
  stopTimer();
  const start = [Number($("startRow").value), Number($("startCol").value)];
  const goal = [Number($("goalRow").value), Number($("goalCol").value)];
  try {
    render(await api("/api/reset", "POST", {
      start, goal,
      static_obstacles: state.environment.static_obstacles
    }));
  } catch (e) { alert(e.message); }
});

refresh().catch(e => alert(e.message));
