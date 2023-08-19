import React from "react";
import "./UserMessage.css";
const UserMessage = ({ message }) => {
  return (
    <div className="btn">
      <div>{message}</div>
    </div>
  );
};

export default UserMessage;
