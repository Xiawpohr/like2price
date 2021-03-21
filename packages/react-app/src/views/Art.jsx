import React, { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import { useQuery, gql } from '@apollo/client';
import useSWR from "swr";
import {
  Row,
  Col,
  Space,
  List,
  Image,
  Typography,
  Input,
  Button,
  Statistic,
  Empty,
} from 'antd'
import {
  LikeOutlined,
  DislikeOutlined,
  TeamOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons";
import fetch from "isomorphic-fetch";
import { useArtProfile } from "../hooks";
import { shortenAddress } from "../helpers";

const { Title, Paragraph, Link } = Typography;

const GET_MEDIA = gql`
  query Media($id: String!) {
    media(id: $id) {
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
`;

const BASE_URL = "https://elk.eslitec.com/gf/api";

export default function Art(props) {
  const { userProvider, userAddress } = props;
  const { address, id } = useParams();

  const { itemId, likeLoading, dislikeLoading, followLoading, like, dislike, follow } = useArtProfile(
    address,
    id,
    userProvider,
  );

  const { data: itemData = {} } = useSWR(`${BASE_URL}/items/${itemId}`);

  const { loading, error, data } = useQuery(GET_MEDIA, {
    variables: { id },
  });

  const [name, setName] = useState("");
  useEffect(() => {
    let stale = false;
    if (data && data.media) {
      fetch(data.media.metadataURI)
        .then(res => res.json())
        .then(metadata => {
          if (!stale) {
            setName(metadata.name);
          }
        });
    }

    return () => {
      stale = true;
    };
  }, [data]);

  const [price, setPrice] = useState();
  useEffect(() => {
    if (itemId) {
      fetch(`${BASE_URL}/price/${itemId}`)
        .then(res => res.json())
        .then(d => {
          setPrice(d.price.toFixed(3));
        });
    }
  }, [itemId]);

  if (error || !data || (data && !data.media)) {
    return <Empty />;
  }

  return (
    <div style={{ margin: "auto", width: "70vw", paddingTop: "25px" }}>
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Image src={data.media.contentURI} />
        </Col>
        <Col span={12}>
          <Title level={3}>{name}</Title>
          <Link href={`https://gateway.ipfs.io/ipns/${itemData.ipns}`} target="_blank">Profile</Link>
          <Paragraph>Owner: {shortenAddress(data.media.owner.id)}</Paragraph>
          <Paragraph>Creator: {shortenAddress(data.media.creator.id)}</Paragraph>
          <Paragraph>Estimated Price: {price} ETH</Paragraph>
          <div style={{ marginTop: "24px" }}>
            <Space>
              <Input type="number" suffix="ETH" />
              <Button>Bid</Button>
            </Space>
          </div>
          <div style={{ marginTop: "24px" }}>
            <Row>
              <Col span={8}>
                <Statistic
                  title="Likes"
                  value={itemData.likes}
                  prefix={<Button type="text" icon={<LikeOutlined />} loading={likeLoading} onClick={like} />}
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="Dislikes"
                  value={itemData.dislikes}
                  prefix={<Button type="text" icon={<DislikeOutlined />} loading={dislikeLoading} onClick={dislike} />}
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="Followers"
                  value={itemData.followers}
                  prefix={<Button type="text" icon={<TeamOutlined />} loading={followLoading} onClick={follow} />}
                />
              </Col>
            </Row>
          </div>
          {/* <div style={{ marginTop: "24px" }}>
            <List
              header="Likes"
              bordered
              dataSource={likeData}
              renderItem={item => (
                <List.Item
                  actions={[
                    <a><SafetyCertificateOutlined /></a>
                  ]}
                >
                  <Address value={item.address} />
                </List.Item>
              )}
            />
          </div>
          <div style={{ marginTop: "24px" }}>
            <List
              header="DisLikes"
              bordered
              dataSource={likeData}
              renderItem={(item) => (
                <List.Item
                  actions={[
                    <a><SafetyCertificateOutlined /></a>
                  ]}
                >
                  <Address value={item.address} />
                </List.Item>
              )}
            />
          </div> */}
        </Col>
      </Row>
    </div>
  )
}
