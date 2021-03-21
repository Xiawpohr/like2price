import React from "react";
import useSWR from "swr";
import {
  List,
  Card,
  Typography,
  Button,
} from "antd";
import { NFTWithProfile } from "../components";

const { Title, Text } = Typography;

const BASE_URL = "https://elk.eslitec.com/gf/api";

export default function Explore(props) {
  const { injectedProvider } = props;
  const { data } = useSWR(`${BASE_URL}/items`);
  console.log(data)

  return (
    <div style={{ margin: "auto", width: "70vw", paddingTop: "25px" }}>
      <List
        grid={{
          gutter: 16,
          column: 3,
        }}
        dataSource={data}
        renderItem={item => (
          <List.Item>
            <NFTWithProfile item={item} injectedProvider={injectedProvider} />
          </List.Item>
        )}
      />
    </div>
  )
}
