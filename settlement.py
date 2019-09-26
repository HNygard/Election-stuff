# Usage
#    python3 settlement.py data.json output.json
#

import math
import json
import sys


data = json.load(open(sys.argv[1]))

votetotals_bergen = data['voteTotals']
number_of_seats_bergen = data['numberOfSeats']

def distribute_seats(votetotals_in,number_of_seats,first_divisor = 1.4, wait = False,Verbose = False,adjustments = {}):
    #Note: The numbers used in votetotals should in most cases be "Stemmelistetall", the number of votes cast multiplied by the number of seats to be distributed,
    #and further modified (subtractions and additions) by personal votes. However, the function will also return correct result if the actual numbers of votes (ballots) cast are used
    #and there are no personal votes considered.
    votetotals = votetotals_in.copy()
    print('Calculating election result from vote totals.')
    print('Number of seats to be distributed: ',number_of_seats)
    print('First divisor:',first_divisor)
    print('Vote totals:')
    print(votetotals)


    #Perform adjustments to vote totals, if any:
    if adjustments:
        for key in adjustments:
            print('Adjusting vote totals for:',key)
            votetotals[key] =  votetotals[key] + adjustments[key]
            print('Vote total for',str(key),'adjusted by',str(adjustments[key]))
            print('New vote total for ',str(key),':',votetotals[key])

    #Create variable to keep track of how many seats have been filled
    awardedseats_total = 0
    
    #Initialize dictionary for quotients 
    quotients = votetotals.copy()

    #Calculate initial quotients (divide vote total by first divisor)
    for key in quotients:
        quotients[key] = quotients[key] / first_divisor

    #Set the initial divisors
    if Verbose:
        print('Setting initial divisors...')
    divisors = dict.fromkeys(votetotals, first_divisor)
    if Verbose:
        print('Initial divisors')
        print(divisors)
    
    #Make an (empty) list of awarded seats
    seats = []
    
    #Make a list of the winning quotient for each seat
    winning_quotients = []
    
    #Make a list of the divisors used to calculate the winning quotient for each seat
    winning_quotient_divisors = []

    #Create dict to keep track of how many seats have been won by each party
    party_seats = dict.fromkeys(votetotals, 0)

    #Create a printable results table  
    result_table = 'Seat #\tWinning party\tDivisor\tQuotient\n'
    result_table = result_table.expandtabs(32)

    while awardedseats_total < number_of_seats:
        if wait == True:
            print('Ready to award seat #',awardedseats_total+1)
            userinput = input('Press Enter to proceed to next seat. Press E + Enter to proceed to end. ')
            if userinput.lower() == 'e':
                wait = False
            print('Input:',userinput)

        if Verbose:
            print('Awarding seat #',awardedseats_total+1,'...')
        #Award the seat to the party with the highest current quotient
        if Verbose:
            print('Current quotients:',quotients)
        seatwinner = max(quotients, key=quotients.get)
        if Verbose:
            print('Winner of seat #',awardedseats_total+1,': ',seatwinner)

        #Update the lists of awarded seats, winning quotients and their divisors
        seats.append(seatwinner)
        winning_quotients.append(quotients[seatwinner])
        winning_quotient_divisors.append(divisors[seatwinner])
        
        if Verbose:
            print('Seats awarded so far:')
            print(seats)

        #Keep track of how many seats have been filled
        awardedseats_total  = len(seats)

        #Append the printable results table
        new_line = str(awardedseats_total)+'\t'+str(seatwinner)+'\t'+str(divisors[seatwinner])+'\t'+'%.3f'%(quotients[seatwinner])+'\n'
        new_line = new_line.expandtabs(32)
        result_table = result_table + new_line
                             
        #Keep track of how many seats won by each party
        party_seats[seatwinner] = party_seats[seatwinner] + 1
        
        #Set the new divisor for the seatwinner
        divisors[seatwinner] = 2*party_seats[seatwinner] + 1

        if Verbose:
            print('New divisor for ',seatwinner,':')
            print(divisors[seatwinner])
        #Calculate the new quotient for the seatwinner:
        quotients[seatwinner] = votetotals[seatwinner] / divisors[seatwinner]
        if Verbose:
            print('New quotient for ',seatwinner,':')
            print(quotients[seatwinner])
        
        if Verbose:
            print('Seats awarded: ',awardedseats_total)

               
    print('SEAT DISTRIBUTION FINISHED.')
    print('Total number of seats awarded:',awardedseats_total)
    print('Seats per party:')
    print(party_seats)

    print(result_table)
    
    return {
        "seats": seats,
        "winning_quotient_divisors": winning_quotient_divisors,
        "winning_quotients": winning_quotients,
        "party_seats": party_seats
    }



print('Bergen #1:')
print('votetotals_bergen:')
print(votetotals_bergen)
result = distribute_seats(votetotals_bergen,number_of_seats_bergen,wait = False)

print('--------- DATA ---------')
print(result)

with open(sys.argv[2], 'w', encoding='utf8') as outfile:
    json.dump(result, outfile, ensure_ascii=False, indent=4, sort_keys=True)