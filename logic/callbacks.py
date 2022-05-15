import pickle
from pathlib import Path

import gym
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.evaluation import evaluate_policy
from tqdm import tqdm


class TqdmCallback(BaseCallback):
    def __init__(self, n_envs: int):
        super().__init__()
        self.progress_bar = None
        self.n_envs = n_envs

    def _on_training_start(self):
        self.progress_bar = tqdm(total=self.locals["total_timesteps"], leave=True)

    def _on_step(self):
        self.progress_bar.update(self.n_envs)
        return True

    def _on_training_end(self):
        # self.progress_bar.close()
        self.progress_bar = None


class SaveOnBestTrainingRewardCallback(BaseCallback):
    def __init__(self, check_freq: int, env_name: str, verbose=1):
        super(SaveOnBestTrainingRewardCallback, self).__init__(verbose)
        self.save_path = Path("data", "models")
        self.save_path.mkdir(exist_ok=True, parents=True)
        self.check_freq = check_freq
        self.best_mean_reward = get_best_score_from_path(self.save_path)
        self.eval_env = gym.make(env_name)
        print("Best score", self.best_mean_reward)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq != 0:
            return True
        self.eval_env.reset()
        mean_reward, std_reward = evaluate_policy(
            self.model, self.eval_env, n_eval_episodes=5, deterministic=True
        )

        # New best model, you could save the agent here
        if mean_reward <= self.best_mean_reward:
            return True

        self.best_mean_reward = mean_reward
        with open(
            Path(self.save_path, "{}_{}.pkl".format(int(mean_reward), int(std_reward))),
            "wb",
        ) as f:
            f.write(pickle.dumps(self.model.get_parameters()))
        return True


def get_best_score_from_path(save_path: Path) -> float:
    best_mean_reward = -999
    for f in save_path.glob("*"):
        current_reward = int(f.name.split("_")[0])
        if current_reward > best_mean_reward:
            best_mean_reward = current_reward
    return float(best_mean_reward)
