from gamechain.play import gc_message
from gamechain.play import gamechain
from gamechain.play import gc_state
from gamechain.games import gp_tictactoe

# init_game_msg = "bitcoincash-gc:62baa03f179a69a7974cdf18bd94a9969cb9094cd1540c5797f5d0f43ed6d81c"
# init_game_msg = "bitcoincash-gc:353278db4ff3e77c17c2abc87c59cc9506c7f64ac7fdbbee68d0e1a88a7e3337"
# init_game_msg = "bitcoincash-gc:af6cbfdf7160d59f50199f81fa0f3c9de8710104b2cdf61ffdcd2ec0729118ae"
# init_game_msg = "bitcoincash-gc:08167c7cdfba0af2770ed5ce018d5a48ff56d960ec70d12cf3556c3e013e377f"
init_game_msg = "bitcoincash-gc:196bbabd4806558e52b899561cbe73f51ce65332790a0380c5eaacf63e6ec965"


stt_txid = init_game_msg.split("bitcoincash-gc:")[1]
stt_message = gc_message.receive_message_by_txid(stt_txid)

if stt_message is None or stt_message.msg_type != gc_message.MSG_STT:
    raise Exception(f"Invalid STT transaction: {init_game_msg}")

init_game_msg = stt_message.msg.msg_data
table_addr = stt_message.receiver_addr

game_processor = gp_tictactoe.TicTacToeProcessor()

game_processor.initialize_game(init_game_msg)
player_pubkeys = game_processor.player_pubkeys

game_messages = gamechain.get_game_messages(table_addr, player_pubkeys)
game_messages_so_far = gc_state.build_gc_message_chain(game_messages)

for gm in game_messages_so_far:
    msg_type = gc_message.get_str_for_msg_type(gm.msg_type)
    print(f"GM TURN [{msg_type}]: {gm.msg.msg_data} ({gm.txid})")