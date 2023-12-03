import React, { useState } from 'react';
import { Button } from '@mantine/core';

interface ServerToggleProps {
  serverName: string;
}

const ServerToggle: React.FC<ServerToggleProps> = ({ serverName }) => {
  const [isServerEnabled, setIsServerEnabled] = useState(true);

  const handleToggle = async () => {
    try {
      const apiUrl = isServerEnabled ? '/api/disable_server' : '/api/add_server';
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ server_name: serverName }),
      });

      if (response.ok) {
        setIsServerEnabled(!isServerEnabled);
        console.log(`Server ${serverName} ${isServerEnabled ? 'disabled' : 'enabled'} successfully`);
      } else {
        console.error(`Error toggling server ${serverName}`);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
      <span style={{ marginRight: '10px' }}>{serverName}</span>
      <Button onClick={handleToggle} variant={isServerEnabled ? 'filled' : 'light'}>
        {isServerEnabled ? 'Disable' : 'Enable'}
      </Button>
    </div>
  );
};

const ServersList: React.FC = () => {
  return (
    <div>
      <ServerToggle serverName="s1" />
      <ServerToggle serverName="s2" />
      <ServerToggle serverName="s3" />
      <ServerToggle serverName="s4" />
    </div>
  );
};

export default ServersList;
