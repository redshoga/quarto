class Quatro:
    def __init__(self, board_size=4):
        self.__board_size = board_size
        self.__board = [None] * 2 ** self.__board_size
        # self.__board = list(range(2 ** self.__board_size))
        # self.__board = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
        self.__remaining_pieces = list(range(2 ** self.__board_size))
        self.__remaining_places = self.__remaining_pieces[:]
        self.__turn = 0

    def get_turn(self):
        return self.__turn

    def get_remaining_pieces(self):
        return self.__remaining_pieces

    def get_remaining_places(self):
        return self.__remaining_places

    def print_board(self):
        # https://iogi.hatenablog.com/entry/split-list-into-sublist
        sub_lists = list(zip(*[iter(self.__board)]*self.__board_size))
        for row_list in sub_lists:
            print(" ".join(
                map(lambda x: self.__piece_to_bin(x), row_list)
            ))

    def __piece_to_bin(self, num):
        if num == None:
            return "_" * self.__board_size
        formatStr = "{0:{fill}" + str(self.__board_size) + "b}"
        return formatStr.format(num, fill='0')

    def set_piece(self, piece, place):
        if (piece in self.get_remaining_pieces() and place in self.get_remaining_places()) == False:
            return False

        self.__remaining_pieces.remove(piece)
        self.__remaining_places.remove(place)
        self.__board[place] = piece
        self.__turn += 1
        return True

    def __board_row(self, idx):
        return self.__board[self.__board_size*idx: self.__board_size*(idx+1)]

    def __board_column(self, idx):
        return self.__board[idx::self.__board_size]

    def __board_diag(self, idx):
        if idx == 0:
            return [ self.__board[(self.__board_size+1) * n] for n in range(self.__board_size)]
        if idx == 1:
            return [ self.__board[(self.__board_size-1) * (n+1)] for n in range(self.__board_size)]

    # self.__check_complete([1,2,4,8]) # False
    # self.__check_complete([3,2,8,0]) # True
    # self.__check_complete([12,9,10,8]) # True
    # self.__check_complete([9,6,8,4]) # False
    def __check_complete(self, line_list):
        if None in line_list:
            return False

        all_one = 2 ** self.__board_size-1

        complete_0 = None
        complete_1 = None

        tmp = all_one
        for val in line_list:
            tmp = tmp & val
        complete_0 = tmp == 0

        tmp = 0
        for val in line_list:
            tmp = tmp | val
        complete_1 = tmp == all_one

        return complete_0 ^ complete_1

    def is_end(self):
        for i in range(self.__board_size):
            if self.__check_complete(self.__board_row(0)):
                return True
            if self.__check_complete(self.__board_column(0)):
                return True
        for i in range(2):
            if self.__check_complete(self.__board_diag(0)):
                return True
        return False

if __name__ == "__main__":
    game = Quatro()
    while True:
        print("TURN:", game.get_turn() + 1)
        game.print_board()

        if game.is_end():
            print("END")
            exit()

        print("USEABLE PIECE:", game.get_remaining_pieces())
        print("USEABLE PLACE:", game.get_remaining_places())

        while True:
            print("PIECE?")
            use_piece = int(input())
            print("PLACE?")
            use_PLACE = int(input())

            if game.set_piece(use_piece, use_PLACE):
                break
            
            print("NOT USEABLE")

        print("---------------")
