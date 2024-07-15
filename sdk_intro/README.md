# Intro to Groundlight Python SDK

Get started writing your own Groundlight applications with this introductory tutorial. 

Watch the full video: [https://www.youtube.com/watch?v=X4n0oiwbb3Y](https://www.youtube.com/watch?v=X4n0oiwbb3Y)

## Instructions

### 1. Create a folder for your sample project
```bash
mkdir gl_sample
cd gl_sample
```
### 2. Create a virtual Python environment for this project.
```bash
python3 -m venv gl_env
```
### 3. Activate your virtual Python environment
Windows:
```bash
gl_env/Scripts/activate
```
Mac/Linux:
```bash
source gl_env/bin/activate
```
### 4. Install dependencies
```bash
pip install groundlight framegrab
```
### 5. Generate API token
Log in to your account at groundlight.ai, go to "Api Tokens" and generate an API token.

More info on API tokens here: https://code.groundlight.ai/python-sdk/docs/getting-started/api-tokens. 

Export your API token to your terminal so you can use it in your sample application

Windows:
```bash
$env:GROUNDLIGHT_API_TOKEN="<YOUR API TOKEN GOES HERE>"
```

Mac/Linux:
```bash
export GROUNDLIGHT_API_TOKEN="<YOUR API TOKEN GOES HERE>"
```

### 6. Write your application

Check out `main.py` in this repo to see the code we used in the tutorial. 

### 7. Run your application

```bash
python3 main.py
```




