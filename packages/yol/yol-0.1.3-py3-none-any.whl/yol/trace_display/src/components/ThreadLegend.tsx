import React from "react";
import "./ThreadLegend.css";

interface ThreadLegendProps {
  threadIds: number[];
  threadNames: string[];
  getColorForThread: (threadId: number) => string;
}

const ThreadLegend: React.FC<ThreadLegendProps> = ({
  threadIds,
  threadNames,
  getColorForThread,
}) => {
  return (
    <div className="thread-legend">
      <div className="thread-legend__title">Threads</div>
      {threadIds.map((threadId, index) => (
        <div key={threadId} className="thread-legend__item">
          <div
            className="thread-legend__color"
            style={{ backgroundColor: getColorForThread(threadId) }}
          />
          <div className="thread-legend__label">
            <strong>ID:</strong> {threadId} | <strong>Name:</strong> {threadNames[index]}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ThreadLegend;
