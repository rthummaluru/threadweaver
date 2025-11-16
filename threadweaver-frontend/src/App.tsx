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

  // State to manage loading state
  const [isLoading, setIsLoading] = useState(false);

  // Updates the current list of messages after user clicks button
  const handleSend = async () => {
    if (inputValue.trim() === '') return;
    setIsLoading(true);
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
    setIsLoading(false);
  }

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(event.target.value);
  }


  return (
    <>
      <div className="app-container flex justify-center items-center bg-red-200 text-center">
        <AppName>
          <h1>ThreadWeaver</h1>
        </AppName>
      </div>
      
      <div className="headings-container text-center">
        <Headings>
          <p>ThreadWeaver is a tool that helps you work seamlessly across Slack, Notion, and WhatsApp Business.</p>
        </Headings>
      </div>

      <div className="chat-container flex justify-center items-center bg-green-200 max-w-lg mx-auto p-4 m-4">
        <Chat>
          <div className="w-full max-w-3xl flex flex-col gap-4">
            {/* Display the list of messages */}
            {chatMessages.map((message, index) => (
              <div className="chat-message flex" key={index}>
                {message.type === 'user' ? 
                  <div className="user-message bg-blue-500 text-white p-3 rounded-lg ml-auto max-w-md">{message.content}</div> : 
                  <div className="assistant-message bg-gray-200 text-black p-3 rounded-lg mr-auto max-w-md">{message.content}</div>}
              </div>
            ))}

            {isLoading && <div className="loading-message bg-black-500 text-white p-3 rounded-lg mr-auto max-w-md">Loading...</div>}
            {!isLoading && chatMessages.length === 0 && <div className="initial-message"> Start a conversation!</div>}
          </div>
        </Chat>
      </div>

      <div className="search-bar-container text-center">
        <QueryBar>
          <textarea className="query-input" placeholder="Enter your query" value={inputValue} onChange={handleInputChange} />
          <Button textContent='Send' handleClick={handleSend} />
        </QueryBar>
      </div>
    </>
  )
}
export default App;
