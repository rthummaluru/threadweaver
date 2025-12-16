import React, { ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

const SignUpForm = ({ children }: Props) => {
    return (
        <form className="signup-form flex flex-col gap-2 w-half max-w-md">
            {children}
        </form>
    )
}

export default SignUpForm;