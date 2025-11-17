import React, { ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

const QueryBar = ({ children }: Props) => {
    return (
        <div className="search-bar flex items-end gap-2">
            {children}
        </div>
    )
}

export default QueryBar;