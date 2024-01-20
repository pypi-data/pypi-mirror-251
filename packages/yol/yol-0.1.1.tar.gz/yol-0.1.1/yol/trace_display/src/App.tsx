/*
Copyright 2023 NeuralBridge AI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 */

/**
 * App Component
 *
 * This is the main application component. It fetches trace data from the `/trace` endpoint,
 * processes the fetched data, and displays it using the TraceGraph component. The component
 * also renders a Header and a Footer.
 *
 * The main data transformation function (`transformJsonToFunctionNode`) recursively processes the
 * fetched data to match the expected format for the TraceGraph component.
 */

import React, { useState, useEffect } from "react";
import TraceGraph from "./components/TraceGraph";
import Header from "./components/Header";
import Footer from "./components/Footer";
import ThreadLegend from "./components/ThreadLegend";
import { FunctionNode, getColorForThread } from "./components/TraceGraph";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { TraceGraphProvider } from "./components/TraceGraphContext";
import NodeWindows from "./components/NodeWindows";
import { set } from "react-hook-form";

/**
 * transformJsonToFunctionNode
 * Transforms the given JSON data into the FunctionNode format suitable for the TraceGraph.
 *
 * @param {FunctionNode} json - The data object to be transformed.
 * @returns {FunctionNode} - The transformed data object.
 */
let execution_counter = 0;
const transformJsonToFunctionNode = (json: FunctionNode): FunctionNode => {
  return {
    position: { x: 0, y: 0 },
    id: "",
    parentId: "",
    function_name: json.function_name,
    args: json.args || [], // Provide an empty array if undefined
    kwargs: json.kwargs || {}, // Provide an empty object if undefined
    thread_id: json.thread_id,
    thread_name: json.thread_name,
    // Recursively transform children nodes
    execution_order: execution_counter++,
    children: json.children?.map(transformJsonToFunctionNode) || [],
    return: json.return,
    latency: json.latency,
    source_code: json.source_code,
    return_type: json.return_type,
    occurrence: 0,
    repeats: 0,
    handleNodeNavigation(): void {},
  };
};

interface ThreadInfo {
  id: number;
  name: string;
}

/**
 * Extracts thread IDs and names from a FunctionNode recursively.
 * @param {FunctionNode} node The FunctionNode to extract thread information from.
 * @returns {ThreadInfo[]} An array of ThreadInfo objects containing the extracted thread IDs and names.
 */
const extractThreadIdsAndNames = (node: FunctionNode): ThreadInfo[] => {
  let threadInfo: ThreadInfo[] = [];

  const traverse = (node: FunctionNode) => {
    if (!threadInfo.some((info) => info.id === node.thread_id)) {
      threadInfo.push({ id: node.thread_id, name: node.thread_name });
    }

    if (node.children) {
      for (let child of node.children) {
        traverse(child);
      }
    }
  };

  traverse(node);

  return threadInfo;
};

const POLL_INTERVAL = 100; // Tnterval to poll newly generated trace data in milliseconds

const App: React.FC = () => {
  // State to hold the processed trace data
  const [traceData, setTraceData] = useState<FunctionNode[]>([]);
  const [threadInfo, setThreadInfo] = useState<ThreadInfo[]>([]);

  // Fetch trace data when the component mounts
  useEffect(() => {
    const fetchTraceData = () => {
      execution_counter = 0; // Included so that the execution counter is resetted after each fetch
      fetch("/trace")
        .then((response) => response.json())
        .then((data: FunctionNode[]) => {
          // Transform each data item
          const transformedData = data.map(transformJsonToFunctionNode);
          setTraceData(transformedData);

          const threadInfo = transformedData.flatMap(extractThreadIdsAndNames);
          setThreadInfo(threadInfo);
        })
        .catch((error) => console.error("Error fetching trace data:", error));
    };

    fetchTraceData(); // Initial Fetch

    const intervalId = setInterval(fetchTraceData, POLL_INTERVAL);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <ThemeProvider theme={createTheme()}>
      <div>
        <Header />
        <ThreadLegend
          threadIds={threadInfo.map((info) => info.id)}
          threadNames={threadInfo.map((info) => info.name)}
          getColorForThread={getColorForThread}
        />
        <TraceGraphProvider>
          <NodeWindows />
          {traceData.map((item, index) => (
            <TraceGraph key={index} jsonData={item} />
          ))}
        </TraceGraphProvider>
        {/* Render a TraceGraph for each trace data item */}
        <Footer />
      </div>
    </ThemeProvider>
  );
};

export default App;
