import Chat from '../components/Chat';
import Button from '../components/Button';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import QueryBar from '../components/QueryBar';
import AppName from '../components/AppName';
import Headings from '../components/Headers';

import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_DEFAULT_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);



const ChatPage = () => {

    // State to manage user latest input
    const [inputValue, setInputValue] = useState('');
  
    // State to manage full list of messages
    const [chatMessages, setChatMessages] = useState<{type: string, content: string}[]>([]);
  
    // State to manage loading state
    const [isLoading, setIsLoading] = useState(false);
  
    // State to manage disabled state of the button
    const [isDisabled, setIsDisabled] = useState(false);
  
    // State to manage session id
    const [sessionId, setSessionId] = useState<string | null>(null);

    // State to manage user id
    const [userId, setUserId] = useState<string | null>(null);

    // State to manage document upload
    const [documentUpload, setDocumentUpload] = useState<File | null>(null);

    // State to manage access token
    const [accessToken, setAccessToken] = useState<string | null>(null);
  
  
    // Get the session id from the backend
    const getSessionId = async () => {
      try {
        console.log('Getting session id...'); 
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/users/sessions/current`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });
        setSessionId(response.data.session_id);
      } catch (error) {
        console.error('Error getting session id:', error);
      }
    }
  
    // Get the messages from the backend
    const getMessages = async () => {
      try {
        console.log('Getting initial messages...');
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/sessions/${sessionId}/messages`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });
        setChatMessages(response.data.messages);
      } catch (error) {
        console.error('Error getting messages:', error);
      }
    }

    // Get the user id from the backend
    useEffect(() => {
      const getUserId = async () => {
        try {
          const { data, error } = await supabase.auth.getSession();
          if (error) {
            throw error;
          }
          console.log('User id:', data.session?.user.id);
          console.log('Access token:', data.session?.access_token);
          setUserId(data.session?.user.id || null);
          setAccessToken(data.session?.access_token || null);
        } catch (error) {
          console.error('Error getting user id:', error);
        }
      }
      getUserId();
    }, []);

  
    useEffect(() => {
      console.log('begingging userId:', userId);
      console.log('begingging accessToken:', accessToken);
      if (userId && accessToken) {
        getSessionId();
      }
    }, [userId, accessToken]);
  
    useEffect(() => {
      if (sessionId) {
        getMessages();
      }
    }, [sessionId]);
  
    // Updates the current list of messages after user clicks button
    const handleSend = async () => {
      if (inputValue.trim() === '') return;
      setIsLoading(true);
      setIsDisabled(true);
      // Update Current list of messages
      setChatMessages([...chatMessages, {type: 'user', content: inputValue}]);
      // Clear current input state
      setInputValue('');
  
      try {
        // Send the message to the backend
        const response = await axios.post('http://127.0.0.1:8000/api/v1/chat', {
          session_id: sessionId,
          messages: [...chatMessages, {type: 'user', content: inputValue}],
        }, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });
          console.log(response.data);
          setChatMessages(prev => [...prev, {type: 'assistant', content: response.data.response_message.content}]);
          setIsLoading(false);
          setIsDisabled(false);
      } catch (error) {
        console.error('Error sending message to backend:', error);
        setIsLoading(false);
        setIsDisabled(false);
      }
    }
    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        setDocumentUpload(file);
        console.log('File selected:', file);
      }
    }
    
    const handleUploadDocument = async () => {
      if (!documentUpload) {
        console.error('No file selected');
        return;
      }

      const formData = new FormData();
      formData.append('file', documentUpload);

      try {
        const response = await axios.post('http://127.0.0.1:8000/api/v1/documents/upload', formData, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log("Upload document response:", response.data);
        alert(`Document uploaded successfully! ${response.data.chunks_created} chunks created`);

        // Refresh file input
        setDocumentUpload(null);


      } catch (error) {
        console.error('Error uploading document:', error);
        alert('Error uploading document. Please try again.');
      }
      setIsDisabled(false);
    } 
  
    const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
      setInputValue(event.target.value);
    }
  
  
    return (
      <>
        <div className="app-container bg-red-200">
          <AppName>
            <h1>ThreadWeaver</h1>
          </AppName>
        </div>
        
        <Headings>
          <p>ThreadWeaver is a tool that helps you work seamlessly across Slack, Notion, and WhatsApp Business.</p>
        </Headings>
  
        <div className="chat-container bg-green-200">
          <Chat>
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
          </Chat>
        </div>
  
        <div className="search-bar-container flex justify-center">
          <QueryBar>
            <input type="file" accept=".txt" onChange={handleFileSelect} />
            <Button textContent='Upload Document' handleClick={handleUploadDocument} disabled={isDisabled} />
            <textarea className="query-input" placeholder="Enter your query" value={inputValue} onChange={handleInputChange} />       
            <Button textContent='Send' handleClick={handleSend} disabled={isDisabled} />
          </QueryBar>
        </div>
      </>
    )
  }

export default ChatPage;