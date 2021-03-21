const { ethers } = require("hardhat");
const {
  Zora,
  constructMediaData,
  constructBidShares,
  sha256FromBuffer,
} = require("@zoralabs/zdk");

async function main() {
  const signers = await ethers.getSigners();
  const zora = new Zora(signers[0], 4);

  const contentHash = await sha256FromBuffer(Buffer.from("human"));
  const metadataHash = await sha256FromBuffer(Buffer.from("human"));

  const mediaData = constructMediaData(
    "https://ipfs.io/ipfs/QmTmFdHtNxepMRJFeqxgBKd5Hx2HmcmHDcbaHqiNUKAUom",
    "https://ipfs.io/ipfs/QmXRUpbLCGUFpgtSikwa94NjkQCrPqhbHY4NQHo1dVMxgp",
    contentHash,
    metadataHash
  );

  const bidShares = constructBidShares(
    10, // creator share
    90, // owner share
    0 // prevOwner share
  );

  const tx = await zora.mint(mediaData, bidShares);
  console.log("Transaction Hash: ", tx.hash);
  await tx.wait(8); // 8 confirmations to finalize

}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
