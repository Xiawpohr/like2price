import React, { useState, useEffect, useCallback } from "react";
import { useQuery, gql } from "@apollo/client";
import { useUserAddress } from "eth-hooks";
import { Link } from "react-router-dom";
import { List, Card, Typography, Button, Divider } from "antd";
import { LikeOutlined, DislikeOutlined, TeamOutlined } from "@ant-design/icons";
import fetch from "isomorphic-fetch";
import { useContractLoader } from "../hooks";
import { Transactor, shortenAddress } from "../helpers";
import NFTWithoutProfile from "../components/NFTWithoutProfile";

const { Title, Paragraph } = Typography;

const GET_MEDIA_BY_OWNER = gql`
  query User($address: String!) {
    user(id: $address) {
      collection {
        id
        owner {
          id
        }
        creator {
          id
        }
        contentURI
        metadataURI
      }
    }
  }
`;

export default function Wallet(props) {
  const { userProvider, gasPrice } = props;

  const tx = Transactor(userProvider, gasPrice);

  const address = useUserAddress(userProvider);
  const writeContracts = useContractLoader(userProvider);

  const { loading, error, data } = useQuery(GET_MEDIA_BY_OWNER, {
    variables: { address: (address || "").toLocaleLowerCase() },
  });

  const [arts, setArts] = useState([]);
  useEffect(() => {
    let stale = false;
    if (!loading && !error) {
      const collection = (data.user || "").collection || [];
      Promise.all(collection.map(item => fetch(item.metadataURI)))
        .then(responses => Promise.all(responses.map(res => res.json())))
        .then(metadatas =>
          metadatas.map((metadata, index) => ({
            name: metadata.name,
            id: collection[index].id,
            image: collection[index].contentURI,
            owner: collection[index].owner.id,
            creator: collection[index].creator.id,
          })),
        )
        .then(items => {
          if (!stale) {
            setArts(items);
          }
        });
    }
    return () => {
      stale = true;
    };
  }, [data]);

  return (
    <div style={{ margin: "auto", width: "70vw", paddingTop: "25px" }}>
      <Divider orientation="left">Empty Profile</Divider>
      <List
        grid={{
          gutter: 16,
          column: 3,
        }}
        loading={loading}
        dataSource={arts}
        renderItem={item => (
          <List.Item>
            <NFTWithoutProfile item={item} address={address} tx={tx} writeContracts={writeContracts} />
          </List.Item>
        )}
      />
      {/* <Divider orientation="left">Registered</Divider>
      <List
        grid={{
          gutter: 16,
          column: 3,
        }}
        dataSource={arts}
        renderItem={(item) => (
          <List.Item>
            <Card
            cover={<img alt="example" src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png" />}
            actions={[
              <Button key="like" type="text" icon={<LikeOutlined />}>12</Button>,
              <Button key="dislike" type="text" icon={<DislikeOutlined />}>34</Button>,
              <Button key="follow" type="text" icon={<TeamOutlined />}>23</Button>,
            ]}
          >
            <Link to="/nfts/0xjfnofr/123">
              <Title level={4}>Artwork Name</Title>
            </Link>
            <Paragraph strong>Owner: address</Paragraph>
            <Paragraph strong>Estimated Price: 12 ETH</Paragraph>
          </Card>
          </List.Item>
        )}
      /> */}
    </div>
  );
}
