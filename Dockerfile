FROM python:3.10-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install solana
RUN sh -c "$(curl -sSfL https://release.solana.com/v1.15.2/install)"
ENV PATH=/root/.cargo/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.local/share/solana/install/active_release/bin
RUN solana-keygen new --outfile /root/.config/solana/id.json --no-passphrase
RUN solana config set --url https://metaplex.devnet.rpcpool.com/
RUN solana config set --keypair /root/.config/solana/id.json
RUN key=$(solana address)
RUN echo solana airdrop 2 ${key}
RUN solana airdrop 2 ${key} --url

# Install sugar metaplex 
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
RUN cargo install sugar-cli

COPY . .
