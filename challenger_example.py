from bitcash import PrivateKeyTestnet
import gcl_secrets
from gamechain.gc_types import GcPrivateKey
from gamechain.lobby import gamechain_lobby, game_shelves, gcl_message
from gamechain.play import gamechain
from gamechain.games import gp_tictactoe

challenger_key_bc: PrivateKeyTestnet = PrivateKeyTestnet(gcl_secrets.CHALLENGER_PRIVATE_KEY)
challenger_key = GcPrivateKey(challenger_key_bc)
JSON_FILE = "challenger.json"

gcl_client = gamechain_lobby.GameChainLobbyClient(challenger_key, JSON_FILE)

lfg_msg = gcl_client.wait_for_lfg(game_shelves.GAMESHELF_ID_TIC_TAC_TOE)

initiator_public_key = lfg_msg.msg.public_key_bytes

print(f"CTX: {lfg_msg}")

alt_conditions = ""
wtp_tx_id = gcl_client.offer_willing_to_play(lfg_msg.sender_addr, lfg_msg.txid_bytes, alt_conditions)

cr = gcl_client.wait_for_challenge_response(wtp_tx_id, initiator_public_key)

if cr.msg_type == gcl_message.MSG_ACC:
    init_game_msg = cr.msg.msg_data
    print(f"ACCEPTED - GAME INIT: {init_game_msg}")

    game_processor = gp_tictactoe.TicTacToeProcessor()

    gamechain.start_playing(init_game_msg, challenger_key, initiator_public_key, JSON_FILE, game_processor)
elif cr.msg_type == gcl_message.MSG_REJ:
    print("REJECTED :(")


gcl_client.stop()
