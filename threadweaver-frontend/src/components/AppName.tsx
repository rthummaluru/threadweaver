import React, { ReactNode } from 'react';


interface Props {
    children: ReactNode;
}

const AppName = ({ children }: Props) => {
  return (
    <div className="app-name flex justify-center items-center text-center">
        {children}
    </div>
  )
};

export default AppName;