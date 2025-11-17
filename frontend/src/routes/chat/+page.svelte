<script lang="ts">
	import { goto } from "$app/navigation";
	import { getTokens, refresh } from "$lib/api/tokenApi";
	import type { TokenPair } from "$lib/models/tokenModels";
  import { onMount } from "svelte";

  interface ChatMessage {
    username: String;
    message: String;
  };

  // Store for messages
  let messages: ChatMessage[] = [];
  let messageText = "";

  let ws: WebSocket;

  function connectWebSocket() {
    const tokens: TokenPair | null = getTokens();

    if (!tokens) {
      console.error("No token found!");
      return;
    }

    // Connect to the WebSocket with subprotocol "authorization" and token
    ws = new WebSocket("ws://localhost:8000/api/chat/ws", ["authorization", tokens.access_token]);

    ws.onopen = () => {
      console.log("Connected to chat WebSocket");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      messages = [...messages, data];
    };

    ws.onclose = (event) => {
      console.log("WebSocket closed:", event);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };
  }

  function sendMessage() {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      console.error("WebSocket is not connected");
      return;
    }
    if (messageText.trim() === "") return;

    ws.send(JSON.stringify({ message: messageText }));
    messageText = "";
  }

  onMount(async () => {
    if (Error.isError(await refresh())) {
      goto("/login");
    }

    connectWebSocket();
  });
</script>

<style>
  .chat-container {
    max-width: 500px;
    margin: 0 auto;
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 8px;
  }
  .messages {
    height: 300px;
    overflow-y: auto;
    border: 1px solid #eee;
    padding: 0.5rem;
    margin-bottom: 0.5rem;
    background-color: #fafafa;
  }
  .message {
    margin-bottom: 0.5rem;
  }
  .username {
    font-weight: bold;
    margin-right: 0.3rem;
  }
  input {
    width: 80%;
    padding: 0.5rem;
  }
  button {
    padding: 0.5rem 1rem;
  }
</style>

<div class="chat-container">
  <div class="messages">
    {#each messages as msg}
      <div class="message">
        <span class="username">{msg.username}:</span>
        <span class="text">{msg.message}</span>
      </div>
    {/each}
  </div>
  <input
    type="text"
    bind:value={messageText}
    placeholder="Type your message..."
    on:keydown={(e) => e.key === "Enter" && sendMessage()}
  />
  <button on:click={sendMessage}>Send</button>
</div>
