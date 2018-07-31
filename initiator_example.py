import datetime
from bitcash import PrivateKeyTestnet

import gcl_secrets
from gamechain.gc_types import GcPrivateKey
from gamechain.lobby import gamechain_lobby, game_shelves
from gamechain.play import gamechain, gc_message_builder

from gamechain.games import gp_tictactoe


def should_play(challenger_game_conditions):
    return True


initiator_key_bc = PrivateKeyTestnet(gcl_secrets.INITIATOR_PRIVATE_KEY)
table_key_bc = PrivateKeyTestnet(gcl_secrets.TABLE_KEY)

initiator_key = GcPrivateKey(initiator_key_bc)
table_key = GcPrivateKey(table_key_bc)
table_addr = table_key.address

JSON_FILE = "initiator.json"

gcl_client = gamechain_lobby.GameChainLobbyClient(initiator_key, JSON_FILE)

my_game_id = "TTT: %s" % datetime.datetime.now()

lfg_txid = gcl_client.look_for_game(game_shelves.GAMESHELF_ID_TIC_TAC_TOE,
                                    my_game_id,
                                    "I go first; I am X")

wtp_msg = gcl_client.wait_for_wtp(lfg_txid)
sender_addr = wtp_msg.sender_addr
challenger_public_key = wtp_msg.msg.public_key_bytes
challenger_game_conditions = wtp_msg.msg.msg_data

p1_addr = initiator_key.address
p1_public_key = initiator_key.public_key
p2_addr = sender_addr
p2_public_key = challenger_public_key

if should_play(challenger_game_conditions):
    print("ISSUING CHALLENGE")
    init_game_msg = gc_message_builder.create_init_game_str_bytes(game_shelves.GAMESHELF_ID_TIC_TAC_TOE,
                                                                  p1_addr, p1_public_key,
                                                                  p2_addr, p2_public_key,
                                                                  challenger_game_conditions)
    padded_my_game_id = gc_message_builder.pad_gameid_to32(my_game_id)
    stt_msg = gc_message_builder.create_set_the_table_message(initiator_key, padded_my_game_id, init_game_msg)
    stt_txid = gcl_client.send_gc_message(table_addr, stt_msg)
    init_game_msg = f"bitcoincash-gc:{stt_txid}"

    gcl_client.accept_wtp(sender_addr, wtp_msg.txid_bytes, init_game_msg)

    game_processor = gp_tictactoe.TicTacToeProcessor()

    gamechain.start_playing(init_game_msg, initiator_key, p1_public_key, JSON_FILE, game_processor)
else:
    gcl_client.reject_wtp(sender_addr)

gcl_client.stop()

