import Button from '../components/Button';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import SignUpForm from '../components/SignUpForm';
import LoginForm from '../components/LoginForm';
import AppName from '../components/AppName';

import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_DEFAULT_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);


const LoginPage = () => {
    // const [mode, setMode] = useState<'login' | 'signup'>('login');
    const navigate = useNavigate();

    // State to manage setup email and password
    const [setupEmail, setSetupEmail] = useState<string>('');
    const [setupPassword, setSetupPassword] = useState<string>('');

    // State to manage login email and password
    const [loginEmail, setLoginEmail] = useState<string>('');
    const [loginPassword, setLoginPassword] = useState<string>('');

    //
    const handleLoginWithEmail = async (event) => {
       // event.preventDefault();
        try {
            const { data, error } = await supabase.auth.signInWithPassword({
                email: loginEmail,
                password: loginPassword,
            });
            if (error) {
                throw error;
            }
            console.log('Login successful:', data);
            navigate('/chat');
        } catch (error) {
            console.error('Error logging in:', error);
            alert('Error logging in. Please try again.');
        }
    }

    // Handle sign up
    const handleSignUp = async (event) => {
       // event.preventDefault();
        try {
            const { data, error } = await supabase.auth.signUp({
                email: setupEmail,
                password: setupPassword,
                options: {
                    emailRedirectTo: 'http://localhost:5173/chat',
                },
            });
            console.log('Sign up data:', data);
            navigate('/chat');
            if (error) {
                throw error;
            }
            console.log('Sign up successful:', data);
        } catch (error) {
            console.error('Error signing up:', error);
            alert('Error signing up. Please try again.');
        }
    }
    return (
        <>
            <div className='app-name-container flex items-center justify-center'>
                <AppName>
                    <h1>ThreadWeaver</h1>
                </AppName>
            </div>
            <div className='login-page-container flex flex-row items-center justify-center align-middle h-screen border-2 border-gray-300 rounded-md p-4'>
                <div className='signup-form-container flex flex-col items-center justify-center border-2 border-gray-300 rounded-md p-4'>
                    <h1>Sign Up</h1>
                    <SignUpForm>
                        <input type="email" placeholder="Email" value={setupEmail} onChange={(e) => setSetupEmail(e.target.value)} />
                        <input type="password" placeholder="Password" value={setupPassword} onChange={(e) => setSetupPassword(e.target.value)} />
                        <Button textContent="Sign Up" handleClick={handleSignUp} />
                    </SignUpForm>
                </div>
                <div className="login-form-container flex flex-col items-center justify-center border-2 border-gray-300 rounded-md p-4">
                    <h1>Login</h1>
                        <LoginForm>
                            <input type="email" placeholder="Email" value={loginEmail} onChange={(e) => setLoginEmail(e.target.value)} />
                            <input type="password" placeholder="Password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} />
                            <Button textContent="Login" handleClick={handleLoginWithEmail} />
                        </LoginForm>
                </div>
            </div>
        </>
    )
}

export default LoginPage;