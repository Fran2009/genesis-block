import hashlib
import struct
import time
import argparse

def sha256d(data):
    """Aplica sha256 dos veces para crear un hash doble."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def create_coinbase_transaction(pszTimestamp, pubkey_script, genesisReward):
    """Crea la transacción coinbase para el bloque génesis."""
    script_len = len(pszTimestamp).to_bytes(1, byteorder='little')
    coinbase_script = b'\x04' + script_len + pszTimestamp
    vin = struct.pack('<32sI', b'\x00' * 32, 0xffffffff) + struct.pack('<B', len(coinbase_script)) + coinbase_script + struct.pack('<I', 0xffffffff)
    vout = struct.pack('<Q', genesisReward) + struct.pack('<B', len(pubkey_script)) + pubkey_script
    tx = struct.pack('<i', 1) + struct.pack('<B', 1) + vin + struct.pack('<B', 1) + vout + struct.pack('<I', 0)
    return tx

def create_block_header(coinbase_tx, nTime, nBits, nNonce, nVersion):
    """Crea la cabecera del bloque."""
    merkle_root = sha256d(coinbase_tx)
    return struct.pack('<i', nVersion) + b'\x00' * 32 + merkle_root + struct.pack('<III', nTime, nBits, nNonce)

def get_target(nBits):
    """Convierte nBits a un target hash usando la fórmula especificada."""
    exponent = (nBits >> 24) & 0xff
    target = nBits * (2**(8*(exponent - 3)))
    return target

def mine_genesis_block(nTime, nBits, nVersion, genesisReward, pszTimestamp, pubkey_script):
    """Minar el bloque génesis buscando un nonce válido."""
    coinbase_tx = create_coinbase_transaction(pszTimestamp.encode('utf-8'), pubkey_script, genesisReward)
    target = get_target(nBits)
    
    for nonce in range(4294967295):
        genesis_block_header = create_block_header(coinbase_tx, nTime, nBits, nonce, nVersion)
        genesis_hash = int(sha256d(genesis_block_header)[::-1].hex(), 16)
        print(f"Testing nonce: {nonce}, Hash: 0x{genesis_hash:064x}, Target: 0x{target:064x}", end='\r')
        if genesis_hash < target:
            print()
            return nonce, genesis_hash, sha256d(coinbase_tx).hex()

    print()
    return -1, None, None

def parse_args():
    parser = argparse.ArgumentParser(description='Genesis Block Miner for a Custom Cryptocurrency')
    parser.add_argument('-z', '--timestamp', help='Custom timestamp for the genesis block.', default="La peseta fue la moneda de curso legal en España y sus territorios de ultramar desde su aprobación el 19 de octubre de 1868 hasta el 28 de febrero de 2002")
    parser.add_argument('-t', '--time', help='UNIX timestamp for the genesis block.', type=int, default=int(time.time()))
    parser.add_argument('-p', '--pubkey', help='Public key hex string for the genesis block.', default="0315069ef0eed8ba096147cb2783a37cc7b28869dc79f1220a6085734a06ccf9f0")
    parser.add_argument('-r', '--reward', help='Genesis block reward.', type=int, default=5500 * 10**8)
    return parser.parse_args()

def main():
    args = parse_args()
    nonce, genesis_hash, hashMerkleRoot = mine_genesis_block(args.time, 0x1d00ffff, 1, args.reward, args.timestamp, bytes.fromhex(args.pubkey))
    
    if nonce != -1:
        print(f"Nonce:          {nonce}")
        print(f"Genesis Hash:   0x{genesis_hash:064x}")
        print(f"Merkle Root:    {hashMerkleRoot}")
        print(f"Timestamp:      {args.time}")
        print(f"Pubkey:         {args.pubkey}")
        print(f"Coins:          {args.reward}")
        print(f"Psz:            '{args.timestamp}'")
    else:
        print("No valid nonce found.")

if __name__ == '__main__':
    main()
