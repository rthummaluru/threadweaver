import React, { ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

const SearchBar = ({ children }: Props) => {
    return (
        <div className="search-bar">
            {children}
        </div>
    )
}

export default SearchBar;