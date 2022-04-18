def entry_exit(price, shares, commission, fee, buy_or_sell):

    overhead = 2*(commission+fee)/shares

    if buy_or_sell == 'buy':
        next_price = price+overhead
    else:
        next_price = price-overhead
        
    return(next_price)
