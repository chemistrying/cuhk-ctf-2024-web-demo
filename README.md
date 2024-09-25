# cuhk-ctf-2024-web-demo

This repo demostrates some common web vulnerabilities including SQL injection, Cross-site scripting (XSS), and remote code execution (RCE). The challenge should be done without looking at the source code of the repository. However, you will be able to obtain the source code after finishing certain stages in the challenge.

NOTE: PLEASE RUN THIS LOCALLY WITHOUT EXPOSING THE PORT OR THERE MIGHT BE RISKS OF GETTING YOUR COMPUTER COMPROMISED.

# Run the vulnerable server locally
1. Clone the repository.
```sh
git clone https://github.com/chemistrying/cuhk-ctf-2024-web-demo
```
2. Open terminal and change directory to `src`.
```sh
cd src
```
3. Install [docker](https://docs.docker.com/get-started/get-docker/). 
4. Run the server.
```sh
docker compose up
```
You may need to add sudo in front of the command if you haven't set up docker user permission group.


## Flags
Flag Number | Flag Content | Required skills
--- | --- | ---
0 | cuhk24ctf{flag0_w0w_you_know_how_to_read_network_traffic} | Analyse network traffic
1 | cuhk24ctf{flag1_w0w_this_is_probably_your_furst_seek_cool_injection_method} | Basic SQL Injection
2 | cuhk24ctf{flag2_w0w_you_now_know_what_robots_are_seeing} | robots.txt
3 | cuhk24ctf{flag3_w0w_you_know_basic_xss_now} | Basic XSS
4 | cuhk24ctf{flag4_0w0_you_got_admin_password_of_the_website} | Blind SQL Injection
5 | cuhk24ctf{flag5_UwU_this_is_the_final_piece_of_puzzle_probably} | RCE with python code
