import React, { useState } from "react";
import { Button } from '@mantine/core';
import { Notification, rem } from '@mantine/core';
import { IconCheck, IconX } from '@tabler/icons-react';
import styles from './ResetData.module.css'; // Import your CSS module

export default function ResetData() {
    const [submitSuccess, setSubmitSuccess] = useState(false);
    const [submitError, setSubmitError] = useState<null | string>(null);
    const [showRunningLine, setShowRunningLine] = useState(false);

    const resetData = async () => {
        try {
            const response = await fetch('/api/reset_data');
            if (response.ok) {
                setSubmitSuccess(true);
                setShowRunningLine(true);

                // Hide success message and running line after 3 seconds
                setTimeout(() => {
                    clearNotification();
                }, 3000);
            } else {
                setSubmitError("Error resetting data");
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    const clearNotification = () => {
        setSubmitSuccess(false);
        setSubmitError(null);
        setShowRunningLine(false);
    };

    const xIcon = <IconX style={{ width: rem(20), height: rem(20) }} />;
    const checkIcon = <IconCheck style={{ width: rem(20), height: rem(20) }} />;

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '10vh' }}>
            <Button variant="filled" onClick={resetData}>Reset Data</Button>
            {submitSuccess && (
                <div style={{ position: 'relative', width: '30%' }}>
                    <Notification
                        icon={checkIcon}
                        color="teal"
                        onClose={clearNotification}
                    >
                        Data reset has been done successfully
                    </Notification>
                    {showRunningLine && (
                        <div className={styles.runningLine}></div>
                    )}
                </div>
            )}

            {submitError && (
                <Notification
                    icon={xIcon}
                    color="red"
                    onClose={clearNotification}
                >
                    {submitError}
                </Notification>
            )}
        </div>
    )
}
