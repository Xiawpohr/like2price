pragma solidity 0.6.8;
//SPDX-License-Identifier: MIT

import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract ProfileRegistry {

  // Address for the media on Zora
  address public mediaContract;

  // mapping from address to id to uri
  mapping (address => mapping (uint256 => string)) private _profileURIs;

  // mapping from address to id to estimatedPrice
  mapping (address => mapping (uint256 => uint256)) private _estimatedPrice;

  event Registered(address contractAddr, uint256 indexed id);

  event PriceUpdated(address contractAddr, uint256 indexed id, uint256 price);

  constructor(address _mediaContractAddr) public {
    mediaContract = _mediaContractAddr;
  }

  function register(address _contractAddr, uint256 _id, string calldata _profileURI) external {
    require(_contractAddr == mediaContract, "only support Zora for now");
    require(IERC721(mediaContract).ownerOf(_id) == msg.sender, "only owner can register");
    _profileURIs[_contractAddr][_id] = _profileURI;
    emit Registered(_contractAddr, _id);
  }

  function updateEstimatedPrice(address _contractAddr, uint256 _id, uint256 _price) external {
    require(_contractAddr == mediaContract, "only support Zora for now");
    require(IERC721(mediaContract).ownerOf(_id) == msg.sender, "only owner can register");
    _estimatedPrice[_contractAddr][_id] = _price;
    emit PriceUpdated(_contractAddr, _id, _price);
  }

  function profileURI(address _contractAddr, uint256 _id) public view returns (string memory) {
    return _profileURIs[_contractAddr][_id];
  }

  function getEstimatedPrice(address _contractAddr, uint256 _id) public view returns (uint256) {
    return _estimatedPrice[_contractAddr][_id];
  }

}
