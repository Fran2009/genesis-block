import hashlib
import struct
import time

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
    
    for nonce in range(4294967295):  # Máximo valor para un uint32
        genesis_block_header = create_block_header(coinbase_tx, nTime, nBits, nonce, nVersion)
        genesis_hash = int(sha256d(genesis_block_header)[::-1].hex(), 16)
        print(f"Testing nonce: {nonce}, Hash: 0x{genesis_hash:064x}, Target: 0x{target:064x}", end='\r')
        if genesis_hash < target:
            print()  # Asegura que el siguiente mensaje aparezca en una nueva línea
            return nonce, genesis_hash, sha256d(coinbase_tx).hex()

    print()  # Asegura que el siguiente mensaje aparezca en una nueva línea
    return -1, None, None  # Si no se encuentra un nonce válido

def main():
    timestamp = "La peseta fue la moneda de curso legal en España y sus territorios de ultramar desde su aprobación el 19 de octubre de 1868 hasta el 28 de febrero de 2002"
    pubkey_hex = "0315069ef0eed8ba096147cb2783a37cc7b28869dc79f1220a6085734a06ccf9f0"
    pubkey_script = bytes.fromhex(pubkey_hex) + b'\xac'  # OP_CHECKSIG
    nTime = int(time.time())
    nBits = 0x1d00ffff  # Dificultad estándar de Bitcoin para el bloque génesis
    nVersion = 1
    genesisReward = 5500 * 10**8

    nonce, genesis_hash, hashMerkleRoot = mine_genesis_block(nTime, nBits, nVersion, genesisReward, timestamp, pubkey_script)

    if nonce != -1:
        print(f"Nonce:          {nonce}")
        print(f"Genesis Hash:   0x{genesis_hash:064x}")
        print(f"Merkle Root:    {hashMerkleRoot}")
        print(f"Timestamp:      {nTime}")
        print(f"Pubkey:         {pubkey_hex}")
        print(f"Coins:          {genesisReward}")
        print(f"Psz:            '{timestamp}'")
    else:
        print("No valid nonce found.")

if __name__ == '__main__':
    main()
