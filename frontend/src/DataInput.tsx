import { Box, TextInput, Group, Button } from "@mantine/core";
import  { FormEvent } from "react";
import { useChartData } from "./ChartDataContext";

export default function DataInput() {
  const { fetchAndUpdateServerData } = useChartData();

  const onEnterData = async (e: FormEvent) => {
    e.preventDefault();
    const data: any = {
      records_count: +(document.getElementById("count") as HTMLInputElement)
        ?.value,
    };
    try {
      const response = await fetch("/api/insert_records", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        console.log("Data submitted successfully");
        await fetchAndUpdateServerData();
      } else {
        console.error("Error submitting data");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <Box maw={340} mx="auto">
        <form onSubmit={onEnterData}>
          <TextInput
            label="Enter Data Count"
            id="count"
            placeholder="Example: 10000"
          />
          <Group justify="flex-end" mt="md">
            <Button type="submit">Submit</Button>
          </Group>
        </form>
      </Box>
    </>
  );
}
