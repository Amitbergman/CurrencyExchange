import numpy as np
import itertools
import time
import matplotlib.pyplot as plt

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
    t1 = time.time()
    for selection in itertools.product(*all_possible_selections):
        sum_inverse_payouts = calc_sum_inverse_payouts(selection, inverse_payouts)

        # save selection of bes and the sum inverse payouts
        list_of_selections.append(selection)
        sum_inverse_payouts_list.append(sum_inverse_payouts)
    t2 = time.time()
    # print(f"=> {len(sum_inverse_payouts_list)} selections reviewed in {t2 - t1} seconds ")

    # find best selection and calculate return
    I = np.argmin(sum_inverse_payouts_list)
    best_selection = list_of_selections[I]
    best_sum_inverse_payout = sum_inverse_payouts_list[I]
    expected_return_in_percent = round((1 - best_sum_inverse_payout) * 100, 2)

    return expected_return_in_percent, best_selection


def make_selections_readable(best_selection):
    return {f"option{i}": f"website{website}" for i, website in enumerate(best_selection)}


def calculate_mean_returns(num_averaging, num_websites, num_of_options, website_gain, website_difference_in_prob_estimation):
    # calculated_mean_returns
    returns_list = []
    for repeat in range(num_averaging):
        # generate random payouts_from_websites: shape = (num_websites, num_options)
        payouts_from_websites = create_random_payouts(num_websites, num_of_options, website_gain, website_difference_in_prob_estimation)

        # brute force search for betting arbitrage
        expected_return_in_percent, best_selection = brute_force_search(num_websites, num_of_options, payouts_from_websites)
        returns_list.append(expected_return_in_percent)  
    mean_returns = np.mean(returns_list)
    max_returns = np.max(returns_list)

    print(f"num_websites={num_websites}, num_of_options={num_of_options}, mean_returns={mean_returns}, max_returns={max_returns}")
    return mean_returns, max_returns


def plot_results(returns_array, title):
    fig, ax = plt.subplots(figsize=(10, 4))
    ms = ax.matshow(returns_array)
    x_ticks = [str(websites_list[0])] + [str(xx) for xx in websites_list]
    y_ticks = [str(options_list[0])] + [str(yy) for yy in options_list]
    ax.xaxis.tick_bottom()
    ax.set_xticklabels(x_ticks)
    ax.set_yticklabels(y_ticks)
    
    plt.xlabel("number of websites")
    plt.ylabel("number of betting options")

    cbar = fig.colorbar(ms,ticks = np.arange(np.min(returns_array), np.max(returns_array)+1))
    cbar.set_label(f'{title} return percentage')

    method_of_calculated = "averaged" if title == "mean" else "calculated"
    plt.title(f"{title} return percentage, {method_of_calculated} over {num_averaging} runs")
    plt.show()


if __name__ == "__main__": 
    # num_websites = 2
    # num_of_options = 10
    num_averaging = 100
    website_difference_in_prob_estimation = 0.3
    website_gain = 0.2
    verbose = True

    # select how many options to consider
    num_websites_range = [5,14] # the runtime grows polynomically depending on this variable
    num_options_range = [2,4] # the runtime grows exponentially depending on this variable
    
    websites_list = list(range(*num_websites_range))
    options_list = list(range(*num_options_range))
    websites, options = np.meshgrid(websites_list, options_list)
    mean_returns_array = np.zeros_like(websites).astype(np.float32)
    max_returns_array = np.zeros_like(websites).astype(np.float32)
    # calculate mean returns
    for i, num_websites in enumerate(range(*num_websites_range)):
        for j, num_of_options in enumerate(range(*num_options_range)):

            mean_returns_array[j,i], max_returns_array[j,i] = calculate_mean_returns(num_averaging, num_websites, num_of_options, website_gain, website_difference_in_prob_estimation)

    plot_results(mean_returns_array, title="mean")
    plot_results(max_returns_array, title="max")
