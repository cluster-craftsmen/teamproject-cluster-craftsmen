import React, { useState } from "react";
import { Button } from '@mantine/core';
import { Notification, rem } from '@mantine/core';
import { IconCheck, IconX } from '@tabler/icons-react';



export default function ResetData() {

    const [submitSuccess, setSubmitSuccess] = useState(false);
    const [submitError, setSubmitError] = useState<null | string>(null);



    const resetData = async () => {
        try {
            const response = await fetch('/api/reset_data');
            if (response.ok) {
                setSubmitSuccess(true);
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
    };

    const xIcon = <IconX style={{ width: rem(20), height: rem(20) }} />;
    const checkIcon = <IconCheck style={{ width: rem(20), height: rem(20) }} />;

    return (
        <>
            <Button variant="filled" onClick={resetData}>Reset Data</Button>
            {submitSuccess && (
                <Notification
                    icon={checkIcon}
                    color="teal"
                    onClose={clearNotification}
                >
                    Data reset has been done successfully
                </Notification>
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
        </>
    )
}