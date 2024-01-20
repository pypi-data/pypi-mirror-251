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
 * TraceGraphNode Component
 *
 * This component represents a node in the trace graph. Each node displays details
 * about a function call including its name, thread ID, arguments (inputs), return values,
 * source code, and latency. The component utilizes the `react-flow-renderer` library
 * to render each node with handles (connection points) at the top and bottom.
 *
 * The component expects data in the form of a `FunctionNode` object which provides
 * the details to be displayed.
 *
 * The visual styling of the node is defined in the `TraceGraphNode.css` file.
 */

import React, { useState, useContext } from "react";
import { Handle, Position } from "react-flow-renderer";
import { FunctionNode, getColorForThread } from "./TraceGraph";
import InputOutputButton from "./InputOutputButton";
import { Argument, Return } from "../types"; // Import the types
import CodeIcon from "@mui/icons-material/Code";
import InputIcon from "@mui/icons-material/Input";
import VisibilityIcon from "@mui/icons-material/Visibility";
import KeyboardArrowLeftIcon from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRightIcon from "@mui/icons-material/KeyboardArrowRight";

import "./TraceGraphNode.css";
import { TraceGraphContext } from "./TraceGraphContext";

interface TraceGraphNodeProps {
  data: FunctionNode;
}

/**
 * TraceGraphNode Component
 *
 * @param {TraceGraphNodeProps} props - Component props.
 * @param {FunctionNode} props.data - Data object for the node.
 * @returns {JSX.Element} The rendered node.
 */

/*const onNodeDragStop = (event, node) => {
  // Update node positions in your state/context
  updateNodePosition(node.id, { x: node.position.x, y: node.position.y });
};
*/

// Props for the Navigation Bar Component on each node
interface NavBarProps {
  currentIndex: number;
  totalCount: number;
  function_name: string;
  parentId: string | undefined;
  handleNav: (
    occurrence: number,
    direction: string,
    function_name: string,
    parentId: string | undefined
  ) => void;
}

/**
 * Represents the navigation bar component on a trace graph node.
 * @param currentIndex - The current repeated function that the node displays.
 * @param totalCount - The total count of functions for that node.
 * @param function_name - The name of the function.
 * @param parentId - The ID of the parent node.
 * @param handleNav - The function to handle navigation.
 */
const NavBar: React.FC<NavBarProps> = ({
  currentIndex,
  totalCount,
  function_name,
  parentId,
  handleNav,
}) => {
  const handleLeftNav = () => {
    handleNav(currentIndex, "l", function_name, parentId);
  };

  const handleRightNav = () => {
    handleNav(currentIndex, "r", function_name, parentId);
  };

  return (
    <div className="trace-graph-node__nav">
      <button onClick={handleLeftNav}>
        <KeyboardArrowLeftIcon />
      </button>

      <span>{`${currentIndex} / ${totalCount}`}</span>
      <button onClick={handleRightNav}>
        <KeyboardArrowRightIcon />
      </button>
    </div>
  );
};

const argumentFormatter = (object: { [key: string]: any }): Argument[] => {
  return Object.entries(object).map(([key, value]): Argument => {
    let formattedValue = " ";
    if (value === null) {
      formattedValue = "null";
    } else if (Array.isArray(value)) {
      formattedValue = `[${value.map((v) => JSON.stringify(v)).join(", ")}]`;
    } else if (typeof value === "object") {
      const entries = Object.entries(value);
      if (entries.length > 0) {
        formattedValue = `{ ${argumentFormatter(value)
          .map((arg) => `${arg.name}: ${arg.value}`)
          .join(", ")} }`;
      } else {
        formattedValue = "{}";
      }
    } else {
      formattedValue = value.toString();
    }

    return {
      name: key,
      value: formattedValue.replace(/["]/g, ""),
      type: "",
    };
  });
};

const returnFormatter = (
  object: { [key: string]: any },
  return_type: string
): Return[] => {
  return Object.entries(object).map(([key, value]): Return => {
    let formattedValue = " ";
    if (value === null) {
      formattedValue = "null";
    } else if (Array.isArray(value)) {
      formattedValue = `[${value.map((v) => JSON.stringify(v)).join(", ")}]`;
    } else if (typeof value === "object") {
      const entries = Object.entries(value);
      if (entries.length > 0) {
        formattedValue = `{ ${returnFormatter(value, return_type)
          .map((arg) => `${arg.value}`)
          .join(", ")} }`;
      } else {
        formattedValue = "{}";
      }
    } else {
      formattedValue = value.toString();
    }

    return {
      value:
        return_type === "dict" && key
          ? `${key}: ${formattedValue.replace(/["]/g, "")}`
          : formattedValue.replace(/["]/g, ""),
      type: "",
    };
  });
};

const TraceGraphNode: React.FC<TraceGraphNodeProps> = ({ data }) => {
  const context = useContext(TraceGraphContext);
  let inputArguments: Argument[] = [];

  // This code converts data.args to the format compatible with argumentFormatter function
  // From: {name: {value, type}}, to: {name: value}
  const compatibleFormat = Object.entries(data.args).reduce(
    (acc, [name, { value }]) => {
      acc[name] = value;
      return acc;
    },
    {} as Record<string, any>
  );

  if (
    compatibleFormat &&
    typeof compatibleFormat === "object" &&
    !Array.isArray(compatibleFormat)
  ) {
    inputArguments = argumentFormatter(compatibleFormat);
  }

  inputArguments.forEach((argument) => {
    argument.type = data.args[argument.name].type;
  });

  if (!context) {
    throw new Error("TraceGraphNode must be used within a TraceGraphProvider");
  }

  const { showWindow } = context;

  let outputReturns: Return[] = [];
  if (
    data.return &&
    typeof data.return === "object" &&
    !Array.isArray(data.return)
  ) {
    outputReturns = returnFormatter({ "": data.return }, data.return_type);
  } else if (data.return) {
    outputReturns = returnFormatter([data.return], data.return_type);
  }
  outputReturns.forEach((output) => {
    output.type = data.return_type;
  });

  return (
    <>
      <>
        <Handle type="target" position={Position.Top} />
        <div className="trace-graph-node">
          <div className="trace-graph-node__title-nav-container">
            <div className="trace-graph-node__title">
              <div
                className="trace-graph-node__color-box"
                style={{ backgroundColor: getColorForThread(data.thread_id) }}
              ></div>
              <span className="trace-graph-node__title-text">
                <strong>{data.function_name}</strong>
              </span>
              {data.repeats !== 1 && (
                <NavBar
                  currentIndex={data.occurrence}
                  totalCount={data.repeats}
                  function_name={data.function_name}
                  parentId={data.parentId}
                  handleNav={data.handleNodeNavigation}
                />
              )}
            </div>
          </div>
          <div className="trace-graph-node__inputs-button">
            <InputOutputButton
              type="Input"
              data={inputArguments}
              icon={<InputIcon />}
              onClick={() => showWindow(data.id.toString(), "Input", data)} // Pass onClick handler
            />
          </div>

          <div className="trace-graph-node__return-button">
            <InputOutputButton
              type="Output"
              data={outputReturns}
              icon={<VisibilityIcon />}
              onClick={() => showWindow(data.id.toString(), "Output", data)} // Pass onClick handler
            />
          </div>

          <div className="trace-graph-node__code-latency-container">
            <div className="trace-graph-node__code">
              <button
                className="trace-graph-node__code-button"
                onClick={() => showWindow(data.id.toString(), "Code", data)}
              >
                <CodeIcon className="trace-graph-node__code-button-icon" />
                <span className="trace-graph-node__code-button-text">
                  <strong>Code</strong>
                </span>
              </button>
            </div>
            <div className="trace-graph-node__latency">
              <span className="trace-graph-node__latency-value">
                {" " + data.latency}
              </span>
            </div>
          </div>
        </div>

        <Handle type="source" position={Position.Bottom} id="a" />
      </>
    </>
  );
};

export default TraceGraphNode;
