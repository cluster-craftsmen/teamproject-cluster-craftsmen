import React, { useState } from 'react';
import { Switch, Notification } from '@mantine/core';
import { useChartData } from './ChartDataContext';

interface ServerToggleProps {
  serverName: string;
}

const ServerToggle: React.FC<ServerToggleProps> = ({ serverName }) => {
  const [isServerEnabled, setIsServerEnabled] = useState(true);
  const [notification, setNotification] = useState<string | null>(null);
  const [isNotificationVisible, setIsNotificationVisible] = useState(false);
  const { fetchAndUpdateServerData } = useChartData();

  const handleToggle = async () => {
    try {
      if (isNotificationVisible) {
        // If notification is visible, don't toggle
        return;
      }

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
        const action = isServerEnabled ? 'disabled' : 'enabled';
        const message = `Server ${serverName} has been ${action} successfully`;

        setNotification(message);
        setIsNotificationVisible(true);

        // Fetch and update server data after toggling the server
        await fetchAndUpdateServerData();

        setTimeout(() => {
          setNotification(null);
          setIsNotificationVisible(false);
        }, 3000);

        console.log(message);
      } else {
        console.error(`Error toggling server ${serverName}`);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={{ marginBottom: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
        <span style={{ marginRight: '10px' }}>{serverName}</span>
        <Switch
          checked={isServerEnabled}
          onChange={handleToggle}
          color={isServerEnabled ? 'teal' : 'red'}
          disabled={isNotificationVisible}
        />
      </div>
      {notification && (
        <Notification
          title={notification}
          onClose={() => setNotification(null)}
          color={isServerEnabled ? 'teal' : 'red'}
          style={{ marginTop: '10px' }}
        />
      )}
    </div>
  );
};

const ServersList: React.FC = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', height: '15vh' }}>
      <ServerToggle serverName="S1" />
      <ServerToggle serverName="S2" />
      <ServerToggle serverName="S3" />
      <ServerToggle serverName="S4" />
    </div>
  );
};

export default ServersList;
