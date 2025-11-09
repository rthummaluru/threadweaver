import React, { ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

const Headings = ({ children }: Props) => {
    return (
        <div className="headings">
            {children}
        </div>
    )
}

export default Headings;