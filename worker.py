import book
import api
import json
import sys
from engine import EngineFPC


def main():
    api_handler = api.Api(
        "https://variants.gcp-prod.chess.com/bot", "SK3slkj3Da", "v2.0.0-beta")
    engine_handler = EngineFPC(f"{sys.executable} 4pc-sunfish.py", api_handler)
    # https://variants.gcp-sandbox.chess-platform.com/bot/
    # https://variants.gcp-prod.chess.com/bot
    start_fen_rbg = "R-0,0,0,0-1,1,1,1-1,1,1,1-0,0,0,0-0-x,x,x,yR,yN,yB,yK,yQ,yB,yN,yR,x,x,x/x,x,x,yP,yP,yP,yP,yP,yP,yP,yP,x,x,x/x,x,x,8,x,x,x/bR,bP,10,gP,gR/bN,bP,10,gP,gN/bB,bP,10,gP,gB/bQ,bP,10,gP,gK/bK,bP,10,gP,gQ/bB,bP,10,gP,gB/bN,bP,10,gP,gN/bR,bP,10,gP,gR/x,x,x,8,x,x,x/x,x,x,rP,rP,rP,rP,rP,rP,rP,rP,x,x,x/x,x,x,rR,rN,rB,rK,rQ,rB,rN,rR,x,x,x"
    start_fen_new = "R-0,0,0,0-1,1,1,1-1,1,1,1-0,0,0,0-0-x,x,x,yR,yN,yB,yK,yQ,yB,yN,yR,x,x,x/x,x,x,yP,yP,yP,yP,yP,yP,yP,yP,x,x,x/x,x,x,8,x,x,x/bR,bP,10,gP,gR/bN,bP,10,gP,gN/bB,bP,10,gP,gB/bQ,bP,10,gP,gK/bK,bP,10,gP,gQ/bB,bP,10,gP,gB/bN,bP,10,gP,gN/bR,bP,10,gP,gR/x,x,x,8,x,x,x/x,x,x,rP,rP,rP,rP,rP,rP,rP,rP,x,x,x/x,x,x,rR,rN,rB,rQ,rK,rB,rN,rR,x,x,x"
    start_fen_byg = "R-0,0,0,0-1,1,1,1-1,1,1,1-0,0,0,0-0-x,x,x,yR,yN,yB,yQ,yK,yB,yN,yR,x,x,x/x,x,x,yP,yP,yP,yP,yP,yP,yP,yP,x,x,x/x,x,x,8,x,x,x/bR,bP,10,gP,gR/bN,bP,10,gP,gN/bB,bP,10,gP,gB/bQ,bP,10,gP,gK/bK,bP,10,gP,gQ/bB,bP,10,gP,gB/bN,bP,10,gP,gN/bR,bP,10,gP,gR/x,x,x,8,x,x,x/x,x,x,rP,rP,rP,rP,rP,rP,rP,rP,x,x,x/x,x,x,rR,rN,rB,rQ,rK,rB,rN,rR,x,x,x"
    start_fen_old = "R-0,0,0,0-1,1,1,1-1,1,1,1-0,0,0,0-0-x,x,x,yR,yN,yB,yK,yQ,yB,yN,yR,x,x,x/x,x,x,yP,yP,yP,yP,yP,yP,yP,yP,x,x,x/x,x,x,8,x,x,x/bR,bP,10,gP,gR/bN,bP,10,gP,gN/bB,bP,10,gP,gB/bK,bP,10,gP,gQ/bQ,bP,10,gP,gK/bB,bP,10,gP,gB/bN,bP,10,gP,gN/bR,bP,10,gP,gR/x,x,x,8,x,x,x/x,x,x,rP,rP,rP,rP,rP,rP,rP,rP,x,x,x/x,x,x,rR,rN,rB,rQ,rK,rB,rN,rR,x,x,x"
    start_fen_by = "R-0,0,0,0-1,1,1,1-1,1,1,1-0,0,0,0-0-x,x,x,yR,yN,yB,yQ,yK,yB,yN,yR,x,x,x/x,x,x,yP,yP,yP,yP,yP,yP,yP,yP,x,x,x/x,x,x,8,x,x,x/bR,bP,10,gP,gR/bN,bP,10,gP,gN/bB,bP,10,gP,gB/bQ,bP,10,gP,gQ/bK,bP,10,gP,gK/bB,bP,10,gP,gB/bN,bP,10,gP,gN/bR,bP,10,gP,gR/x,x,x,8,x,x,x/x,x,x,rP,rP,rP,rP,rP,rP,rP,rP,x,x,x/x,x,x,rR,rN,rB,rQ,rK,rB,rN,rR,x,x,x"
    did_greeting = False
    game_start_log = True
    depth = nodes = 0
    # book_handler = book.Book(0, "blank.book")
    did_not_game_search = True
    eval = mainline_book = start_fen = ""
    while True:
        did_greeting = False
        game_start_log = True
        if (did_not_game_search):
            did_not_game_search = False
            print("_________________________________")
            print("Awaiting a game to start...")
        response = api_handler.stream()
        lines = response.iter_lines()
        next(lines)
        while True:
            try:
                state = json.loads(next(lines).decode('utf-8'))
                if "info" in state and state['info'] == "no game found":
                    break
                if (game_start_log):
                    game_start_log = False
                    print("_________________________________")
                    print("Starting game...")
                did_not_game_search = True
                if "move" in state:
                    if state['info'] == "it's your turn":
                        san = state['move']['san']
                        if not did_greeting:
                            # mainline_book += san
                            did_greeting = True
                        else:
                            # mainline_book += " " + san
                        # book_move = book_handler.get_book_move(mainline_book)
                        # if book_move != "":
                        #     print("_________________________________")
                        #     print("Playing book move `" + book_move + "`.`")
                        #     api_handler.play(book_move)
                        #     mainline_book += " " + book_move
                        
                        
                        # else: # indent lines 62-77 (both inclusive) when uncommenting and trying to add book again
                            print("_________________________________")
                            print("Looking for an engine move...")
                            print("_________________________________")
                            fen = state['move']['fen'].replace("\n", "")
                            if (engine_handler.search_fen_str(fen, 9) == 'search complete'):
                                latest_info = engine_handler.move_info[-1]
                            depth_reached, nodes_reached, bestmove_found, pos_eval, elapsed, pvline = engine_handler.decode_uci_move(
                                latest_info)
                            eval = pos_eval
                            print("_________________________________")
                            print("CPEval(depth:"+str(depth_reached)+",nodes="+str(
                                nodes_reached)+",bestmove="+bestmove_found+",posScore="+pos_eval+")")
                            print("_________________________________")
                            print("Playing engine move `" +
                                  bestmove_found + "`.`")
                            api_handler.play(bestmove_found)
                    if state['info'] == "Game over":
                        api_handler.chat("gg")
                        break
                else:
                    if "info" in state and state['info'] == "it's your turn":
                        if not did_greeting:
                            did_greeting = True
                        # book_move = book_handler.get_book_move(mainline_book)
                        # if book_move != "":
                        #     print("_________________________________")
                        #     print("Playing book move `" + book_move + "`.`")
                        #     # sleep(1)
                        #     api_handler.play(book_move)
                        #     mainline_book += book_move
                        
                        # else:
                            print("_________________________________")
                            print("Looking for an engine move...")
                            print("_________________________________")
                            fen = state['fen4'].replace("\n", "")
                            if "4PCo" == fen:
                                start_fen = start_fen_old
                            elif "4PC" == fen:
                                start_fen = start_fen_new
                            elif "4PCb" == fen:
                                start_fen = start_fen_by
                            elif "4PCn" == fen:
                                start_fen = start_fen_byg
                            else:
                                start_fen = fen
                            if (engine_handler.search_fen_str(start_fen, 9) == 'search complete'):
                                latest_info = engine_handler.move_info[-1]
                            depth_reached, nodes_reached, bestmove_found, pos_eval, elapsed, pvline = engine_handler.decode_uci_move(
                                latest_info)
                            eval = pos_eval
                            print("_________________________________")
                            print("CPEval(depth:"+str(depth_reached)+",nodes="+str(
                                nodes_reached)+",bestmove="+bestmove_found+",posScore="+pos_eval+")")
                            print("_________________________________")
                            print("Playing engine move `" +
                                  bestmove_found + "`.`")
                            api_handler.play(bestmove_found)
                if "info" in state and state['info'] == "Game over":
                    api_handler.chat("gg")
                    break
            except StopIteration:
                break


if __name__ == '__main__':
    main()
