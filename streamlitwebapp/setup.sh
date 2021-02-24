mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"arielmadjar1@gemail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
