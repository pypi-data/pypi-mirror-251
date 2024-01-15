#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import ray.tune as tune
import numpy as np
from typing import List, Union, Callable


def uniform(lower: float, upper: float) -> "tune.sample.Float":
    '''
    Sample a float uniformly between lower and upper.

    :param lower: Lower bound of the sampling range.
    :param upper: Upper bound of the sampling range.
    '''
    return tune.uniform(lower, upper)


def quniform(lower: float, upper: float, q: float) -> "tune.sample.Float":
    '''
    Sample a float uniformly between lower and upper.
    Round the result to nearest value with granularity q, include upper.

    :param lower: Lower bound of the sampling range.
    :param upper: Upper bound of the sampling range.
    :param q: Granularity for increment.
    '''
    return tune.quniform(lower, upper, q)


def loguniform(lower: float, upper: float, base: int=10) -> "tune.sample.Float":
    '''
    Sample a float between lower and upper.
    Power distribute uniformly between log_{base}(lower) and log_{base}(upper).

    :param lower: Lower bound of the sampling range.
    :param upper: Upper bound of the sampling range.
    :param base: Log base for distribution. Default to 10.
    '''
    return tune.loguniform(lower, upper, base)


def qloguniform(lower: float, upper: float, q: float, base: int=10) -> "tune.sample.Float":
    '''
    Sample a float between lower and upper.
    Power distribute uniformly between log_{base}(lower) and log_{base}(upper).
    Round the result to nearest value with granularity q, include upper.

    :param lower: Lower bound of the sampling range.
    :param upper: Upper bound of the sampling range.
    :param q: Granularity for increment.
    :param base: Log base for distribution. Default to 10.
    '''
    return tune.qloguniform(lower, upper, q, base)


def randn(mean: float=0.0, std: float=1.0) -> "tune.sample.Float":
    '''
    Sample a float from normal distribution.

    :param mean: Mean of the normal distribution. Default to 0.0.
    :param std: Std of the normal distribution. Default to 1.0.
    '''
    return tune.randn(mean, std)


def qrandn(mean: float, std: float, q: float) -> "tune.sample.Float":
    '''
    Sample a float from normal distribution.
    Round the result to nearest value with granularity q.

    :param mean: Mean of the normal distribution. Default to 0.0.
    :param std: Std of the normal distribution. Default to 1.0.
    :param q: Granularity for increment.
    '''
    return tune.qrandn(mean, std, q)


def randint(lower: int, upper: int) -> "tune.sample.Integer":
    '''
    Uniformly sample integer between lower and upper. (Both inclusive)

    :param lower: Lower bound of the sampling range.
    :param upper: Upper bound of the sampling range.
    '''
    return tune.randint(lower, upper)


def qrandint(lower: int, upper: int, q: int=1) -> "tune.sample.Integer":
    '''
    Uniformly sample integer between lower and upper. (Both inclusive)
    Round the result to nearest value with granularity q.

    :param lower: Lower bound of the sampling range.
    :param upper: Upper bound of the sampling range.
    :param q: Integer Granularity for increment.
    '''
    return tune.qrandint(lower, upper, q)


def choice(categories: List) -> "tune.sample.Categorical":
    '''
    Uniformly sample from a list

    :param categories: A list to be sampled.
    '''
    return tune.choice(categories)


def choice_n(categories: List, min_items: int, max_items: int) -> "tune.sample.Function":
    """
    Sample a subset from a list

    :param categories: A list to be sampled
    :param min_items: minimum number of items to be sampled
    :param max_items: maximum number of items to be sampled
    """
    return tune.sample_from(
        lambda spec: list(
            np.random.choice(
                categories,
                size=np.random.randint(
                    low=min_items,
                    high=max_items),
                replace=False
            )))


def sample_from(func: Callable) -> Callable:
    '''
    Sample from a function.

    :param func: The function to be sampled.
    '''
    return tune.sample_from(func)


def grid_search(values: List) -> dict:
    '''
    Specifying grid search over a list.

    :param values: A list to be grid searched.
    '''
    return tune.grid_search(values)
