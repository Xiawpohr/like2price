import { useState, useCallback, useEffect } from "react";
import { useUserAddress } from "eth-hooks";
import fetch from "isomorphic-fetch";

const BASE_URL = "https://elk.eslitec.com/gf/api";

function generateMessage(contractAddr, tokenId, type, blockNumber) {
  return {
    version: "0.0.1",
    contractAddr,
    tokenId,
    type,
    timestamp: blockNumber,
  };
}

export default function useArtProfile(contractAddr, tokenId, provider) {
  const address = useUserAddress(provider);

  const [itemId, setItemId] = useState("");
  useEffect(() => {
    fetch(`${BASE_URL}/items/id?nft_id=${tokenId}`)
      .then(res => res.json())
      .then(data => {
        setItemId(data.id);
      });
  }, [tokenId]);

  const [likeLoading, setLikeLoading] = useState(false);

  const like = useCallback(async () => {
    try {
      setLikeLoading(true);
      // sign message
      const blockNumber = await provider.getBlockNumber();
      const signer = await provider.getSigner();
      const message = generateMessage(contractAddr, tokenId, "like", blockNumber);
      const sig = await signer.signMessage(JSON.stringify(message));
      console.log(sig);

      // send message
      const item = {
        sig,
        address,
        msg: message,
        type: "likes", // likes, dislikes, followers
        version: 1,
        item: itemId,
      };
      await fetch(`${BASE_URL}/signs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(item),
      });
    } finally {
      setLikeLoading(false);
    }
  }, [contractAddr, tokenId, provider, address, itemId]);

  const [dislikeLoading, setDislikeLoading] = useState(false);

  const dislike = useCallback(async () => {
    try {
      setDislikeLoading(true);
      // sign message
      const blockNumber = await provider.getBlockNumber();
      const signer = await provider.getSigner();
      const message = generateMessage(contractAddr, tokenId, "dislike", blockNumber);
      const sig = await signer.signMessage(JSON.stringify(message));

      // send message
      const item = {
        sig,
        address,
        msg: message,
        type: "dislikes", // likes, dislikes, followers
        version: 1,
        item: itemId,
      };
      await fetch(`${BASE_URL}/signs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(item),
      });
    } finally {
      setDislikeLoading(false);
    }
  }, [contractAddr, tokenId, provider, address, itemId]);

  const [followLoading, setFollowLoading] = useState(false);

  const follow = useCallback(async () => {
    try {
      setFollowLoading(true);
      // sign message
      const blockNumber = await provider.getBlockNumber();
      const signer = await provider.getSigner();
      const message = generateMessage(contractAddr, tokenId, "follow", blockNumber);
      const sig = await signer.signMessage(JSON.stringify(message));

      // send message
      const item = {
        sig,
        address,
        msg: message,
        type: "followers", // likes, dislikes, followers
        version: 1,
        item: itemId,
      };
      await fetch(`${BASE_URL}/signs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(item),
      });
    } finally {
      setFollowLoading(false);
    }
  }, [contractAddr, tokenId, provider, address, itemId]);

  return {
    itemId,
    likeLoading,
    dislikeLoading,
    followLoading,
    like,
    dislike,
    follow,
  };
}
