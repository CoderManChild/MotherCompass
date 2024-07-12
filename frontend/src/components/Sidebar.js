import React, { useState } from 'react';
import './Sidebar.css';

const Sidebar = () => {
  const [events, setEvents] = useState([
    'July 15: Newborn Care Workshop',
    'August 1: Breastfeeding Basics',
    'September 10: Postpartum Recovery'
  ]);

  const addEvent = () => {
    const event = prompt('Enter your event:');
    if (event) {
      setEvents([...events, event]);
    }
  };

  return (
    <aside className="sidebar" id="sidebar">
      <h2>Events</h2>
      <ul id="events-list">
        {events.map((event, index) => (
          <li key={index}>{event}</li>
        ))}
      </ul>
      <button onClick={addEvent}>Add Event</button>
      <h2>Participants</h2>
      <ul>
        <li>Dr. Smith (OB/GYN)</li>
        <li>Nurse Mary (CNM)</li>
        <li>Mother</li>
      </ul>
    </aside>
  );
};

export default Sidebar;
