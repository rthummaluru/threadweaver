import Button from '../components/Button';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const handleLoginWithEmail = () => {
    console.log('Login with email');
}

const LoginPage = () => {
    return (
        <>
        <div className="login-container flex flex-col items-center justify-center h-screen">
            <h1>Login</h1>
            <form className="login-form flex flex-col gap-2 w-half max-w-md">
                <input type="email" placeholder="Email" />
                <input type="password" placeholder="Password" />
                <Button textContent="Login" handleClick={handleLoginWithEmail} />
            </form>
        </div>
        </>
    )
}

export default LoginPage;