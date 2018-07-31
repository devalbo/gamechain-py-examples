from gamechain.play import gc_message
from gamechain.comm import gc_comm

txid = "1e31c70e74454c140c7eb3df196cdfe6f6670a4cf43e532a6e8715164243efcb"

sender_addr, receiver_addr, op_return_asms = gc_comm.get_sender_receiver_op_returns_by_txid(txid)
op_return_msg = gc_message.join_gc_op_returns(op_return_asms)

print(op_return_msg)

