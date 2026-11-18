# Robot_Navgation_in_Dynamic_Environments
A* Search and Replanning in Dynamic Environments with Moving obstacles
## Installation & Running Instructions

### 1. Clone or Download the Project
Download the project source code and open the project folder in Visual Studio Code.

### 2. Create a Virtual Environment
Open the VS Code Terminal and run:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Install Required Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Application

```bash
python backend/app.py
```

### 6. Open the Web Application

Open a web browser and visit:

```text
http://127.0.0.1:5000
```

The Robot Navigation simulation interface will be displayed in the browser.

**Note:** Keep the terminal running while using the application. Press `Ctrl + C` to stop the Flask server.