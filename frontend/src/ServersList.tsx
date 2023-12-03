// import React, { useState, useEffect } from 'react';
// import { Switch, Group } from '@mantine/core';

// const ServerList: React.FC = () => {
//   const [servers, setServers] = useState<string[]>(['server1', 'server2', 'server3', 'server4']);
//   const [serverStatus, setServerStatus] = useState<{ [key: string]: boolean }>({});

//   const addServer = async (serverName: string) => {
//     try {
//       const response = await fetch('/api/add_server', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ server_name: serverName }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to add server');
//       }

//       // Update the local state to reflect the change
//       setServerStatus((prevStatus) => ({
//         ...prevStatus,
//         [serverName]: true,
//       }));
//     } catch (error) {
//       console.error('Error adding server:', error);
//     }
//   };

//   const disableServer = async (serverName: string) => {
//     try {
//       const response = await fetch('/api/disable_server', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ server_name: serverName }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to disable server');
//       }

//       // Update the local state to reflect the change
//       setServerStatus((prevStatus) => ({
//         ...prevStatus,
//         [serverName]: false,
//       }));
//     } catch (error) {
//       console.error('Error disabling server:', error);
//     }
//   };

//   return (
//     <div style={{ textAlign: 'center' }}>
//       <h2>Server List</h2>
//       <Group style={{ display: 'flex', justifyContent: 'center' }}>
//         {servers.map((server) => (
//           <Group key={server} style={{ marginRight: '10px' }}>
//             <div>{server}</div>
//             <Switch
//               size="md" // Adjust the size as needed
//               checked={serverStatus[server] || false} // Ensure it's either true or false
//               onChange={() => (serverStatus[server] ? disableServer(server) : addServer(server))}
//             />
//           </Group>
//         ))}
//       </Group>
//     </div>
//   );
// };

// export default ServerList;


import React, { useState } from 'react';
import { Button, Notification } from '@mantine/core';

interface ServerToggleProps {
  serverName: string;
}

const ServerToggle: React.FC<ServerToggleProps> = ({ serverName }) => {
  const [isServerEnabled, setIsServerEnabled] = useState(true);
  const [notification, setNotification] = useState<string | null>(null);

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
        const action = isServerEnabled ? 'disabled' : 'enabled';
        const message = `Server ${serverName} has been ${action} successfully`;

        setNotification(message);

        console.log(message);
      } else {
        console.error(`Error toggling server ${serverName}`);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleCloseNotification = () => {
    setNotification(null);
  };

  return (
    <div style={{ marginBottom: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
        <span style={{ marginRight: '10px' }}>{serverName}</span>
        <Button onClick={handleToggle} variant={isServerEnabled ? 'filled' : 'light'}>
          {isServerEnabled ? 'Disable' : 'Enable'}
        </Button>
      </div>
      {notification && (
        <Notification
          title={notification}
          onClose={handleCloseNotification}
          color="teal"
          style={{ marginTop: '10px' }} // Adjust the margin top as needed
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

