# 警告: pickle モジュールは安全ではありません。信頼できるデータのみを非 pickle 化してください。
# https://docs.python.org/ja/3/library/pickle.html
import pickle

test_data = b"\x80\x04\x95C\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\n_permanent\x94\x88\x8c\rcurrent_index\x94K\x00\x8c\x04auth\x94\x89\x8c\tquestions\x94]\x94(K\x05K\x08K\x06eu."
print(pickle.loads(test_data))