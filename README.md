<p align="center">
  <img src="logo.jpg" height="200">
</p>
<h1 align="center">
  NEUROHUB
</h1>

## Installation for developers

``` bash
git clone https://github.com/BBG-Deep-Inc/chatgpt.git
```

``` bash
cd chatgpt
python3 -m venv .venv   
source chatgpt/.venv/bin/activate 
```


``` bash
cd frontend
pip3 install -r requirements.txt
python3 app.py
```

``` bash
cd backend
pip3 install -r requirements.txt
python3 api.py
```

> [!IMPORTANT]
> The frontend requires a running backend server to function. Make sure to start the backend first.
## Licence
NEUROHUB is released under the [Apache License 2.0](LICENSE).
