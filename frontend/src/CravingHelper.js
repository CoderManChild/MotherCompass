import React, { useState } from 'react';
import './CravingHelper.css';

const CravingHelper = () => {
  const [craving, setCraving] = useState('');
  const [feeling, setFeeling] = useState('');
  const [diet, setDiet] = useState('vegan');
  const [output, setOutput] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    const generatedOutput = {
      recipe: {
        name: "Vegan Orange & Coconut Pudding",
        ingredients: [
          "1 can (13.5 oz) full-fat coconut milk, chilled overnight",
          "1/2 cup vegan orange juice",
          "1/4 cup maple syrup",
          "1 teaspoon vanilla extract",
          "Pinch of salt",
          "1/4 cup chopped candied orange peel (optional)"
        ],
        instructions: [
          "Scoop out the solid coconut cream from the chilled can, leaving the liquid behind.",
          "In a mixing bowl, beat the coconut cream until fluffy.",
          "Add the orange juice, maple syrup, vanilla extract, and salt to the coconut cream.",
          "Beat until smooth and creamy.",
          "Fold in the candied orange peel, if using.",
          "Pour the pudding into individual serving bowls and refrigerate for at least 2 hours or until set.",
          "Serve chilled."
        ]
      },
      stretch: {
        name: "Upper Back and Shoulder Release",
        description: "This gentle stretch can help release tension in your upper back and shoulders.",
        instructions: [
          "Stand with your feet hip-width apart.",
          "Interlace your fingers behind your back, palms facing out.",
          "Lift your arms up and back, keeping your shoulders relaxed.",
          "Hold for 30 seconds, breathing deeply.",
          "Release your arms and repeat 2-3 times."
        ]
      },
      quote: {
        text: "“The journey of a thousand miles begins with a single step.” - Lao Tzu",
        meaning: "This quote reminds you that even though pregnancy might feel long, every day is a step forward. You're making progress with each passing moment."
      }
    };
    setOutput(generatedOutput);
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
