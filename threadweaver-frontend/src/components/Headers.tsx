import React, { ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

const Headings = ({ children }: Props) => {
    return (
        <div className="headings text-center">
            {children}
        </div>
    )
}

export default Headings;