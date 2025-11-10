import React from 'react';
import AppName from './components/AppName';
import Headings from './components/Headers';
import QueryBar from './components/QueryBar';
import Chat from './components/Chat';
import Button from './components/Button';
import { useState } from 'react';
import axios from 'axios';

const App = () => {

  // State to manage user latest input
  const [inputValue, setInputValue] = useState('');

  // State to manage full list of messages
  const [chatMessages, setChatMessages] = useState<{type: string, content: string}[]>([]);

  // Updates the current list of messages after user clicks button
  const handleSend = async () => {
    if (inputValue.trim() === '') return;
    // Update Current list of messages
    setChatMessages([...chatMessages, {type: 'user', content: inputValue}]);
    // Clear current input state
    setInputValue('');

    // Send the message to the backend
    const response = await axios.post('http://127.0.0.1:8000/api/v1/chat', {
      messages: [...chatMessages, {type: 'user', content: inputValue}],
    });
    console.log(response.data);
    setChatMessages(prev => [...prev, {type: 'assistant', content: response.data.response_message.content}]);
  }

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(event.target.value);
  }


  return (
    <>
      <AppName>
        <h1>ThreadWeaver</h1>
      </AppName>
      
      <div className="headings-container">
        <Headings>
          <p>ThreadWeaver is a tool that helps you work seamlessly across Slack, Notion, and WhatsApp Business.</p>
        </Headings>
      </div>

      <div className="chat-container">
        <Chat>
          <div>
            {/* Display the list of messages */}
            {chatMessages.map((message, index) => (
              <div className="chat-message" key={index}>
                {message.type === 'user' ? <div className="user-message">{message.content}</div> : <div className="assistant-message">{message.content}</div>}
              </div>
            ))}
          </div>
        </Chat>
      </div>

      <div className="search-bar-container">
        <QueryBar>
          <textarea className="query-input" placeholder="Enter your query" value={inputValue} onChange={handleInputChange} />
          <Button textContent='Send' handleClick={handleSend} />
        </QueryBar>
      </div>
    </>
  )
}
export default App;
