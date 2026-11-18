from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
from simulator import Simulator

ROOT = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_folder=str(ROOT / "frontend"), static_url_path="")
simulator = Simulator()

@app.get("/")
def index():
    return send_from_directory(ROOT / "frontend", "index.html")

@app.get("/api/state")
def state():
    return jsonify(simulator.snapshot())

@app.post("/api/start")
def start():
    simulator.start()
    return jsonify(simulator.snapshot())

@app.post("/api/pause")
def pause():
    simulator.pause()
    return jsonify(simulator.snapshot())

@app.post("/api/step")
def step():
    return jsonify(simulator.step())

@app.post("/api/reset")
def reset():
    data = request.get_json(silent=True) or {}
    try:
        simulator.reset(data)
        return jsonify(simulator.snapshot())
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400

@app.post("/api/obstacle")
def add_obstacle():
    data = request.get_json(force=True)
    position = tuple(data.get("position", []))
    if len(position) != 2:
        return jsonify({"error": "Position must be [row, col]."}), 400
    if simulator.environment.add_obstacle(position):
        simulator.running = False
        simulator.replanner.plan(simulator.environment, simulator.robot, simulator.obstacles)
        simulator.last_event = f"Static obstacle added at {position}"
        return jsonify(simulator.snapshot())
    return jsonify({"error": "Invalid position or Start/Goal cell."}), 400

@app.delete("/api/obstacle")
def remove_obstacle():
    data = request.get_json(force=True)
    position = tuple(data.get("position", []))
    simulator.environment.remove_obstacle(position)
    simulator.replanner.plan(simulator.environment, simulator.robot, simulator.obstacles)
    simulator.last_event = f"Static obstacle removed at {position}"
    return jsonify(simulator.snapshot())

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
