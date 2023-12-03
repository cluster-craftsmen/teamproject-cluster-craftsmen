import React, { useState } from "react";
import { Button, Notification, rem } from "@mantine/core";
import { IconCheck, IconX } from "@tabler/icons-react";
import { useChartData } from "./ChartDataContext";
import styles from "./ResetData.module.css";

export default function ResetData() {
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [submitError, setSubmitError] = useState<null | string>(null);
  const [showRunningLine, setShowRunningLine] = useState(false);
  const { fetchAndUpdateServerData } = useChartData();

  const resetData = async () => {
    try {
      const response = await fetch("/api/reset_data");
      if (response.ok) {
        setSubmitSuccess(true);
        setShowRunningLine(true);
        await fetchAndUpdateServerData();

        setTimeout(() => {
          setSubmitSuccess(false);
          setShowRunningLine(false);
        }, 3000);
      } else {
        setSubmitError("Error resetting data");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const xIcon = <IconX style={{ width: rem(20), height: rem(20) }} />;
  const checkIcon = <IconCheck style={{ width: rem(20), height: rem(20) }} />;

  const clearNotification = () => {
    setSubmitSuccess(false);
    setSubmitError(null);
    setShowRunningLine(false);
};

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "10vh",
      }}
    >
      <Button variant="filled" onClick={resetData}>
        Reset Data
      </Button>
      {submitSuccess && (
        <div style={{ position: "relative", width: "30%" }}>
          <Notification
            icon={checkIcon}
            color="teal"
            onClose={clearNotification}
          >
            Data reset has been done successfully
          </Notification>
          {showRunningLine && <div className={styles.runningLine}></div>}
        </div>
      )}

      {submitError && (
        <Notification icon={xIcon} color="red" onClose={clearNotification}>
          {submitError}
        </Notification>
      )}
    </div>
  );
}
