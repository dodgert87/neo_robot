# Chatbot Frontend Documentation

## Overview
A simple, interactive chatbot frontend built with HTML, CSS (Bootstrap), and JavaScript. It integrates with a backend API to process user messages, supports speech-to-text input via microphone, and provides text-to-speech output through speakers. The application is styled with Bootstrap for a modern, responsive design.

**Version**: 1.0

---

## Features
- **Chat Interface**: Displays user messages (right-aligned) and bot responses (left-aligned).
- **Speech-to-Text**: Converts spoken input from the microphone into text using the Web Speech API's `SpeechRecognition`.
- **Text-to-Speech**: Reads bot responses aloud using the Web Speech API's `SpeechSynthesis`.
- **Random User ID**: Generates a unique `userId` for each session.
- **Backend Integration**: Sends POST requests to `http://127.0.0.1:8000/chat/` and displays the `response.response` field.
- **Responsive Design**: Styled with Bootstrap 5.3.3 for a polished, mobile-friendly look.
- **Error Handling**: Shows errors in the chat UI if backend requests fail or speech features encounter issues.

---

## Prerequisites
- **Browser**: A modern browser supporting the Web Speech API (e.g., Chrome, Firefox, Edge).
- **Backend Server**: A running backend API at `http://127.0.0.1:8000/chat/` that accepts POST requests with a JSON body:
```json
{
  "userId": "string",
  "requestBody": "string"
}
```
and returns a response in the format:

```json
{
  "status": "success",
  "response": {
    "response": "Bot response text here",
    ...
  }
}
```
- **Local Server**: Python 3.x to serve the HTML file.
- **Microphone**: A working laptop/desktop microphone for speech-to-text.

### Run the Local Server
Open a terminal in the directory containing index.html.
Run:

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```
This starts a server on port 8080.

### Access the Application
Open a browser and navigate to http://localhost:8080/.
The chatbot interface should load.

### Ensure Backend is Running
Verify that your backend server is active on http://127.0.0.1:8000/chat/. Test it with a tool like Postman if needed.


### Usage

#### Typing a Message
1. Open [http://localhost:8080/](http://localhost:8080/).
2. Type a message (e.g., "tell me the weather update in Tampere") in the input field.
3. Press **Enter** or click **Send**.
4. Your message will appear on the right (blue), and the bot’s response will appear on the left (gray) and be spoken aloud.

#### Speaking a Message
1. Click the 🎤 **Start Listening** button.
2. Grant microphone access when prompted.
3. Speak clearly (e.g., "tell me a joke").
4. The button will change to 🎤 **Stop Listening**, and "Listening..." will appear in the chat.
5. When you finish speaking (or click **Stop**), the transcribed text will appear as a user message and be sent to the backend.
6. The bot will respond in both text and speech.


## Code Structure

### HTML
- **Head**:
    - Meta tags for charset and viewport.
    - Bootstrap 5.3.3 CSS CDN.
    - Custom CSS for chat container and message alignment.
- **Body**:
    - Bootstrap container with title, chat container (`#chat-container`), and input group (`#input-container`).
    - Buttons: **Send** and 🎤 **Start Listening**.
    - Bootstrap JS CDN.

### CSS
- **Bootstrap**:
    - Base styling for layout, buttons, and input.
- **Custom**:
    - `#chat-container`: 400px height, scrollable, light gray background.
    - `.message`: Padding, margin, max-width for messages.
    - `.user-message` / `.bot-message`: Alignment and Bootstrap classes (`bg-primary`, `bg-light`).

### JavaScript
- **Constants**:
    - `chatContainer`, `chatInput`, `micBtn`: DOM references.
    - `userId`: Random session ID.
- **Functions**:
    - `generateUserId()`: Creates a unique ID (e.g., `user-abc123xyz`).
    - `addMessage(text, isUser)`: Adds messages to the UI with appropriate styling.
    - `speakText(text)`: Converts text to speech (`en-US`).
    - `sendChatRequest(message)`: Sends POST requests to the backend.
    - `sendMessage()`: Handles typed input submission.
    - `toggleSpeechRecognition()`: Starts/stops speech recognition.


### Text-to-Speech Details

#### API
Utilizes `SpeechSynthesisUtterance` from the Web Speech API.

#### Configuration
- **`lang`**: `'en-US'` - English (US) voice.
- **`rate`**: `1` - Normal speaking speed (range: 0.1 to 10).
- **`volume`**: `1` - Full volume (range: 0 to 1).

#### Behavior
- Triggered on bot responses, converting the `response.response` text into audible speech via the device’s speakers.
- **Fallback**: If unsupported, displays "Sorry, your browser does not support text-to-speech."

---

### Speech-to-Text Details

#### API
Uses `SpeechRecognition` (or `webkitSpeechRecognition` for Chrome compatibility).

#### Configuration
- **`lang`**: `'en-US'` - Recognizes English (US) speech.
- **`interimResults`**: `false` - Delivers only final transcription, not partial results.
- **`maxAlternatives`**: `1` - Returns the single best transcription.

#### Behavior
- Activated by the 🎤 **Start Listening** button.
- Captures audio from the microphone, transcribes it, and adds it as a user message.
- Automatically sends the transcribed text to the backend.

#### Events
- **`onresult`**: Processes the transcription and triggers the chat flow.
- **`onstart`**: Updates UI to indicate listening.
- **`onend`**: Resets UI when recognition stops.
- **`onerror`**: Handles errors (e.g., "no-speech", "audio-capture").

#### Fallback
Disables the mic button and shows "Not Supported" if the browser lacks support.

---

### Limitations
- Requires an active backend server.
- No persistent chat history (clears on refresh).
- Basic error handling; enhance as needed for production.
