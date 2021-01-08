import numpy as np


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

if __name__ == "__main__": 
    num_websites = 2
    num_of_options = 3
    # website_difference_in_prob_estimation = 0.1
    # website_gain = 0.02

    # payouts_from_websites = create_random_payouts(num_websites, num_of_options, website_gain, website_difference_in_prob_estimation)
    
    payouts_from_websites = np.array([
        [5.8, 3.8, 1.35],
        [4.4, 2.75, 13/20]
    ])
    inverse_payouts = 1. / payouts_from_websites

    # shape of payouts_from_websites is (num_websites, num_options)
    print(inverse_payouts.shape)
    print(np.sum(inverse_payouts, 1))


    # brute force search - 2 options

    # create all options
    options = []
    for i  in range(num_websites):
        for j in range(num_websites):
            for k in range(num_websites):
                choice_for_option1 = i
                choice_for_option2 = j
                choice_for_option3 = k
                options.append((choice_for_option1, choice_for_option2, choice_for_option3))

    # calculate the sum inverse payouts of all the options
    sum_inverse_payouts_list = []
    for selection in options:
        sum_inverse_payouts = 0
        for option, website_choice in enumerate(selection):
            sum_inverse_payouts += inverse_payouts[website_choice, option]
        sum_inverse_payouts_list.append(sum_inverse_payouts)

    I = np.argmin(sum_inverse_payouts_list)
    best_selection = options[I]
    print(sum_inverse_payouts_list)
    print(sum_inverse_payouts_list[I])

    best_sum_inverse_payout = sum_inverse_payouts_list[I]
    expected_return_in_percent = round((1 - best_sum_inverse_payout) * 100, 2)
    if best_sum_inverse_payout < 1:
        print("found profitable selection for betting arbitrage")
        print(f"websites to select each option = {best_selection}")
        print(f"expected return = {expected_return_in_percent} %")
    else:
        print(f"didn't find profitable selection for betting arbitrage")
        print(f"expected loss = {expected_return_in_percent} %")

