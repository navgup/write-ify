import React, {useState} from 'react';
import "./textbox.css"

function InteractiveTextBox({inputText, onInputUpdate}) {
  
    const handleInputChange = (event) => {
      onInputUpdate(event.target.value);
    };
  
    
    return (
      <div className="textbox-container">
        <textarea
          className="custom-textbox"
          placeholder="Start Writing..."
          value={inputText}
          onChange={handleInputChange}
        />
     </div>
    );
  }
  
  export default InteractiveTextBox;