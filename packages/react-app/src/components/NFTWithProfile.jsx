import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Card, Button, Typography } from "antd";
import { LikeOutlined, DislikeOutlined, TeamOutlined } from "@ant-design/icons";
import { useArtProfile } from "../hooks";
import { shortenAddress } from "../helpers";

const { Title, Paragraph } = Typography;

const MEDIA_CONTRACT = "0x7C2668BD0D3c050703CEcC956C11Bd520c26f7d4";
const BASE_URL = "https://elk.eslitec.com/gf/api";

export default function NFTWithProfile(props) {
  const { item = {}, injectedProvider } = props;

  const { likeLoading, dislikeLoading, followLoading, like, dislike, follow } = useArtProfile(
    item.nft_address,
    item.nft_id,
    injectedProvider,
  );

  const [price, setPrice] = useState();
  useEffect(() => {
    if (item.id) {
      fetch(`${BASE_URL}/price/${item.id}`)
      .then(res => res.json())
      .then(data => {
          setPrice(data.price.toFixed(3));
        });
    }
  }, [item]);

  return (
    <Card
      cover={<img alt="example" src={item.token_uri} />}
      actions={[
        <Button key="like" type="text" icon={<LikeOutlined />} loading={likeLoading} onClick={like}>
          {item.likes}
        </Button>,
        <Button key="dislike" type="text" icon={<DislikeOutlined />} loading={dislikeLoading} onClick={dislike}>
          {item.dislikes}
        </Button>,
        <Button key="follow" type="text" icon={<TeamOutlined />} loading={followLoading} onClick={follow}>
          {item.followers}
        </Button>,
      ]}
    >
      <Link to={`/nfts/${MEDIA_CONTRACT}/${item.nft_id}`}>
        <Title level={4}>{item.nft_name || "artwork name"}</Title>
      </Link>
      <Paragraph strong>Owner: {shortenAddress(item.owner)}</Paragraph>
      <Paragraph strong>Estimated Price: {price} ETH</Paragraph>
    </Card>
  );
}
