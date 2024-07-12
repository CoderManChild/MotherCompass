import React, { useState, useEffect } from 'react';
import './ChatContainer.css';

const ChatContainer = () => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/messages');
      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const sendMessage = async () => {
    if (messageInput.trim() !== '') {
      const newMessage = { type: 'sent', sender: 'Mother', text: messageInput };
      try {
        const response = await fetch('http://127.0.0.1:5000/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newMessage)
        });
        const data = await response.json();
        setMessages([...messages, data]);
        setMessageInput('');
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  return (
    <section className="chat-container">
      <h1 className="chat-title">Mother's Compass Group Chat</h1>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <p>{msg.sender}: {msg.text}</p>
          </div>
        ))}
      </div>
      <div className="input-box">
        <input
          type="text"
          value={messageInput}
          onChange={(e) => setMessageInput(e.target.value)}
          placeholder="Type your message here..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </section>
  );
};

export default ChatContainer;
