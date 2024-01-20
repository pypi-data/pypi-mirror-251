import React, { useState, useEffect } from "react";
import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";
import "./VersionCheck.css";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

const VersionCheck: React.FC = () => {
  const [versionInfo, setVersionInfo] = useState({
    current_version: "",
    latest_version: "",
    message: "",
  });

  useEffect(() => {
    fetch("/check-version")
      .then((response) => response.json())
      .then((data) => {
        setVersionInfo(data);
      })
      .catch((error) => console.error("Error checking version:", error));
  }, []);

  if (
    versionInfo.current_version &&
    versionInfo.latest_version !== versionInfo.current_version
  ) {
    return (
      <Alert
        severity="warning"
        className="versionCheck__alert versionCheck__alert--warning"
      >
        {versionInfo.message} -
        <Button
          color="inherit"
          className="versionCheck__button"
          onClick={() =>
            navigator.clipboard.writeText("pip install --upgrade yol")
          }
        >
          {/* Icon before the text */}
          <span className="versionCheck__command">
            pip install --upgrade yol
          </span>{" "}
          {/* Text with space */}
          <ContentCopyIcon className="versionCheck__copy-icon" />{" "}
        </Button>
      </Alert>
    );
  }
  return null;
};

export default VersionCheck;
