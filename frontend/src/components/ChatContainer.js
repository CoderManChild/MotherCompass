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
      const response = await fetch('http://127.0.0.1:8000/api/posts/');
      const data = await response.json();
      if (data.success) {
        // Assuming the backend returns an array of messages in `data.data`
        setMessages(data.data);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const sendMessage = async () => {
    if (messageInput.trim() !== '') {
      const newMessage = { title: 'New Message', content: messageInput, mother_id: 1 }; // example mother_id
      try {
        const response = await fetch('http://127.0.0.1:8000/api/posts/1', { // example mother_id
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newMessage)
        });
        const data = await response.json();
        if (data.success) {
          setMessages([...messages, data.data]);
          setMessageInput('');
        }
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
            <p>{msg.title}: {msg.content}</p>
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
