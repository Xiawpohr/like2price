import React from "react";
import { PageHeader } from "antd";

// displays a page header

export default function Header() {
  return (
    <a href="/">
      <PageHeader
        title="Like2Price"
        subTitle="switch to Rinkeby and try it"
        style={{ cursor: "pointer" }}
      />
    </a>
  );
}
