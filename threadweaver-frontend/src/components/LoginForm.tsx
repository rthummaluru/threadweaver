import React, { ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

const LoginForm = ({ children }: Props) => {
    return (
        <form className="login-form flex flex-col gap-2 w-half max-w-md">
            {children}
        </form>
    )
}

export default LoginForm;