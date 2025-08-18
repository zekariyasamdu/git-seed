#!/bin/sh
set -e

# Initialize IPFS if first run
if [ ! -f "$IPFS_PATH/config" ]; then
    ipfs init
fi

# Ensure swarm.key is in the right place
cp /data/ipfs/swarm.key $IPFS_PATH/swarm.key

# Start the IPFS daemon in the background
ipfs daemon --enable-pubsub-experiment &
DAEMON_PID=$!

# Wait for daemon to be ready
sleep 5

# Add and pin main branch repo copy
CID=$(ipfs add -r /repo --pin=true | tail -n1 | awk '{print $2}')
echo "Repo main branch pinned with CID: $CID"

# Keep daemon running in foreground
wait $DAEMON_PID
