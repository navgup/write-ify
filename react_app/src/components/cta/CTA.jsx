import React, {useState, useEffect} from 'react';
import './cta.css';
import InteractiveTextBox from './textbox.jsx';
import { UseSelector } from 'react-redux';
import axios from "axios";

export const CTA = () => {

  const [inputValue, setInputValue] = useState('');


const sendText = async (text) => {
  try {
    const response = await axios.post('https://navgup.pythonanywhere.com/predict', { text });
    return response.data; 
  } catch (error) {
    console.error('Error processing text:', error);
    return null;
  }
};

useEffect(() => {
    const intervalId = setInterval(() => {
      // Check if the input value is not empty
      if (inputValue.trim() !== '') {
        sendText(inputValue) 
          .then(result => {
            if (result !== null) {
              console.log('Result from ML model:', result);
            }
          })
          .catch(error => {
            console.error('Error processing text:', error);
          });
      }
    }, 40000); // 60000 ms = 1 minute

    return () => {
      clearInterval(intervalId); 
    };
  }, [inputValue]);

  return (
    <div>
      <InteractiveTextBox inputText={inputValue} onInputUpdate={setInputValue} />
    </div>
  )
}

export default CTA
