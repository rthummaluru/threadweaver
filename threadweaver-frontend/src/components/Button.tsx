import React, { ReactNode } from 'react';

interface Props {
    textContent: string;
    handleClick: () => void;
    disabled?: boolean;
}

const Button = ({ textContent, handleClick, disabled = false}: Props) => {
    return (
        <button type="submit" onClick={handleClick} disabled={disabled}>
            {textContent}
        </button>
    )
}

export default Button;