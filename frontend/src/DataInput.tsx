import { Box, Group, Button } from "@mantine/core";
import { FormEvent } from "react";
import { useChartData } from "./ChartDataContext";

export default function DataInput() {
  const { fetchAndUpdateServerData } = useChartData();

  const onEnterData = async (e: FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("file-input") as HTMLInputElement;

    if (fileInput.files && fileInput.files[0]) {
      formData.append("file", fileInput.files[0]);

      try {
        const response = await fetch("/api/insert_records", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          console.log("File submitted successfully");
          await fetchAndUpdateServerData();
        } else {
          console.error("Error submitting file");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    } else {
      console.error("No file selected");
    }
  };

  return (
    <Box maw={340} mx="auto">
      <form onSubmit={onEnterData}>
        <input type="file" id="file-input" />
        <Group justify="flex-end" mt="md">
          <Button type="submit">Submit File</Button>
        </Group>
      </form>
    </Box>
  );
}
