import random
import time
from azure.eventhub import EventHubProducerClient, EventData

connection_str = "Endpoint=sb://livestreamnamespace.servicebus.windows.net/;SharedAccessKeyName=livestreamspolicy;SharedAccessKey=T913SsxzLaW0ckm/GWLSxvjtgKjKDSPet+AEhJlGnds=;EntityPath=livestreamdataehub"
event_hub_name = "livestreamdataehub"

# Financial trading parameters
symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
transaction_types = ["BUY", "SELL"]

producer = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=event_hub_name)

def generate_transaction():
    symbol = random.choice(symbols)
    transaction_type = random.choice(transaction_types)

    # Mimic an extremely volatile market with more visible transaction types
    price = round(random.uniform(10, 5000), 2)  # Wider price range for extreme volatility
    quantity = random.randint(100, 3000)  # High volume trades to amplify changes

    # Balance BUY and SELL probabilities dynamically for visible pie chart updates
    if random.random() < 0.3:  # Increase SELL probability slightly
        transaction_type = "SELL"
    else:
        transaction_type = "BUY"

    # Create rapid fluctuations in the market
    if random.random() < 0.5:  # 50% chance of dramatic changes
        price *= random.choice([0.4, 0.6, 1.5, 2])  # Significant price dips or spikes
        quantity *= random.choice([1, 2, 3])

    return {
        "timestamp": time.time(),
        "symbol": symbol,
        "transaction_type": transaction_type,
        "price": price,
        "quantity": quantity
    }

try:
    with producer:
        while True:
            event_data_batch = producer.create_batch()

            for _ in range(50):  # Send 50 transactions per batch for extremely high activity
                transaction = generate_transaction()
                event_data_batch.add(EventData(str(transaction)))

            producer.send_batch(event_data_batch)
            print("Transaction batch sent!")
            time.sleep(0.1)  # Send data every 0.1 seconds for ultra-fast updates
except KeyboardInterrupt:
    print("Transaction simulation stopped.")
