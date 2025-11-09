import React from 'react';
import AppName from './components/AppName';
import Headings from './components/Headers';
import QueryBar from './components/QueryBar';
import Chat from './components/Chat';
import Button from './components/Button';

const App = () => {
  
  // Acknowledge the click button event
  const handleQuery = () => {
    alert('Query Button Clicked!')
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
            <p>what can i help you with?</p>
          </div>
        </Chat>
      </div>

      <div className="search-bar-container">
        <QueryBar>
          <textarea className="query-input" placeholder="Enter your query" />
          <Button textContent='Send' handleClick={handleQuery} />
        </QueryBar>
      </div>
    </>
  )
}
export default App;
