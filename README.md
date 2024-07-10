![Screenshot 2024-07-07 122552](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/c5bf4cc0-8d7d-4ac9-b007-516f8586077e)
![Screenshot 2024-07-07 122600](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/5c5d55c7-5c0e-4f29-b3b8-fe88299d8b7e)
![Screenshot 2024-07-07 122634](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/2f84e362-827b-4325-825c-213f673b0271)
![Screenshot 2024-07-07 123327](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/d6bcdc87-0e65-4166-a5f9-5f732c53db48)
![Screenshot 2024-07-07 124520](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/46df5148-fd3b-4953-8c14-b88afbd672ac)
![Screenshot 2024-07-07 124536](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/d342d69a-6c52-4297-9d55-9255effd48af)
![Screenshot 2024-07-07 124547](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/ea0c214c-f973-4929-94ed-1d0d99e879d8)
![Screenshot 2024-07-07 124657](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/4c768ce1-df60-4dce-a968-bcfdadee7bfb)
![Screenshot 2024-07-07 124853](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/be427500-18ed-4b45-912a-83875da5882b)
![Screenshot 2024-07-07 124907](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/3a7179f6-82d0-4535-a955-a36d1acc66cc)
![Screenshot 2024-07-07 124928](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/d3aab9a0-5128-4ef6-ab28-9a9ad0872e17)
![Screenshot 2024-07-07 233512](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/467d6741-1e24-4720-9643-f4aacb727ac2)
![Screenshot 2024-07-08 002901](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/6caedd4f-808d-4ac1-993b-306f1cbe0154)
![Screenshot 2024-07-08 003013](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/3342eea4-952f-4dcf-ae76-83c9ee0384bc)
![Screenshot 2024-07-08 003023](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/eb1e45fa-43ea-4a02-9cb8-928bff996b0f)
![Screenshot 2024-07-08 003939](https://github.com/Aayushi-4094/Coud-native-monitoring/assets/97082852/ee873114-9776-4cd0-8268-adc5a486c366)


# Kubernetes Flask Application Deployment

This guide provides detailed instructions on how to deploy a Flask application on Kubernetes using AWS EKS and ECR. We will use Kubernetes for orchestration and management and Amazon ECR for storing Docker images. The steps include creating a Docker image for the Flask app, pushing it to ECR, creating a Kubernetes cluster on EKS, and deploying the application on the cluster.

## Prerequisites

1. **AWS Account**: You need an AWS account to use AWS services.
2. **AWS CLI**: Install and configure the AWS CLI with your credentials.
3. **kubectl**: Install kubectl to interact with your Kubernetes cluster.
4. **Docker**: Install Docker to build and manage container images.
5. **Python**: Ensure Python is installed on your system.

## Step-by-Step Guide

### 1. Flask Application

Create a simple Flask application with system monitoring capabilities.

#### `app.py`
```python
import psutil
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/cpu')
def index():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    message = None
    if cpu_percent > 80 or mem_percent > 80:
        message = "High CPU or Memory utilisation detected. Please scale up"
    return render_template("index.html", cpu_percent=cpu_percent, mem_percent=mem_percent, message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### `index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitoring</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        .plot-graph-div {
            margin: auto;
            width: 50%;
            background-color: rgba(151, 128, 128, 0.688);
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>System Monitoring</h1>
        <div id="cpu-gauge" class="plot-graph-div"></div>
        <div id="mem-gauge" class="plot-graph-div"></div>
        {% if message %}
        <div class="alert alert-danger">{{ message }}</div>
        {% endif %}
    </div>
    <script>
        var cpuGauge = {
            type: "indicator",
            mode: "gauge+number",
            value: {{ cpu_percent }},
            gauge: {
                axis: { range: [null, 100] },
                bar: { color: "#1f77b4" },
                bgcolor: "white",
                borderwidth: 2,
                bordercolor: "#ccc",
                steps: [
                    { range: [0, 50], color: "green" },
                    { range: [50, 85], color: "orange" },
                    { range: [85, 100], color: "red" }
                ],
                threshold: {
                    line: { color: "red", width: 4 },
                    thickness: 0.75,
                    value: {{ cpu_percent }}
                }
            }
        };

        var memGauge = {
            type: "indicator",
            mode: "gauge+number",
            value: {{ mem_percent }},
            gauge: {
                axis: { range: [null, 100] },
                bar: { color: "#1f77b4" },
                bgcolor: "white",
                borderwidth: 2,
                bordercolor: "#ccc",
                steps: [
                    { range: [0, 50], color: "green" },
                    { range: [50, 85], color: "orange" },
                    { range: [85, 100], color: "red" }
                ],
                threshold: {
                    line: { color: "red", width: 4 },
                    thickness: 0.75,
                    value: {{ mem_percent }}
                }
            }
        };

        var cpuGaugeLayout = {
            title: { text: "CPU Utilisation" }
        };
        var memGaugeLayout = {
            title: { text: "Memory Utilisation" }
        };

        Plotly.newPlot('cpu-gauge', [cpuGauge], cpuGaugeLayout);
        Plotly.newPlot('mem-gauge', [memGauge], memGaugeLayout);
    </script>
</body>
</html>
```

### 2. Dockerize the Application

Create a Dockerfile to containerize the Flask application.

#### `Dockerfile`
```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirement.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 to the host
EXPOSE 5000

# Define the command to run the application
CMD ["flask", "run"]
```

#### `requirement.txt`
```txt
Flask==2.2.3
MarkupSafe==2.1.2
Werkzeug==2.2.3
itsdangerous==2.1.2
psutil==5.8.0
plotly==5.5.0
tenacity==8.0.1
boto3==1.9.148
kubernetes==21.7.0
```

### 3. Build and Push Docker Image to ECR

#### `ecr.py`
```python
import boto3

ecr_client = boto3.client('ecr')

repository_name = 'my-cloud-native-repo'

response = ecr_client.create_repository(repositoryName=repository_name)

repository_uri = response['repository']['repositoryUri']
print(repository_uri)
```

**Commands:**
```sh
# Install dependencies
pip install boto3

# Create ECR repository
python ecr.py

# Build Docker image
docker build -t my-flask-app .

# Authenticate Docker to ECR
$(aws ecr get-login --no-include-email --region us-east-1)

# Tag the Docker image
docker tag my-flask-app:latest <repository_uri>:latest

# Push the Docker image to ECR
docker push <repository_uri>:latest
```

### 4. Create EKS Cluster

#### Create the Cluster

1. **Create a Cluster Role**:
    - Attach the `AmazonEKSClusterPolicy` policy.
    - Name the role `EKSClusterRole`.

2. **Create the Cluster**:
    - Name the cluster `cloud-native-cluster`.
    - Use the `EKSClusterRole`.
    - Configure subnets and VPC as per your setup.
    - Create the cluster and wait for it to become active.

3. **Create Node Group**:
    - Name the node group `EKSNodeRole`.
    - Attach the `AmazonEKSWorkerNodePolicy`, `AmazonEC2ContainerRegistryReadOnly`, and `AmazonEKS_CNI_Policy` policies.
    - Create the node group.

### 5. Deploy the Application to EKS

#### `kubernetes_script.py`
```python
from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "my-flask-app"}),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="<repository_uri>:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)
```

**Commands:**
```sh
# Install dependencies
pip install kubernetes

# Run the Kubernetes script
python kubernetes_script.py
```

### 6. Verify Deployment

**Commands:**
```sh
# Get pods
kubectl get pods -n default -w

# Get services
kubectl get svc -n default

# Describe pod
kubectl describe pod <pod_name> -n default

# Get deployments
kubectl get deployments -n default

# Edit deployment
kubectl edit deployment <deployment_name> -

n default

# Port forward to access the Flask application
kubectl port-forward svc/my-flask-service 5000:5000
```

This README provides a comprehensive guide to deploying a Flask application on AWS EKS using Kubernetes. Follow the steps to set up your environment, build and push your Docker image to ECR, create an EKS cluster, deploy your application, and verify the deployment.
