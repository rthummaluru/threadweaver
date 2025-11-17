import React, { ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

const Chat = ({ children }: Props) => {
    return (
        <div className="chat flex justify-center items-center max-w-lg mx-auto p-4 m-4">
            <div className="w-full max-w-3xl flex flex-col gap-4">
                {children}
            </div>
        </div>
    )
}

export default Chat;