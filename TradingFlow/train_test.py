from prettytable import PrettyTable as PrettyTable
import random
import warnings

from src.Environment import Environment
from src.Agent import Agent
from src.utils import load_data, print_stats, plot_multiple_conf_interval, load_data_ram


################## INFORMATION ######################
### THIS FILE FOR MODELS LEADERBORS TRAINING ########
#####################################################


def main():
    # ----------------------------- LOAD DATA ---------------------------------------------------------------------------
    data_path = (
        "/home/alxy/Codes/Trading-Bot---Deep-Reinforcement-Learning/user_data/input"
    )
    models_path = "/home/alxy/Codes/Trading-Bot---Deep-Reinforcement-Learning/user_data/models/prod"
    df, last_tick = load_data_ram(days=14)
    print("tain on: ", last_tick)

    # ----------------------------- AGENTS COMPARISON --------------------------------
    REPLAY_MEM_SIZE = 10000
    BATCH_SIZE = 40
    GAMMA = 0.98
    EPS_START = 1
    EPS_END = 0.12
    EPS_STEPS = 300
    LEARNING_RATE = 0.001
    INPUT_DIM = 24
    HIDDEN_DIM = 120
    ACTION_NUMBER = 3
    TARGET_UPDATE = 10
    N_TEST = 10
    TRADING_PERIOD = 2000
    index = random.randrange(len(df) - TRADING_PERIOD - 1)

    dqn_agent = Agent(
        REPLAY_MEM_SIZE,
        BATCH_SIZE,
        GAMMA,
        EPS_START,
        EPS_END,
        EPS_STEPS,
        LEARNING_RATE,
        INPUT_DIM,
        HIDDEN_DIM,
        ACTION_NUMBER,
        TARGET_UPDATE,
        MODEL="dqn",
        DOUBLE=False,
    )
    if str(dqn_agent.device) == "cpu":
        warnings.warn(
            "Device is set to CPU. This will lead to a very slow training. Consider to run pretained models by"
            "executing main.py script instead of train_test.py!"
        )

    double_dqn_agent = Agent(
        REPLAY_MEM_SIZE,
        BATCH_SIZE,
        GAMMA,
        EPS_START,
        EPS_END,
        EPS_STEPS,
        LEARNING_RATE,
        INPUT_DIM,
        HIDDEN_DIM,
        ACTION_NUMBER,
        TARGET_UPDATE,
        MODEL="dqn",
        DOUBLE=True,
    )

    dueling_double_dqn_agent = Agent(
        REPLAY_MEM_SIZE,
        BATCH_SIZE,
        GAMMA,
        EPS_START,
        EPS_END,
        EPS_STEPS,
        LEARNING_RATE,
        INPUT_DIM,
        HIDDEN_DIM,
        ACTION_NUMBER,
        TARGET_UPDATE,
        MODEL="ddqn",
        DOUBLE=True,
    )

    train_size = int(TRADING_PERIOD * 0.8)
    profit_dqn_return = []
    sharpe_dqn_return = []
    profit_ddqn_return = []
    sharpe_ddqn_return = []
    profit_dueling_ddqn_return = []
    sharpe_dueling_ddqn_return = []

    profit_train_env = Environment(df[index : index + train_size], "profit")
    sharpe_train_env = Environment(df[index : index + train_size], "sr")

    # ProfitDQN
    cr_profit_dqn = dqn_agent.train(profit_train_env, models_path)
    profit_train_env.reset()

    # Profit Double DQN
    cr_profit_ddqn = double_dqn_agent.train(profit_train_env, models_path)
    profit_train_env.reset()

    # Profit Dueling Double DQN
    cr_profit_dueling_ddqn = dueling_double_dqn_agent.train(
        profit_train_env, models_path
    )
    profit_train_env.reset()

    i = 0
    while i < N_TEST:
        print("Test nr. %s" % str(i + 1))
        index = random.randrange(len(df) - TRADING_PERIOD - 1)

        profit_test_env = Environment(
            df[index + train_size : index + TRADING_PERIOD], "profit"
        )

        # ProfitDQN
        cr_profit_dqn_test, _ = dqn_agent.test(profit_test_env)
        profit_dqn_return.append(profit_test_env.cumulative_return)
        profit_test_env.reset()

        # Profit Double DQN
        cr_profit_ddqn_test, _ = double_dqn_agent.test(profit_test_env)
        profit_ddqn_return.append(profit_test_env.cumulative_return)
        profit_test_env.reset()

        # Profit Dueling Double DQN
        cr_profit_dueling_ddqn_test, _ = dueling_double_dqn_agent.test(profit_test_env)
        profit_dueling_ddqn_return.append(profit_test_env.cumulative_return)
        profit_test_env.reset()

        i += 1

    dqn_agent = Agent(
        REPLAY_MEM_SIZE,
        BATCH_SIZE,
        GAMMA,
        EPS_START,
        EPS_END,
        EPS_STEPS,
        LEARNING_RATE,
        INPUT_DIM,
        HIDDEN_DIM,
        ACTION_NUMBER,
        TARGET_UPDATE,
        MODEL="dqn",
        DOUBLE=False,
    )

    double_dqn_agent = Agent(
        REPLAY_MEM_SIZE,
        BATCH_SIZE,
        GAMMA,
        EPS_START,
        EPS_END,
        EPS_STEPS,
        LEARNING_RATE,
        INPUT_DIM,
        HIDDEN_DIM,
        ACTION_NUMBER,
        TARGET_UPDATE,
        MODEL="dqn",
        DOUBLE=True,
    )

    dueling_double_dqn_agent = Agent(
        REPLAY_MEM_SIZE,
        BATCH_SIZE,
        GAMMA,
        EPS_START,
        EPS_END,
        EPS_STEPS,
        LEARNING_RATE,
        INPUT_DIM,
        HIDDEN_DIM,
        ACTION_NUMBER,
        TARGET_UPDATE,
        MODEL="ddqn",
        DOUBLE=True,
    )

    # SharpeDQN
    cr_sharpe_dqn = dqn_agent.train(sharpe_train_env, models_path)
    sharpe_train_env.reset()

    # Sharpe Double DQN
    cr_sharpe_ddqn = double_dqn_agent.train(sharpe_train_env, models_path)
    sharpe_train_env.reset()

    # Sharpe Dueling Double DQN
    cr_sharpe_dueling_ddqn = dueling_double_dqn_agent.train(
        sharpe_train_env, models_path
    )
    sharpe_train_env.reset()

    i = 0
    while i < N_TEST:
        print("Test nr. %s" % str(i + 1))
        index = random.randrange(len(df) - TRADING_PERIOD - 1)

        sharpe_test_env = Environment(
            df[index + train_size : index + TRADING_PERIOD], "sr"
        )

        # SharpeDQN
        cr_sharpe_dqn_test, _ = dqn_agent.test(sharpe_test_env)
        sharpe_dqn_return.append(sharpe_test_env.cumulative_return)
        sharpe_test_env.reset()

        # Sharpe Double DQN
        cr_sharpe_ddqn_test, _ = double_dqn_agent.test(sharpe_test_env)
        sharpe_ddqn_return.append(sharpe_test_env.cumulative_return)
        sharpe_test_env.reset()

        # Sharpe Dueling Double DQN
        cr_sharpe_dueling_ddqn_test, _ = dueling_double_dqn_agent.test(sharpe_test_env)
        sharpe_dueling_ddqn_return.append(sharpe_test_env.cumulative_return)
        sharpe_test_env.reset()

        i += 1

    # --------------------------------------- Print Test Stats ---------------------------------------------------------
    t = PrettyTable(
        [
            "Trading System",
            "Avg. Return (%)",
            "Max Return (%)",
            "Min Return (%)",
            "Std. Dev.",
        ]
    )
    print_stats("ProfitDQN", profit_dqn_return, t)
    print_stats("SharpeDQN", sharpe_dqn_return, t)
    print_stats("ProfitDDQN", profit_ddqn_return, t)
    print_stats("SharpeDDQN", sharpe_ddqn_return, t)
    print_stats("ProfitD-DDQN", profit_dueling_ddqn_return, t)
    print_stats("SharpeD-DDQN", sharpe_dueling_ddqn_return, t)

    print(t)
    plot_multiple_conf_interval(
        [
            "ProfitDQN",
            "SharpeDQN",
            "ProfitDDQN",
            "SharpeDDQN",
            "ProfitD-DDQN",
            "SharpeD-DDQN",
        ],
        [
            profit_dqn_return,
            sharpe_dqn_return,
            profit_ddqn_return,
            sharpe_ddqn_return,
            profit_dueling_ddqn_return,
            sharpe_dueling_ddqn_return,
        ],
    )


if __name__ == "__main__":
    main()
