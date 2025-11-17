import React, { ReactNode } from 'react';

interface Props {
    textContent: string;
    handleClick: () => void;
    disabled?: boolean;
}

const Button = ({ textContent, handleClick, disabled = false}: Props) => {
    return (
        <button type="submit" onClick={handleClick} disabled={disabled} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            {textContent}
        </button>
    )
}

export default Button;