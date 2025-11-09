import React from 'react';
import AppName from './components/AppName';
import Headings from './components/Headers';
import QueryBar from './components/QueryBar';
import Chat from './components/Chat';
import Button from './components/Button';
import { useState } from 'react';

const App = () => {

  // State to manage user latest input
  const [inputValue, setInputValue] = useState('');

  // State to manage full list of messages
  const [chatMessages, setChatMessages] = useState<string[]>([]);

  // Updates the current list of messages after user clicks button
  const handleSend = () => {
    if (inputValue.trim() === '') return;

    // Update Current list of messages
    setChatMessages([...chatMessages, inputValue]);
    // Clear current input state
    setInputValue('');
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
                {message}
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
