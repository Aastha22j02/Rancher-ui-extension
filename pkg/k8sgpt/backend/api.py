from fastapi import FastAPI, HTTPException, Query
import subprocess
import shlex
from typing import List
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import os, json
import uuid, ssl
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration to allow requests from your frontend (e.g., localhost:8005)
origins = [
"https://localhost:8005",
"http://localhost:8005",
# Add more allowed origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Directory to store uploaded kubeconfig files
UPLOAD_DIR = "uploaded_kubeconfigs"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def execute_command(command: str):
    print(command)
    try:
        args = shlex.split(command)
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        
        # Try to parse the output as JSON
        try:
            output = json.loads(result.stdout)
            return output
        except json.JSONDecodeError:
            # If parsing fails, return the raw output
            return {"stdout": result.stdout}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command execution failed: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/upload_kubeconfig")
async def upload_kubeconfig(file: UploadFile = File(...)):
    try:
        # Generate a unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return JSONResponse(content={"filename": unique_filename}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/install-operator")
async def install_operator(
    kubeconfig_filename: str = Query(None, description="Filename of the uploaded kubeconfig")
):
    if not kubeconfig_filename:
        return JSONResponse(content={"error": "Kubeconfig filename is required"}, status_code=400)

    kubeconfig_path = os.path.join(UPLOAD_DIR, kubeconfig_filename)
    if not os.path.exists(kubeconfig_path):
        return JSONResponse(content={"error": "Kubeconfig file not found"}, status_code=404)

    commands = [
        f"helm repo add k8sgpt https://charts.k8sgpt.ai/ --kubeconfig {kubeconfig_path}",
        f"helm repo update --kubeconfig {kubeconfig_path}",
        f"helm install release k8sgpt/k8sgpt-operator -n k8sgpt-operator-system --create-namespace --kubeconfig {kubeconfig_path}"
    ]

    results = []
    for command in commands:
        try:
            result = execute_command(command)
            results.append({"command": command, "result": result})
        except HTTPException as e:
            results.append({"command": command, "error": e.detail})
            break  # Stop execution if a command fails

    return JSONResponse(content={"results": results}, status_code=200)

@app.get("/analyze")
async def analyze(
    kubeconfig_filename: str = Query(None, description="Filename of the uploaded kubeconfig"),
    anonymize: bool = Query(False, description="Anonymize data before sending it to the AI backend"),
    backend: str = Query(None, description="Backend AI provider"),
    custom_analysis: bool = Query(False, description="Enable custom analyzers"),
    custom_headers: List[str] = Query(None, description="Custom Headers, <key>:<value>"),
    explain: bool = Query(False, description="Explain the problem"),
    filter: List[str] = Query(None, description="Filter for these analyzers"),
    interactive: bool = Query(False, description="Enable interactive mode"),
    language: str = Query("english", description="Language to use for AI"),
    max_concurrency: int = Query(10, description="Maximum number of concurrent requests"),
    namespace: str = Query(None, description="Namespace to analyze"),
    no_cache: bool = Query(False, description="Do not use cached data"),
    output: str = Query("text", description="Output format (text, json)"),
    selector: str = Query(None, description="Label selector"),
    with_doc: bool = Query(False, description="Give me the official documentation of the involved field"),
    config: str = Query(None, description="Default config file"),
    kubeconfig: str = Query(None, description="Path to a kubeconfig"),
    kubecontext: str = Query(None, description="Kubernetes context to use")
):
    command = "k8sgpt analyze"
    
    if anonymize:
        command += " --anonymize"
    if backend:
        command += f" --backend {backend}"
    if custom_analysis:
        command += " --custom-analysis"
    if custom_headers:
        for header in custom_headers:
            command += f" --custom-headers {header}"
    if explain:
        command += " --explain"
    if filter:
        for f in filter:
            command += f" --filter {f}"
    if interactive:
        command += " --interactive"
    if language != "english":
        command += f" --language {language}"
    if max_concurrency != 10:
        command += f" --max-concurrency {max_concurrency}"
    if namespace:
        command += f" --namespace {namespace}"
    if no_cache:
        command += " --no-cache"
    if output != "text":
        command += f" --output {output}"
    if selector:
        command += f" --selector {selector}"
    if with_doc:
        command += " --with-doc"
    if config:
        command += f" --config {config}"
    if kubeconfig:
        command += f" --kubeconfig {kubeconfig}"
    if kubecontext:
        command += f" --kubecontext {kubecontext}"
    
    # Handle kubeconfig
    if kubeconfig_filename:
        kubeconfig_path = os.path.join(UPLOAD_DIR, kubeconfig_filename)
        if os.path.exists(kubeconfig_path):
            command += f" --kubeconfig {kubeconfig_path}"
        else:
            return JSONResponse(content={"error": "Kubeconfig file not found"}, status_code=404)

    return execute_command(command + " --output=json")

@app.post("/auth/add")
async def auth_add(
    backend: str = Query("openai", description="Backend AI provider"),
    baseurl: str = Query(None, description="URL AI provider"),
    compartmentId: str = Query(None, description="Compartment ID for generative AI model (only for oci backend)"),
    endpointname: str = Query(None, description="Endpoint Name (only for amazonbedrock, amazonsagemaker backends)"),
    engine: str = Query(None, description="Azure AI deployment name (only for azureopenai backend)"),
    maxtokens: int = Query(2048, description="Specify a maximum output length"),
    model: str = Query("gpt-3.5-turbo", description="Backend AI model"),
    organizationId: str = Query(None, description="OpenAI or AzureOpenAI Organization ID"),
    password: str = Query(None, description="Backend AI password"),
    providerId: str = Query(None, description="Provider specific ID for e.g. project (only for googlevertexai backend)"),
    providerRegion: str = Query(None, description="Provider Region name (only for amazonbedrock, googlevertexai backend)"),
    temperature: float = Query(0.7, description="The sampling temperature"),
    topk: int = Query(50, description="Sampling Cutoff"),
    topp: float = Query(0.5, description="Probability Cutoff"),
    config: str = Query(None, description="Default config file"),
    kubeconfig: str = Query(None, description="Path to a kubeconfig"),
    kubecontext: str = Query(None, description="Kubernetes context to use")
):
    command = f"k8sgpt auth add --backend {backend}"
    
    if baseurl:
        command += f" --baseurl {baseurl}"
    if compartmentId:
        command += f" --compartmentId {compartmentId}"
    if endpointname:
        command += f" --endpointname {endpointname}"
    if engine:
        command += f" --engine {engine}"
    if maxtokens != 2048:
        command += f" --maxtokens {maxtokens}"
    if model != "gpt-3.5-turbo":
        command += f" --model {model}"
    if organizationId:
        command += f" --organizationId {organizationId}"
    if password:
        command += f" --password {password}"
    if providerId:
        command += f" --providerId {providerId}"
    if providerRegion:
        command += f" --providerRegion {providerRegion}"
    if temperature != 0.7:
        command += f" --temperature {temperature}"
    if topk != 50:
        command += f" --topk {topk}"
    if topp != 0.5:
        command += f" --topp {topp}"
    if config:
        command += f" --config {config}"
    if kubeconfig:
        command += f" --kubeconfig {kubeconfig}"
    if kubecontext:
        command += f" --kubecontext {kubecontext}"
    
    return execute_command(command)

@app.post("/auth/default")
async def auth_default(
    provider: str = Query(..., description="The name of the provider to set as default"),
    config: str = Query(None, description="Default config file"),
    kubeconfig: str = Query(None, description="Path to a kubeconfig"),
    kubecontext: str = Query(None, description="Kubernetes context to use")
):
    command = f"k8sgpt auth default --provider {provider}"
    
    if config:
        command += f" --config {config}"
    if kubeconfig:
        command += f" --kubeconfig {kubeconfig}"
    if kubecontext:
        command += f" --kubecontext {kubecontext}"
    
    return execute_command(command)

@app.get("/auth/list")
async def auth_list(
    details: bool = Query(False, description="Print active provider configuration details"),
    config: str = Query(None, description="Default config file"),
    kubeconfig: str = Query(None, description="Path to a kubeconfig"),
    kubecontext: str = Query(None, description="Kubernetes context to use")
):
    command = "k8sgpt auth list"
    
    if details:
        command += " --details"
    if config:
        command += f" --config {config}"
    if kubeconfig:
        command += f" --kubeconfig {kubeconfig}"
    if kubecontext:
        command += f" --kubecontext {kubecontext}"
    
    return execute_command(command)



@app.delete("/auth/remove")
async def auth_remove(
    backends: List[str] = Query(..., description="Backend AI providers to remove"),
    config: str = Query(None, description="Default config file"),
    kubeconfig: str = Query(None, description="Path to a kubeconfig"),
    kubecontext: str = Query(None, description="Kubernetes context to use")
):
    backends_str = ",".join(backends)
    command = f"k8sgpt auth remove --backends {backends_str}"
    
    if config:
        command += f" --config {config}"
    if kubeconfig:
        command += f" --kubeconfig {kubeconfig}"
    if kubecontext:
        command += f" --kubecontext {kubecontext}"
    
    return execute_command(command)

@app.put("/auth/update")
async def auth_update(
    backend: str = Query(..., description="Update backend AI provider"),
    baseurl: str = Query(None, description="Update URL AI provider"),
    engine: str = Query(None, description="Update Azure AI deployment name"),
    model: str = Query(None, description="Update backend AI model"),
    organizationId: str = Query(None, description="Update OpenAI or Azure organization Id"),
    password: str = Query(None, description="Update backend AI password"),
    temperature: float = Query(None, description="The sampling temperature"),
    config: str = Query(None, description="Default config file"),
    kubeconfig: str = Query(None, description="Path to a kubeconfig"),
    kubecontext: str = Query(None, description="Kubernetes context to use")
):
    command = f"k8sgpt auth update --backend {backend}"
    
    if baseurl:
        command += f" --baseurl {baseurl}"
    if engine:
        command += f" --engine {engine}"
    if model:
        command += f" --model {model}"
    if organizationId:
        command += f" --organizationId {organizationId}"
    if password:
        command += f" --password {password}"
    if temperature is not None:
        command += f" --temperature {temperature}"
    if config:
        command += f" --config {config}"
    if kubeconfig:
        command += f" --kubeconfig {kubeconfig}"
    if kubecontext:
        command += f" --kubecontext {kubecontext}"
    
    return execute_command(command)


@app.get("/cache/{action}")
async def cache(action: str):
    return execute_command(f"k8sgpt cache {action}")

@app.get("/filters/{action}")
async def filters(action: str):
    return execute_command(f"k8sgpt filters {action}")

@app.get("/generate/{backend}")
async def generate(backend: str):
    return execute_command(f"k8sgpt generate {backend}")

@app.get("/integration/{action}")
async def integration(action: str):
    return execute_command(f"k8sgpt integration {action}")

@app.get("/serve")
async def serve():
    return execute_command("k8sgpt serve")

@app.get("/version")
async def version():
    return execute_command("k8sgpt version")

if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )
