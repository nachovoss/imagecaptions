
# Image Captioning App

## Description
This Flask-based application generates captions for images using machine learning. It leverages Hypercorn and asyncio for improved performance.

## Setup & Installation

### Local Environment
**Prerequisites:**
- Python 3.9
- Pip
- Virtualenv (optional)

**Steps:**
1. Clone the repository.
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv #python3 for linux
   source venv/bin/activate  # linux
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Docker Environment
**Prerequisites:**
- Docker
- Docker Compose

**Steps:**
1. Run `docker-compose up` to start the application.

## Performance Enhancement with Hypercorn and Asyncio
The application uses Hypercorn as an ASGI server, along with asyncio, to enhance performance through asynchronous processing. This setup allows for handling multiple requests efficiently.

## Scaling Up with Kubernetes
For scaling the application:

1. Create Kubernetes configurations for deployment, services, and horizontal pod autoscalers.
2. Deploy to a Kubernetes cluster, adjusting replicas as needed for load.

## Usage
Send a POST request to `/caption` with an image file.
   curl -X POST -F "file=@path/to/your/image.jpg" http://localhost:5000/caption
   


## Running Tests
Execute tests using `python -m unittest` from the src directory.

## Contributing
Contributions are welcome following the standard fork, branch, and pull request workflow.

## License
[MIT License](LICENSE)
