import Button from '../components/Button';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SignUpForm from '../components/SignUpForm';
import LoginForm from '../components/LoginForm';
import AppName from '../components/AppName';

// const [mode, setMode] = useState<'login' | 'signup'>('login');

const handleLoginWithEmail = () => {
    console.log('Login with email');
}

const handleSignUp = () => {
    console.log('Sign Up');
}


const LoginPage = () => {
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
                        <input type="email" placeholder="Email" />
                        <input type="password" placeholder="Password" />
                        <Button textContent="Sign Up" handleClick={handleSignUp} />
                    </SignUpForm>
                </div>
                <div className="login-form-container flex flex-col items-center justify-center border-2 border-gray-300 rounded-md p-4">
                    <h1>Login</h1>
                        <LoginForm>
                            <input type="email" placeholder="Email" />
                            <input type="password" placeholder="Password" />
                            <Button textContent="Login" handleClick={handleLoginWithEmail} />
                        </LoginForm>
                </div>
            </div>
        </>
    )
}

export default LoginPage;