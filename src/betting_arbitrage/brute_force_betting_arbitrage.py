import numpy as np
import itertools


def create_random_payouts(num_websites, num_of_options, website_gain, website_difference_in_prob_estimation):
        p_true = np.random.rand(num_of_options)
        p_true = p_true / np.sum(p_true)

        # create 
        payouts_from_websites = []
        for i in range(num_websites):
            website_p_estimation = p_true + website_difference_in_prob_estimation * np.random.rand(num_of_options)
            website_p_estimation = website_p_estimation / np.sum(website_p_estimation)
            p_website_offer = website_p_estimation + website_gain * np.random.rand(num_of_options)
            payouts = 1. / p_website_offer
            payouts_from_websites.append(payouts)

        payouts_from_websites = np.array(payouts_from_websites)
        return payouts_from_websites


def calc_sum_inverse_payouts(selection, inverse_payouts):
    sum_inverse_payouts = 0
    for option, website_choice in enumerate(selection):
        sum_inverse_payouts += inverse_payouts[website_choice, option]
    return sum_inverse_payouts



def brute_force_search(num_websites, num_of_options, payouts_from_websites):
    inverse_payouts = 1 / payouts_from_websites

    # create all options
    all_possible_selections = [list(range(num_websites)) for _ in range(num_of_options)]

    # calculate the sum inverse payouts of all the options
    sum_inverse_payouts_list = []
    list_of_selections = []
    for selection in itertools.product(*all_possible_selections):
        sum_inverse_payouts = calc_sum_inverse_payouts(selection, inverse_payouts)

        # save selection of bes and the sum inverse payouts
        list_of_selections.append(selection)
        sum_inverse_payouts_list.append(sum_inverse_payouts)

    print(f"num possible selecitons reviewed = {len(sum_inverse_payouts_list)}")

    # find best selection and calculate return
    I = np.argmin(sum_inverse_payouts_list)
    best_selection = list_of_selections[I]
    best_sum_inverse_payout = sum_inverse_payouts_list[I]
    expected_return_in_percent = round((1 - best_sum_inverse_payout) * 100, 2)

    return expected_return_in_percent, best_selection


if __name__ == "__main__": 
    num_websites = 2
    num_of_options = 3
    website_difference_in_prob_estimation = 0.1
    website_gain = 0.02
    verbose = False

    # generate random payouts_from_websites: shape = (num_websites, num_options)
    payouts_from_websites = create_random_payouts(num_websites, num_of_options, website_gain, website_difference_in_prob_estimation)

    # visual inspection
    if verbose:
        inverse_payouts = 1. / payouts_from_websites
        sum_inhouse_inverse_payouts = np.sum(inverse_payouts, 1)
        percantage_gain_of_house = np.round((sum_inhouse_inverse_payouts - 1) * 100, 2)
        print(f"house proffit = {percantage_gain_of_house} percent")
        print(f"shape of inverse payout array = {inverse_payouts.shape}")

    # brute force search for betting arbitrage
    expected_return_in_percent, best_selection = brute_force_search(num_websites, num_of_options, payouts_from_websites)
    
    # final printout
    print("\n\n=========================")
    if expected_return_in_percent > 0:
        print("YAY found a profitable selection for betting arbitrage! :)")
        print(f"websites to select each option = {best_selection}")
        print(f"expected return of investment = +{expected_return_in_percent} %")
    else:
        print(f"OH didn't find a profitable selection for betting arbitrage :(")
        print(f"expected loss of investment = {expected_return_in_percent} %")

