import { getAddress } from '@ethersproject/address'

export function isAddress(value) {
  try {
    return getAddress(value);
  } catch (err) {
    return false;
  }
}

export function shortenAddress(address, digits = 4) {
  if (!isAddress(address)) {
    return null;
    // throw Error(`Invalid 'address' parameter '${address}'.`);
  }
  return `${address.substring(0, digits + 2)}...${address.substring(42 - digits)}`;
}
