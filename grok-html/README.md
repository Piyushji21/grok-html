# Grok AI Interface

A modern web interface for interacting with Grok AI and ChatGPT, featuring a chat-like UI with real-time streaming, code syntax highlighting, and conversation history.

## Features

- **Chat Interface**: Modern chat-like UI with message bubbles and typing indicators
- **Multi-AI Support**: Switch between Grok and ChatGPT models
- **Real-time Streaming**: Live response streaming for Grok
- **Code Highlighting**: Automatic syntax highlighting for code blocks with copy functionality
- **Conversation History**: Save and load previous conversations
- **Responsive Design**: Works on desktop and mobile devices
- **Proxy Support**: Configure custom proxies for API requests

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the API server:
   ```bash
   python api_server.py
   ```

4. Open `index.html` in your web browser

The server will start on `http://localhost:6969`

## Usage

1. **Configure Proxy**: Enter your proxy server details in the format `http://user:pass@host:port`
2. **Select AI Model**: Choose between Grok or ChatGPT from the dropdown
3. **Send Messages**: Type your message and press Enter or click the send button
4. **Enable Streaming**: Check the streaming option for real-time responses (Grok only)
5. **View History**: Use the sidebar to toggle and load previous conversations

### API Endpoints

#### POST /ask
Send a message to the AI.

**Request Body:**
```json
{
  "proxy": "http://user:pass@host:port",
  "message": "Your message here",
  "model": "grok-3-auto",
  "ai_type": "grok",
  "stream": false,
  "image": "base64_encoded_image" // For ChatGPT with images
}
```

**Response:**
```json
{
  "status": "success",
  "stream_response": ["Response", "tokens"],
  "extra_data": {...}
}
```

## Project Structure

- `index.html` - Main web interface
- `api_server.py` - FastAPI backend server
- `test_request.py` - API testing script
- `core/` - Core Grok API implementation
- `wrapper/` - Reverse engineering utilities for API access
- `hosting/` - Hosting-related files
- `requirements.txt` - Python dependencies

## Configuration

### Backend Configuration

The API server runs on port 6969 by default. You can modify this in `api_server.py`:

```python
if __name__ == "__main__":
    run("api_server:app", host="0.0.0.0", port=6969)
```

### Frontend Configuration

Update the API base URL in `index.html` if needed:

```javascript
const API_BASE_URL = 'http://localhost:6969';
```

## Troubleshooting

### Common Issues

1. **"Failed to fetch" errors**: Ensure the API server is running and the proxy is correctly configured
2. **Streaming not working**: Streaming is only supported for Grok models
3. **Image upload not working**: Image uploads are only available for ChatGPT

### Proxy Configuration

Make sure your proxy supports HTTPS requests and has the correct format:
- `http://host:port`
- `http://user:pass@host:port`

## Contributing

This project uses reverse engineering techniques to access AI APIs. Please be aware of the terms of service for the respective AI platforms.

## License

This project is for educational purposes only. Use at your own risk.
