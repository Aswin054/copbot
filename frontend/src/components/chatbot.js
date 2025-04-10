import React, { useState } from "react";
import axios from "axios";
import "../styles/Chatbot.css";

const Chatbot = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  // Send message to backend
  const sendMessage = async () => {
    if (!query.trim()) return;

    const userMessage = { text: query, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");

    setIsTyping(true); // Show typing indicator

    try {
      const response = await axios.post("https://copbot-tbpj.onrender.com/query", { query });

      setTimeout(() => {
        setIsTyping(false); // Remove typing indicator
        const botMessage = { text: response.data.response, sender: "bot" };
        setMessages((prev) => [...prev, botMessage]); // ✅ Add bot response after 30ms
      }, 30);
    } catch (error) {
      console.error("Error sending message:", error);
      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        { text: "Error: Unable to connect to the server.", sender: "bot" },
      ]);
    }
  };

  // ✅ Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chat-header">
        <h2>CopBot Chatbox</h2>
      </div>

      {/* ✅ Chat Area */}
      <div className="chat-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className="message-bubble">{msg.text}</div>
          </div>
        ))}
        {isTyping && (
          <div className="message bot">
            <div className="message-bubble typing">...</div>
          </div>
        )}
      </div>

      {/* ✅ Input Area */}
      <div className="input-area">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask CopBot something..."
        />
        <button onClick={sendMessage}>Ask</button>
      </div>
    </div>
  );
};

export default Chatbot;
