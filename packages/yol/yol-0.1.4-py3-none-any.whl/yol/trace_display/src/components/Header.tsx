import React from "react";
import Button from "@material-ui/core/Button";
import "./Header.css";
import VersionCheck from "./VersionCheck";
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

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header__logo">YOL</div>
      <VersionCheck />
      <Button
        variant="contained"
        className="header__feedback"
        href="https://forms.gle/WSyYjaa8B7cYHTuu5"
        target="_blank"
        rel="noopener noreferrer"
      >
        Feedback
      </Button>
    </header>
  );
};

export default Header;