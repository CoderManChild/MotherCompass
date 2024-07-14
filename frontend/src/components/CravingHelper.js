import React, { useState } from 'react';
import './CravingHelper.css';

const CravingHelper = () => {
  const [craving, setCraving] = useState('');
  const [feeling, setFeeling] = useState('');
  const [diet, setDiet] = useState('vegan');
  const [output, setOutput] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/cravings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          craving,
          feeling,
          diet,
        }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setOutput(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="craving-helper">
      <h1>Craving Helper</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="craving">What are you craving?</label>
          <input
            type="text"
            id="craving"
            value={craving}
            onChange={(e) => setCraving(e.target.value)}
            placeholder="e.g., oranges in a sweet dish"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="feeling">How are you feeling?</label>
          <input
            type="text"
            id="feeling"
            value={feeling}
            onChange={(e) => setFeeling(e.target.value)}
            placeholder="e.g., some upper back and shoulder pain"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="diet">Your dietary preference:</label>
          <select
            id="diet"
            value={diet}
            onChange={(e) => setDiet(e.target.value)}
          >
            <option value="vegan">Vegan</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="gluten-free">Gluten-Free</option>
            <option value="none">None</option>
          </select>
        </div>
        <button type="submit">Get Help</button>
      </form>
      {output && (
        <div className="output">
          <h2>Generated Output</h2>
          <div className="output-section">
            <div className="recipe">
              <h3>{output.recipe.name}</h3>
              <h4>Ingredients:</h4>
              <ul>
                {output.recipe.ingredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
              <h4>Instructions:</h4>
              <ol>
                {output.recipe.instructions.map((instruction, index) => (
                  <li key={index}>{instruction}</li>
                ))}
              </ol>
            </div>
            <div className="stretch">
              <h3>{output.stretch.name}</h3>
              <p>{output.stretch.description}</p>
              <ol>
                {output.stretch.instructions.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
            </div>
            <div className="quote">
              <blockquote>
                <p>{output.quote.text}</p>
                <p><em>{output.quote.meaning}</em></p>
              </blockquote>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CravingHelper;


