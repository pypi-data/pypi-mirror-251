from turtle import forward
from typing import Any
from news_recommender_metrics.RADio.dart_metrics_abstract import DartMetricsAbstract
from news_recommender_metrics.RADio.divergence_metrics import (
    DivergenceMetricAbstract,
    JSDivergence,
)
from news_recommender_metrics.utils.probability_mass_function.probability_mass_function import (
    ProbabilityMassFunction,
)
from news_recommender_metrics.utils.probability_mass_function.rank_aware_probability_mass_function import (
    RankAwareProbabilityMassFunction,
)


class Fragmentation:
    def __init__(
        self,
        is_rank_aware: bool = True,
        rank_weight_method: str = "MMR",
    ) -> None:
        self.is_rank_aware = is_rank_aware
        self.rank_weight_method = rank_weight_method

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.forward(*args, **kwds)

    def forward(
        self,
        recommendations_of_userA: list[str],
        recommendations_of_userB: list[str],
    ) -> float:
        """_summary_

        Parameters
        ----------
        recommendations_of_userA : list[str]
            recommendation result for the user A. it's assumed being sorted by recommendation ranking.
        recommendations_of_userB : list[str]
            recommendation result for the user B. it's assumed being sorted by recommendation ranking.

        Returns
        -------
        float
            Fragmentation of the recommendation results.
        """
        P_dist = (
            RankAwareProbabilityMassFunction.from_ranking(recommendations_of_userA, self.rank_weight_method)
            if self.is_rank_aware
            else ProbabilityMassFunction.from_list(recommendations_of_userA)
        )
        Q_dist = (
            RankAwareProbabilityMassFunction.from_ranking(recommendations_of_userB, self.rank_weight_method)
            if self.is_rank_aware
            else ProbabilityMassFunction.from_list(recommendations_of_userB)
        )
        calculator = JSDivergence()
        return calculator.calc(P_dist.pmf, Q_dist.pmf)
