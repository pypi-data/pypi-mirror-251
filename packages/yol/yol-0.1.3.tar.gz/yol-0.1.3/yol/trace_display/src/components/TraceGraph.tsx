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
 * TraceGraph Component
 *
 * This component visualizes a function trace in a graphical format. The data representation
 * utilizes nodes to depict function calls and edges to show relationships between calls.
 * Each node contains information about a function call like its name, arguments, return value, and latency.
 * Edges establish parent-child relationships between function calls.
 *
 * The data is processed from a structured JSON, which gets converted into nodes and edges compatible with the ReactFlow library.
 *
 * Components:
 * - TraceGraph: The primary component which integrates the processed data into ReactFlow for visualization.
 * - TraceGraphNode: A custom node visualization for the graph.
 *
 * Dependencies:
 * - react-flow-renderer: Provides the graphical flow visualization.
 */

import React, { useState, useEffect, useMemo, useCallback } from "react";
import ReactFlow, { Background, BezierEdge } from "react-flow-renderer";
import TraceGraphNode from "./TraceGraphNode";
import dagre from "dagre";

// Interfaces and Types

// Represents a structured data about a function call.
export interface FunctionNode {
  id: string;
  parentId: string | undefined;
  position: { x: number; y: number };
  function_name: string; // Name of the function.
  args: Record<string, any>; // Arguments passed to the function.
  kwargs: Record<string, any>; // Keyword arguments passed to the function.
  thread_id: number; // ID of the thread where the function was executed.
  thread_name: string; // Name of the thread where the function was executed (may be specified by the user or python default).
  children: FunctionNode[]; // Child function calls made from within this function.
  return: any; // Return value of the function.
  latency: number; // Time taken for function execution.
  source_code: string; // Source code of the function.
  execution_order: number;
  return_type: string; // Type of return value of the function.
  occurrence: number; // Position of the function in repeated calls
  repeats: number; // Number of repeats for a particular function
  handleNodeNavigation: (
    // Function to handle node navigation
    position: number,
    direction: string,
    function_name: string,
    parentId: string | undefined
  ) => void;
}

// Holds the formatted data for a node.
interface NodeData {
  position: { x: number; y: number };
  id: string;
  function_name: string;
  args: any;
  return: any;
  source_code: string;
  thread_id: number;
  latency: string;
  return_type: string;
  occurrence: number;
  repeats: number;
  parentId: string | undefined;
  handleNodeNavigation: (
    position: number,
    direction: string,
    function_name: string,
    parentId: string
  ) => void;
}

// Represents a visual node in the graph.
interface Node {
  id: string; // Unique ID for the node.
  parentId: string | undefined;
  type: string; // Type of the node, used for custom visualization.
  data: NodeData; // Formatted data displayed on the node.
  position: { x: number; y: number }; // Position of the node in the graph.
}

// Represents a visual edge/connection between nodes in the graph.
interface Edge {
  id: string; // Unique ID for the edge.
  source: string; // ID of the source node.
  target: string; // ID of the target node.
  animated: boolean; // Animation for the edge.
  label?: string;
  style?: { strokeWidth: number; stroke: string };
  labelStyle?: { fontSize: string };
}

// Represents the state of elements (both nodes and edges).
// Also contains a map for keeping state of repeated nodes.
interface ElementState {
  nodes: Node[];
  edges: Edge[];
  lastGraphState: Map<string, Number>;
}

// Required args for converting nodes to repeated node structure.
export interface ConvertToRepeatedCallsArgs {
  occurrence: number;
  direction: string;
  function_name: string;
  parentId: string | undefined;
}

const nodeTypes = {
  traceGraphNode: TraceGraphNode, // Custom node visualization.
};

const edgeTypes = {
  customEdge: BezierEdge,
};

/**
 * Formats the raw function node data into a structured label for display.
 *
 * @param nodeData - Raw function data that needs to be formatted.
 * @returns The formatted data suitable for the graph node.
 */
const formatFunctionNodeLabel = (nodeData: FunctionNode): NodeData => {
  const formattedLatency = nodeData.latency
    ? `${nodeData.latency.toFixed(3)}ms`
    : "";

  return {
    position: nodeData.position,
    id: nodeData.id,
    parentId: nodeData.parentId,
    function_name: nodeData.function_name,
    args: nodeData.args,
    return: nodeData.return,
    source_code: nodeData.source_code,
    thread_id: nodeData.thread_id,
    latency: formattedLatency,
    return_type: nodeData.return_type,
    repeats: nodeData.repeats,
    occurrence: nodeData.occurrence,
    handleNodeNavigation: nodeData.handleNodeNavigation,
  };
};

/**
 * Converts the provided JSON data into nodes and edges for the graph.
 *
 * @param jsonData - The raw function trace data.
 * @returns Nodes and edges structured for ReactFlow.
 */

// Define a type for the layout direction as a union of possible string literals
type LayoutDirection = "TB" | "BT" | "LR" | "RL";

const applyGraphLayout = (
  { nodes, edges, lastGraphState }: ElementState,
  direction: LayoutDirection = "TB"
) => {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: direction });
  g.setDefaultEdgeLabel(() => ({}));

  nodes.forEach((node) => {
    // Assuming each node has a fixed width and height for simplicity
    g.setNode(node.id, { width: 300, height: 450 });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const layoutedNodes: Node[] = nodes.map((node) => {
    const nodeWithLayout = g.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithLayout.x - nodeWithLayout.width / 2,
        y: nodeWithLayout.y - nodeWithLayout.height / 2,
      },
    };
  });

  // No changes needed for the edges, but they are returned to keep the function signature consistent
  return {
    nodes: layoutedNodes,
    edges: edges,
    lastGraphState: lastGraphState,
  };
};

export const getColorForThread = (threadId: number): string => {
  let colors = [
    "#b33c39",
    "#ffd966",
    "#ff7f50",
    "#38783e",
    "#711DB0",
    "#384f78",
    "#C21292",
    "#BED754",
    "#E0AED0",
    "#163020",
    // ... Add more colors as needed
  ];
  // Create a hash-like value from the threadId
  let hash = 0;
  const idString = threadId.toString();
  for (let i = 0; i < idString.length; i++) {
    hash = (hash << 5) - hash + idString.charCodeAt(i);
    hash = hash & hash; // Convert to 32bit integer
  }
  hash = Math.abs(hash); // Ensure it's a positive number

  return colors[hash % colors.length]; // Using the hash value for color selection
};
const convertToNodeStructure = (
  jsonData: FunctionNode,
  handleNodeNavigation: (
    position: number,
    direction: string,
    function_name: string,
    parentId: string
  ) => void
): ElementState => {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const graphState: Map<string, Number> = new Map<string, Number>();
  const queue: {
    node: FunctionNode;
    parentId?: string;
    depth: number;
    xOffset: number;
  }[] = [{ node: jsonData, depth: 0, xOffset: 0 }];

  let idCounter = 1;
  let xSpacing = 700; // horizontal space between nodes

  while (queue.length) {
    const { node, parentId, depth, xOffset } = queue.shift()!;
    const nodeId = `node-${idCounter++}`;
    node.id = nodeId;
    node.parentId = parentId;
    node.position = { x: xOffset, y: depth * 500 };
    nodes.push({
      id: nodeId,
      parentId: parentId,
      type: "traceGraphNode",
      data: formatFunctionNodeLabel(node),
      position: { x: xOffset, y: depth * 500 },
    });
    if (parentId) {
      edges.push({
        id: `edge-${parentId}-${nodeId}`,
        source: parentId,
        target: nodeId,
        animated: true,
        label: `${node.execution_order}`,
        style: { strokeWidth: 8, stroke: getColorForThread(node.thread_id) },
        labelStyle: { fontSize: "1.7em" },
      });
    }

    node.children.forEach((child, index) =>
      queue.push({
        node: child,
        parentId: nodeId,
        depth: depth + 1,
        xOffset: xOffset + (index - (node.children.length - 1) / 2) * xSpacing,
      })
    );
  }

  const nodesWithHandlers = nodes.map((node: Node) => ({
    ...node,
    data: {
      ...node.data,
      handleNodeNavigation,
    },
  }));

  return {
    nodes: nodesWithHandlers,
    edges,
    lastGraphState: graphState,
  };
};

/**
 * Converts the provided nodes and edges that came from convertToNodeStructure function into the repeated calls structure.
 * It first identifies repeated calls from function name and parent id.
 * It then finds the next function to navigate to based on the occurrence and direction and pushes that to newNodes.
 * If we are in initialization, it shows first occurrence for every repeated node.
 * If not in initialization, it computes the nodes that are affected by this move and pushes them.
 * The ones that are not affected are added from the lastGraphState.
 * Lastly it computes newEdges from newNodes.
 *
 * @param ElementState - Nodes and edges structured for ReactFlow. Also an empty graphState map.
 * @param ConvertToRepeatedCallsArgs - Arguments for computing the necessary navigation which are obtained from TraceGraphNode.
 * @param initialization - Initialization flag to determine whether a navigation is happening or a new jsonData has came.
 * @returns Nodes and edges structured to represent repeated calls. Also nextGraphState map to keep track of repeated nodes.
 */
const convertToRepeatedCalls = (
  { nodes, edges, lastGraphState }: ElementState,
  {
    occurrence,
    direction,
    function_name,
    parentId,
  }: ConvertToRepeatedCallsArgs,
  initialization: boolean
): ElementState => {
  const newNodes: Node[] = [];
  const newEdges: Edge[] = [];
  const repeatMap: Map<string, Node[]> = new Map<string, Node[]>();
  const nextGraphState: Map<string, Number> = new Map<string, Number>();

  for (let [key, value] of lastGraphState) {
    nextGraphState.set(key, value);
  }

  // Populating the map of repeated nodes
  nodes.forEach((node) => {
    const identifier = `${node.data.function_name}-from-${node.parentId}`;

    if (repeatMap.has(identifier)) {
      repeatMap.get(identifier)!.push(node);
    } else {
      repeatMap.set(identifier, [node]);
    }
  });

  // Getting the function we are navigating to
  // If the arguments passed are invalid, we navigate to the first node which is the main function
  // This is the case when we are initializing the graph
  let nextNavNode: Node;
  const prevNavId = `${function_name}-from-${parentId}`;
  if (repeatMap.has(prevNavId)) {
    const navRepeatedNodes = repeatMap.get(prevNavId)!;

    if (direction == "r") {
      nextNavNode = navRepeatedNodes[occurrence % navRepeatedNodes.length];
    } else if (direction == "l") {
      nextNavNode =
        navRepeatedNodes[
          (occurrence - 2 + navRepeatedNodes.length) % navRepeatedNodes.length
        ];
    } else {
      nextNavNode = nodes[0];
    }
  } else {
    nextNavNode = nodes[0];
  }

  newNodes.push(nextNavNode);

  if (initialization) {
    repeatMap.forEach((repeatedNodes, identifier) => {
      let i = 1;
      repeatedNodes.forEach((repeatedNode: Node) => {
        repeatedNode.data.occurrence = i;
        repeatedNode.data.repeats = repeatedNodes.length;
        i++;
        if (
          (repeatedNode !== nextNavNode &&
            newNodes.some((node) => node.id === repeatedNode.parentId) &&
            !newNodes.some(
              (node) =>
                node.parentId === repeatedNode.parentId &&
                node.data.function_name === repeatedNode.data.function_name
            )) ||
          repeatedNode.parentId === undefined
        ) {
          if (!newNodes.includes(repeatedNode)) {
            newNodes.push(repeatedNode);
          }
        } else {
        }
      });
    });

    newNodes.forEach((node) => {
      const identifier = `${node.data.function_name}-from-${node.parentId}`;
      nextGraphState.set(identifier, 1);
      edges.forEach((edge) => {
        if (
          node.id === edge.target &&
          newNodes.some((node) => node.id === edge.source)
        ) {
          const updatedEdge = { ...edge };
          updatedEdge.target = node.id;
          newEdges.push(updatedEdge);
        }
      });
    });

    return {
      nodes: newNodes,
      edges: newEdges,
      lastGraphState: nextGraphState,
    };
  } else {
    // A quick run through to initialize the occurrence and repeats of each node
    // As they get lost in the process of converting to repeated calls
    repeatMap.forEach((repeatedNodes, identifier) => {
      let i = 1;
      repeatedNodes.forEach((repeatedNode: Node) => {
        repeatedNode.data.occurrence = i;
        repeatedNode.data.repeats = repeatedNodes.length;
        i++;
      });
    });

    // Keep track of nodes that are affected by the navigation
    const negAffectedNodes: Node[] = [];
    const posEffectedNodes: Node[] = [];

    const dropQueue: Node[] = [];
    dropQueue.push(repeatMap.get(prevNavId)![occurrence - 1]);
    while (dropQueue.length) {
      const popNode = dropQueue.shift()!;
      nodes.forEach((node) => {
        if (node.parentId === popNode.id) {
          negAffectedNodes.push(node);
          dropQueue.push(node);
        }
      });
    }
    negAffectedNodes.forEach((node) => {
      const badlyIdentifier = `${node.data.function_name}-from-${node.parentId}`;
      nextGraphState.set(badlyIdentifier, -1);
    });

    const addQueue: Node[] = [];
    addQueue.push(nextNavNode);
    while (addQueue.length) {
      const popNode = addQueue.shift()!;
      nodes.forEach((node) => {
        if (node.parentId === popNode.id) {
          posEffectedNodes.push(node);
          addQueue.push(node);
        }
      });
    }
    posEffectedNodes.forEach((node) => {
      const goodlyIdentifier = `${node.data.function_name}-from-${node.parentId}`;
      nextGraphState.set(goodlyIdentifier, 1);
    });

    nextGraphState.set(prevNavId, nextNavNode.data.occurrence);

    nextGraphState.forEach((value, key) => {
      if (value !== -1) {
        newNodes.push(repeatMap.get(key)![Number(value) - 1]);
      }
    });

    // Remove the first new node -the one we are navigating to- as it's pushed again
    // We are doing this to keep the order of the nodes
    newNodes.shift();

    newNodes.forEach((node) => {
      edges.forEach((edge) => {
        if (
          node.id === edge.target &&
          newNodes.some((node) => node.id === edge.source)
        ) {
          const updatedEdge = { ...edge };
          updatedEdge.target = node.id;
          newEdges.push(updatedEdge);
        }
      });
    });

    return {
      nodes: newNodes,
      edges: newEdges,
      lastGraphState: nextGraphState,
    };
  }
};

const TraceGraph: React.FC<{ jsonData: FunctionNode }> = ({ jsonData }) => {
  // useMemo was necessary as the graph was updating itself on every render
  const jsonDataString = useMemo(() => JSON.stringify(jsonData), [jsonData]);

  // This function is passed to TraceGraphNode to handle node navigation
  const handleNodeNavigation = (
    occurrence: number,
    direction: string,
    function_name: string,
    parentId: string | undefined
  ) => {
    elements.lastGraphState = elementsRef.current?.lastGraphState!;

    const convertedState = convertToNodeStructure(
      jsonData,
      handleNodeNavigation
    );
    convertedState.lastGraphState = elements.lastGraphState;

    const args: ConvertToRepeatedCallsArgs = {
      occurrence,
      direction,
      function_name,
      parentId,
    };

    const repeatedState = convertToRepeatedCalls(convertedState, args, false);
    const layoutedState = applyGraphLayout(repeatedState);

    setElements(layoutedState);
  };

  // useCallback was necessary as the element state was resetting itself on every render
  const initializeElements = useCallback(
    (jsonData: FunctionNode) => {
      const convertedState = convertToNodeStructure(
        jsonData,
        handleNodeNavigation
      );

      const args: ConvertToRepeatedCallsArgs = {
        occurrence: -1,
        direction: "None",
        function_name: "-1",
        parentId: "-1",
      };

      const repeatedState = convertToRepeatedCalls(convertedState, args, true);

      const layoutedState = applyGraphLayout(repeatedState);

      return layoutedState;
    },
    [jsonDataString]
  );

  const [elements, setElements] = useState<ElementState>(() =>
    initializeElements(jsonData)
  );
  const elementsRef = React.useRef<ElementState>();
  elementsRef.current = elements;

  useEffect(() => {
    elementsRef.current = elements;
  }, [elements]);

  useEffect(() => {
    const layoutedState = initializeElements(jsonData);
    setElements(layoutedState);
  }, [jsonDataString]);

  return (
    <div style={{ height: "90vh" }}>
      <ReactFlow
        nodes={elements.nodes}
        edges={elements.edges}
        fitView={true}
        attributionPosition="bottom-right"
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
      >
        <Background color="#aaa" gap={16} />
      </ReactFlow>
    </div>
  );
};

export default TraceGraph;
