import React, { ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

const QueryBar = ({ children }: Props) => {
    return (
        <div className="search-bar">
            {children}
        </div>
    )
}

export default QueryBar;