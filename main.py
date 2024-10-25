
from api.interface import get_trades

                
def main():
    positions = get_trades()
    open_positions = []
    closed_positions = []
    for position in positions: 
        if position.is_open == False:
            closed_positions.append(position)
        else:
            open_positions.append(position)





if __name__ == "__main__":
    main()