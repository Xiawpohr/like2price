import React, { useState, useCallback } from "react";
import { Link } from "react-router-dom";
import {
  Card,
  Button,
  Typography,
} from "antd";
import { shortenAddress } from "../helpers";

const { Title, Paragraph } = Typography;

const MEDIA_CONTRACT = "0x7C2668BD0D3c050703CEcC956C11Bd520c26f7d4";
const BASE_URL = "https://elk.eslitec.com/gf/api";

export default function NFTWithoutProfile(props) {
  const { item, address, tx, writeContracts } = props;

  const [isLoading, setIsLoading] = useState(false);

  const register = useCallback(
    async (contractAddr, id) => {
      if (!contractAddr || !id) return;

      setIsLoading(true);
      try {
        // create profile on IPFS
        const data = {
          nft_id: id,
          nft_address: contractAddr,
          wallet_address: address,
        };
        const res = await fetch(`${BASE_URL}/items`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
        const profile = await res.json();
        const profileHash = profile.ipns;

        // register profile to Ethereum
        tx(writeContracts.ProfileRegistry.register(contractAddr, id, profileHash));
      } finally {
        setIsLoading(false);
      }
    },
    [address, writeContracts],
  );

  return (
    <Card
      cover={<img alt="example" src={item.image} />}
      actions={[
        <Button key="like" type="text" loading={isLoading} onClick={() => register(MEDIA_CONTRACT, item.id)}>
          Creat Profile
        </Button>,
      ]}
    >
      <Link to={`/nfts/${MEDIA_CONTRACT}/${item.id}`}>
        <Title level={4}>{item.name}</Title>
      </Link>
      <Paragraph strong>Owner: {shortenAddress(item.owner)}</Paragraph>
      <Paragraph strong>Creator: {shortenAddress(item.creator)}</Paragraph>
    </Card>
  );
}
